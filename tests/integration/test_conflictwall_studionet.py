"""High-signal stable Studionet lifecycle for ConflictWall.

This integration test intentionally targets stable Studionet only. It deploys a
fresh ConflictWall and tiny ProtectedEngagementRegistry consumer, establishes a
protected Alpha Bank exposure, proves competing Beta Bank protected work is
blocked, and proves public Beta work plus protected work in another domain remain
available.
"""

from gltest import get_contract_factory, get_default_account
from gltest.assertions import tx_execution_failed, tx_execution_succeeded
import time

WALL = "conflictwall.py"
REGISTRY = "protected_engagement_registry.py"
TX_KW = {"consensus_max_rotations": 3, "wait_interval": 10000, "wait_retries": 25}


def ok(receipt):
    assert tx_execution_succeeded(receipt), receipt


def test_conflictwall_history_dependent_gate():
    account = get_default_account()
    wall_factory = get_contract_factory(contract_file_path=WALL)
    wall = wall_factory.deploy(account=account, **TX_KW)
    assert wall.address
    registry_factory = get_contract_factory(contract_file_path=REGISTRY)
    registry = registry_factory.deploy(args=[wall.address], account=account, **TX_KW)
    assert registry.address

    p = wall.create_policy(args=[
        "professional-conflict-wall",
        "Prevent an autonomous professional that has obtained protected client-specific information from accepting protected work for a competing client in the same frozen conflict domain.",
        "Protected exposure includes client-confidential, non-public, strategic, security, financial, customer, operational, fiduciary or privileged work. Public generic work without material client-specific exposure is unprotected.",
    ]).transact(**TX_KW)
    ok(p)
    ok(wall.add_domain(args=[1, "commercial-banking", "Retail and corporate banks competing for deposits, lending, payments, treasury and related commercial banking business."]).transact(**TX_KW))
    ok(wall.add_domain(args=[1, "airlines", "Commercial passenger airlines competing for routes, pricing, fleet utilisation, loyalty and passenger demand."]).transact(**TX_KW))
    ok(wall.add_client(args=[1, 1, "alpha-bank", "Alpha Bank", "A commercial bank offering retail and corporate banking services."]).transact(**TX_KW))
    ok(wall.add_client(args=[1, 1, "beta-bank", "Beta Bank", "A competing commercial bank offering retail and corporate banking services."]).transact(**TX_KW))
    ok(wall.add_client(args=[1, 2, "aero-one", "Aero One", "A commercial passenger airline serving domestic and regional routes."]).transact(**TX_KW))
    ok(wall.add_client(args=[1, 2, "fly-fast", "Fly Fast", "A competing commercial passenger airline serving domestic and regional routes."]).transact(**TX_KW))
    ok(wall.seal_policy(args=[1]).transact(**TX_KW))

    ok(wall.propose_engagement(args=[1, 1, "alpha-private", "Review Alpha Bank's confidential pricing strategy, internal risk appetite and non-public customer acquisition plan.", registry.address]).transact(**TX_KW))
    ok(wall.resolve_engagement(args=[1]).transact(**TX_KW))
    alpha = wall.get_engagement(args=[1]).call()
    assert alpha["status_name"] == "ALLOWED"
    assert alpha["classification_name"] == "PROTECTED"

    actor = alpha["actor"]
    ok(registry.accept(args=[1, 1, actor, "alpha-private"]).transact(**TX_KW))
    for _ in range(12):
        if wall.get_engagement(args=[1]).call()["status_name"] == "CONSUMED":
            break
        time.sleep(5)
    assert wall.get_engagement(args=[1]).call()["status_name"] == "CONSUMED"

    ok(wall.propose_engagement(args=[1, 2, "beta-private", "Advise Beta Bank using its non-public pricing strategy, risk data and confidential customer plans.", registry.address]).transact(**TX_KW))
    ok(wall.resolve_engagement(args=[2]).transact(**TX_KW))
    assert wall.get_engagement(args=[2]).call()["status_name"] == "BLOCKED"
    denied = registry.accept(args=[2, 1, actor, "beta-private"]).transact(**TX_KW)
    assert tx_execution_failed(denied), denied

    ok(wall.propose_engagement(args=[1, 2, "beta-public", "Copyedit Beta Bank's already-public annual report into a public brochure using only public material and no client-confidential information.", registry.address]).transact(**TX_KW))
    ok(wall.resolve_engagement(args=[3]).transact(**TX_KW))
    public_item = wall.get_engagement(args=[3]).call()
    assert public_item["status_name"] == "ALLOWED"
    assert public_item["classification_name"] == "UNPROTECTED"

    ok(wall.propose_engagement(args=[1, 3, "aero-private", "Review Aero One's confidential route profitability, fleet plan and non-public pricing strategy.", registry.address]).transact(**TX_KW))
    ok(wall.resolve_engagement(args=[4]).transact(**TX_KW))
    aero = wall.get_engagement(args=[4]).call()
    assert aero["status_name"] == "ALLOWED"
    assert aero["classification_name"] == "PROTECTED"
