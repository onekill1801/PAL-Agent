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


def get_provider(name: str | None = None) -> LLMProvider:
    """Resolve a provider: explicit ``name`` > $PAL_LLM > auto (claude if present)."""
    choice = (name or os.environ.get("PAL_LLM") or "").lower()
    if choice == "stub":
        return StubProvider()
    if choice in ("claude", "claude-cli"):
        return ClaudeCLIProvider()
    if shutil.which("claude"):
        return ClaudeCLIProvider()
    return StubProvider()
