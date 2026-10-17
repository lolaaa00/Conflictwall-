#!/usr/bin/env python3
"""Deploy ConflictWall to stable Studionet after verifying chain ID 61999."""
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
RPC = "https://studio.genlayer.com/api"
CHAIN_ID = 61999
CONTRACT = ROOT / "contracts" / "conflictwall.py"


def verify_chain() -> None:
    req = urllib.request.Request(
        RPC,
        data=json.dumps({"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}).encode(),
        headers={"Content-Type":"application/json","User-Agent":"conflictwall-deploy/1.0"},
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        payload = json.load(response)
    actual = int(payload["result"], 16)
    if actual != CHAIN_ID:
        raise SystemExit(f"ERROR: RPC chain ID {actual}, expected {CHAIN_ID}")
    print(f"Verified stable Studionet chain ID: {actual}")


def main() -> int:
    subprocess.run([sys.executable, "scripts/preflight.py"], cwd=ROOT, check=True)
    verify_chain()
    local_cli = ROOT / "node_modules" / ".bin" / ("genlayer.cmd" if sys.platform.startswith("win") else "genlayer")
    cli = str(local_cli) if local_cli.exists() else shutil.which("genlayer")
    if cli is None:
        print("ERROR: install repo-local genlayer@0.39.1 with npm install", file=sys.stderr)
        return 2
    subprocess.run([cli, "account", "show"], cwd=ROOT, check=True)
    subprocess.run([cli, "deploy", "--contract", str(CONTRACT), "--rpc", RPC], cwd=ROOT, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
