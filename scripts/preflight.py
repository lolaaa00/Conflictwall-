#!/usr/bin/env python3
from __future__ import annotations

import ast
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CORE = ROOT / "contracts" / "conflictwall.py"
CONSUMER = ROOT / "contracts" / "protected_engagement_registry.py"
CONFIG = ROOT / "gltest.config.yaml"
DEPLOY = ROOT / "scripts" / "deploy_studionet.py"
IGNORED = {".git", ".venv", ".pytest_cache", "__pycache__", "artifacts", "node_modules"}
checks = 0


def ok(value: bool, message: str) -> None:
    global checks
    checks += 1
    if not value:
        raise AssertionError(message)


def text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    ok(CORE.is_file(), "missing core contract")
    ok(CONSUMER.is_file(), "missing consumer contract")
    ok(not (ROOT / "frontend").exists(), "standalone primitive must not have a frontend")
    for path in sorted(ROOT.rglob("*.py")):
        if any(part in IGNORED for part in path.relative_to(ROOT).parts):
            continue
        ast.parse(text(path), filename=str(path))
        ok(True, f"syntax {path.relative_to(ROOT)}")

    core = text(CORE)
    consumer = text(CONSUMER)
    config = text(CONFIG)
    required = [
        "class ConflictWall(gl.Contract)",
        "gl.vm.run_nondet_unsafe",
        "def validator_fn",
        "leader_class == own_class",
        "POLICY_SEALED",
        "CLASS_PROTECTED",
        "CLASS_UNPROTECTED",
        "CLASS_AMBIGUOUS",
        "def wall_state",
        "def is_permitted",
        "def consume",
        "ExposureLocked",
        "Resolving protected access is itself the exposure event",
    ]
    for needle in required:
        ok(needle in core, f"missing invariant: {needle}")
    ok("@gl.contract_interface" in consumer, "consumer must use typed contract interface")
    ok(".view().is_permitted" in consumer, "consumer must gate through ConflictWall view")
    ok('.emit(on="finalized").consume' in consumer, "consumer must acknowledge consumption after finalization")
    ok("https://studio.genlayer.com/api" in config, "stable Studionet RPC missing")
    ok("studionet:" in config, "Studionet test network missing")
    ok("61999" in text(DEPLOY), "deployment script must assert chain 61999")

    # The repository must never silently acquire a product UI.
    for candidate in ("frontend", "app", "web", "dashboard"):
        ok(not (ROOT / candidate).exists(), f"unexpected product directory: {candidate}")

    direct = text(ROOT / "tests" / "direct" / "test_conflictwall.py")
    ok(direct.count("def test_") >= 28, "expected at least 28 Direct Mode tests")
    for phrase in (
        "competing_beta_protected_engagement_is_blocked",
        "different_conflict_domain_remains_open",
        "public_competitor_work_is_allowed",
        "validator_rejects_state_relevant_classification_disagreement",
        "consumer_contract_rejects_blocked_permit",
    ):
        ok(phrase in direct, f"missing high-signal regression: {phrase}")

    readme = text(ROOT / "README.md")
    ok("no frontend" in readme.lower(), "README must state no-frontend boundary")
    ok("61999" in readme, "README must state stable chain")
    ok("Brewer" in readme and "Chinese Wall" in readme, "README must identify the underlying primitive")

    print(f"PASS: {checks} preflight checks")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
