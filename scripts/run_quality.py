#!/usr/bin/env python3
from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager

ROOT = pathlib.Path(__file__).resolve().parents[1]
STABLE_GENVM_VERSION = "v0.2.16"


def run(cmd: list[str], env: dict[str, str] | None = None) -> None:
    print("+", " ".join(cmd), flush=True)
    rc = subprocess.run(cmd, cwd=ROOT, check=False, env=env).returncode
    if rc != 0:
        raise SystemExit(rc)


@contextmanager
def stable_genvm_environment() -> Iterator[dict[str, str]]:
    if os.environ.get("GENVMROOT"):
        yield os.environ.copy()
        return
    from genvm_linter.validate.artifacts import download_artifacts
    from genvm_linter.validate.sdk_loader import extract_sdk_paths, parse_contract_header
    tarball = download_artifacts(STABLE_GENVM_VERSION)
    sdk_paths, _ = extract_sdk_paths(tarball, parse_contract_header(ROOT / "contracts" / "conflictwall.py"))
    if not sdk_paths:
        raise SystemExit("ERROR: stable GenVM SDK extraction produced no paths")
    with tempfile.TemporaryDirectory(prefix="conflictwall-genvm-") as tmp:
        genvmroot = pathlib.Path(tmp)
        sdk_link = genvmroot / "runners" / "genlayer-py-std" / "src"
        sdk_link.parent.mkdir(parents=True)
        sdk_link.symlink_to(sdk_paths[0], target_is_directory=True)
        env = os.environ.copy()
        env["GENVMROOT"] = str(genvmroot)
        yield env


def main() -> int:
    run([sys.executable, "scripts/preflight.py"])
    run([sys.executable, "-m", "compileall", "-q", "contracts", "scripts", "tests"])
    if not shutil.which("pytest"):
        raise SystemExit("ERROR: install requirements-test.txt")
    run([sys.executable, "-m", "pytest", "tests/direct", "-v", "-s"])
    linter = shutil.which("genvm-lint")
    if linter is None:
        adjacent_linter = pathlib.Path(sys.executable).with_name("genvm-lint")
        if adjacent_linter.is_file():
            linter = str(adjacent_linter)
    if linter is None:
        raise SystemExit("ERROR: install requirements.txt")
    with stable_genvm_environment() as env:
        run([linter, "check", "contracts/conflictwall.py"], env=env)
        run([linter, "check", "contracts/protected_engagement_registry.py"], env=env)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
