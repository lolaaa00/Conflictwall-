#!/usr/bin/env python3
"""Deploy the tiny ConflictWall consumer to stable Studionet."""
from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
RPC = "https://studio.genlayer.com/api"
CONTRACT = ROOT / "contracts" / "protected_engagement_registry.py"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python scripts/deploy_consumer_studionet.py <CONFLICTWALL_ADDRESS>")
        return 2
    address = sys.argv[1]
    local_cli = ROOT / "node_modules" / ".bin" / ("genlayer.cmd" if sys.platform.startswith("win") else "genlayer")
    cli = str(local_cli) if local_cli.exists() else shutil.which("genlayer")
    if cli is None:
        print("ERROR: install repo-local genlayer@0.39.1 with npm install", file=sys.stderr)
        return 2
    subprocess.run([
        cli, "deploy", "--contract", str(CONTRACT), "--rpc", RPC, "--args", f'["{address}"]'
    ], cwd=ROOT, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
