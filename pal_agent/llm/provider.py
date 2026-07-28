"""LLM providers behind one interface (N4: all module I/O is validated JSON).

- ``StubProvider``   deterministic, offline — used in tests and when no model is
  configured. Never calls out; returns canned/echoed content.
- ``ClaudeCLIProvider`` shells out to the ``claude`` CLI (subscription, no API key).

``get_provider()`` picks Claude when the CLI is on PATH, else the stub. Every
``structured()`` result is validated against a JSON Schema and retried once on a
schema miss, so downstream modules can trust the shape.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import urllib.error
import urllib.request

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None


class SchemaError(ValueError):
    """Raised when a provider cannot produce output matching the schema."""


def validate_output(obj: dict, schema: dict) -> dict:
    """Validate ``obj`` against ``schema`` (no-op if jsonschema is absent)."""
    if jsonschema is not None:
        jsonschema.validate(obj, schema)
    return obj


def _extract_json(text: str) -> dict:
    """Pull the first JSON object out of a model response (handles ``` fences)."""
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    candidate = fenced.group(1) if fenced else None
    if candidate is None:
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            candidate = text[start:end + 1]
    if candidate is None:
        raise SchemaError("no JSON object found in model output")
    return json.loads(candidate)


class LLMProvider:
    """Interface. Subclasses implement ``complete``; ``structured`` builds on it."""

    name = "base"

    def complete(self, prompt: str, system: str | None = None) -> str:
        raise NotImplementedError

    def structured(self, prompt: str, schema: dict, system: str | None = None) -> dict:
        instruction = (f"{prompt}\n\nReturn ONLY a JSON object matching this schema "
                       f"(no prose, no code fence):\n{json.dumps(schema)}")
        last_err = None
        for _ in range(2):
            raw = self.complete(instruction, system=system)
            try:
                return validate_output(_extract_json(raw), schema)
            except Exception as e:  # noqa: BLE001 - retry once, then surface
                last_err = e
        raise SchemaError(f"{self.name} output failed schema validation: {last_err}")


class StubProvider(LLMProvider):
    """Deterministic, offline provider for tests and no-model environments."""

    name = "stub"

    def __init__(self, text: str | None = None, obj: dict | None = None):
        self._text = text
        self._obj = obj

    def complete(self, prompt: str, system: str | None = None) -> str:
        if self._text is not None:
            return self._text
        # Echo a compact, deterministic acknowledgement of the prompt.
        head = " ".join(prompt.split())[:160]
        return f"[stub] {head}"

    def structured(self, prompt: str, schema: dict, system: str | None = None) -> dict:
        if self._obj is not None:
            return validate_output(self._obj, schema)
        return validate_output(_default_for_schema(schema), schema)


def _default_for_schema(schema: dict) -> dict:
    """Build a minimal object satisfying an object schema's required fields,
    honouring ``const``/``enum``/``minimum`` so constrained schemas still validate."""
    out = {}
    props = schema.get("properties", {})
    for key in schema.get("required", list(props)):
        spec = props.get(key, {})
        if "const" in spec:
            out[key] = spec["const"]
        elif spec.get("enum"):
            out[key] = spec["enum"][0]
        elif spec.get("type") in ("number", "integer"):
            out[key] = spec.get("minimum", 0)
        else:
            out[key] = {"string": "", "boolean": False,
                        "array": [], "object": {}}.get(spec.get("type", "string"), None)
    return out


class ClaudeCLIProvider(LLMProvider):
    """Headless ``claude -p`` calls (subscription CLI; no API key needed)."""

    name = "claude-cli"

    def __init__(self, binary: str = "claude", timeout: int = 120):
        self.binary = shutil.which(binary) or binary
        self.timeout = timeout

    def complete(self, prompt: str, system: str | None = None) -> str:
        cmd = [self.binary, "-p", prompt]
        if system:
            cmd += ["--append-system-prompt", system]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)
        if proc.returncode != 0:
            raise RuntimeError(f"claude CLI exited {proc.returncode}: {proc.stderr[-500:]}")
        return proc.stdout.strip()


def _http_post_json(url: str, payload: dict, headers: dict, timeout: int) -> dict:
    """POST JSON and parse a JSON response (stdlib urllib). Raises RuntimeError on failure."""
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"Content-Type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        raise RuntimeError(f"HTTP {e.code} from {url}: {body[:400]}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"cannot reach {url}: {e.reason}")


class OllamaProvider(LLMProvider):
    """Local models via Ollama (http://localhost:11434). No API key, fully offline-capable.

    Env: OLLAMA_HOST (default http://localhost:11434), PAL_MODEL (default 'llama3.1')."""

    name = "ollama"

    def __init__(self, model: str | None = None, host: str | None = None, timeout: int = 180):
        self.host = (host or os.environ.get("OLLAMA_HOST") or "http://localhost:11434").rstrip("/")
        self.model = model or os.environ.get("PAL_MODEL") or "llama3.1"
        self.timeout = timeout

    def complete(self, prompt: str, system: str | None = None) -> str:
        messages = ([{"role": "system", "content": system}] if system else []) + \
                   [{"role": "user", "content": prompt}]
        out = _http_post_json(f"{self.host}/api/chat",
                              {"model": self.model, "messages": messages, "stream": False},
                              headers={}, timeout=self.timeout)
        return (out.get("message") or {}).get("content", "").strip()


class OpenAICompatibleProvider(LLMProvider):
    """Any OpenAI-compatible /chat/completions endpoint: OpenAI, vLLM, LM Studio, LocalAI,
    Together, Groq, etc. Env: OPENAI_BASE_URL (default https://api.openai.com/v1),
    OPENAI_API_KEY, PAL_MODEL (default 'gpt-4o-mini')."""

    name = "openai"

    def __init__(self, model: str | None = None, base_url: str | None = None,
                 api_key: str | None = None, timeout: int = 180):
        self.base_url = (base_url or os.environ.get("OPENAI_BASE_URL")
                         or "https://api.openai.com/v1").rstrip("/")
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.model = model or os.environ.get("PAL_MODEL") or "gpt-4o-mini"
        self.timeout = timeout

    def complete(self, prompt: str, system: str | None = None) -> str:
        messages = ([{"role": "system", "content": system}] if system else []) + \
                   [{"role": "user", "content": prompt}]
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        out = _http_post_json(f"{self.base_url}/chat/completions",
                              {"model": self.model, "messages": messages, "temperature": 0.3},
                              headers=headers, timeout=self.timeout)
        return out["choices"][0]["message"]["content"].strip()


# Registry so get_provider stays a simple lookup as providers grow.
_PROVIDERS = {
    "stub": StubProvider,
    "claude": ClaudeCLIProvider,
    "claude-cli": ClaudeCLIProvider,
    "ollama": OllamaProvider,
    "openai": OpenAICompatibleProvider,
    "openai-compatible": OpenAICompatibleProvider,
    "vllm": OpenAICompatibleProvider,
    "lmstudio": OpenAICompatibleProvider,
}


def get_provider(name: str | None = None) -> LLMProvider:
    """Resolve a provider: explicit ``name`` > $PAL_LLM > auto (claude if present, else stub).

    The learner's context (vault) is model-independent — switching the provider only
    changes who generates challenges/narratives, never the stored progress."""
    choice = (name or os.environ.get("PAL_LLM") or "").lower()
    if choice in _PROVIDERS:
        return _PROVIDERS[choice]()
    if choice:
        raise ValueError(f"unknown provider '{choice}'. Known: {', '.join(sorted(_PROVIDERS))}")
    if shutil.which("claude"):
        return ClaudeCLIProvider()
    return StubProvider()
