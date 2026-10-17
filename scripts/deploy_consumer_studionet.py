#!/usr/bin/env python3
"""Deploy the tiny ConflictWall consumer to stable Studionet."""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
RPC = "https://studio.genlayer.com/api"
CHAIN_ID = 61999
CONTRACT = ROOT / "contracts" / "protected_engagement_registry.py"


def verify_chain() -> None:
    request = urllib.request.Request(
        RPC,
        data=json.dumps({"jsonrpc": "2.0", "method": "eth_chainId", "params": [], "id": 1}).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "conflictwall-deploy/1.0"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.load(response)
    actual = int(payload["result"], 16)
    if actual != CHAIN_ID:
        raise SystemExit(f"ERROR: RPC chain ID {actual}, expected {CHAIN_ID}")
    print(f"Verified stable Studionet chain ID: {actual}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python scripts/deploy_consumer_studionet.py <CONFLICTWALL_ADDRESS>")
        return 2
    address = sys.argv[1]
    subprocess.run([sys.executable, "scripts/preflight.py"], cwd=ROOT, check=True)
    verify_chain()
    local_cli = ROOT / "node_modules" / ".bin" / ("genlayer.cmd" if sys.platform.startswith("win") else "genlayer")
    if not local_cli.exists():
        print("ERROR: install repo-local genlayer@0.39.1 with npm install", file=sys.stderr)
        return 2
    cli = str(local_cli)
    subprocess.run([cli, "account", "show"], cwd=ROOT, check=True)
    subprocess.run([
        cli, "deploy", "--contract", str(CONTRACT), "--rpc", RPC, "--args", f'["{address}"]'
    ], cwd=ROOT, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
