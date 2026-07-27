"""Deterministic Code Execution sandbox (F4.1).

Run a learner's code in isolation and return a pass/fail verdict from the process
exit code, plus stdout/stderr and elapsed time (a coarse benchmark). Prefers a
locked-down Docker container (``--network none``, memory-capped); falls back to an
isolated subprocess when Docker is unavailable or ``use_docker=False`` (used in
tests so no image pull is needed).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, field

_EXT = {"python": "main.py", "go": "main.go"}
_DEFAULT_IMAGE = {"python": "python:3.11-slim", "go": "golang:1.22"}


@dataclass
class Verdict:
    passed: bool
    exit_code: int
    engine: str
    elapsed_ms: float
    stdout: str = ""
    stderr: str = ""
    error: str = field(default="")

    def to_dict(self) -> dict:
        d = self.__dict__.copy()
        if not d["error"]:
            d.pop("error")
        return d


def docker_available() -> bool:
    return bool(shutil.which("docker"))


def _local_cmd(language: str, filename: str, race: bool) -> list[str]:
    if language == "python":
        return ["python3", filename]
    if language == "go":
        return ["go", "run"] + (["-race"] if race else []) + [filename]
    raise ValueError(f"unsupported language: {language}")


def run_code(code: str, language: str = "python", *, use_docker: bool = True,
             image: str | None = None, timeout: int = 30, memory: str = "256m",
             race: bool = False) -> Verdict:
    if language not in _EXT:
        return Verdict(False, -1, "none", 0.0, error=f"unsupported language: {language}")
    use_docker = use_docker and docker_available()
    engine = "docker" if use_docker else "subprocess"
    img = image or _DEFAULT_IMAGE[language]

    cwd = tempfile.mkdtemp(prefix="pal_sandbox_")
    try:
        fname = _EXT[language]
        with open(os.path.join(cwd, fname), "w", encoding="utf-8", newline="\n") as f:
            f.write(code)
        if use_docker:
            cmd = ["docker", "run", "--rm", "--network", "none", f"--memory={memory}",
                   "-v", f"{cwd}:/app", "-w", "/app", img]
            cmd += (["python", fname] if language == "python"
                    else ["sh", "-c", "go run " + ("-race " if race else "") + fname])
        else:
            cmd = _local_cmd(language, os.path.join(cwd, fname), race)

        start = time.perf_counter()
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return Verdict(False, -1, engine, timeout * 1000.0, error="timeout")
        except OSError as e:
            return Verdict(False, -1, engine, 0.0, error=f"failed to run: {e}")
        elapsed = (time.perf_counter() - start) * 1000
        return Verdict(proc.returncode == 0, proc.returncode, engine, round(elapsed, 2),
                       stdout=proc.stdout[-4000:], stderr=proc.stderr[-4000:])
    finally:
        shutil.rmtree(cwd, ignore_errors=True)
