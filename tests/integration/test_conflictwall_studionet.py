"""High-signal stable Studionet lifecycle for ConflictWall.

This integration test intentionally targets stable Studionet only. It deploys a
fresh ConflictWall and tiny ProtectedEngagementRegistry consumer, establishes a
protected Alpha Bank exposure, proves competing Beta Bank protected work is
blocked, and proves public Beta work plus protected work in another domain remain
available.
"""

from gltest import get_contract_factory, get_default_account
from gltest.accounts import get_accounts
from gltest.assertions import tx_execution_failed, tx_execution_succeeded
from gltest.clients import get_gl_provider
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.request

from genlayer_py.exceptions import GenLayerError

WALL = "conflictwall.py"
REGISTRY = "protected_engagement_registry.py"
RPC = "https://studio.genlayer.com/api"
CHAIN_ID = 61999
TX_KW = {
    "consensus_max_rotations": 3,
    "wait_interval": 10000,
    "wait_retries": 40,
    "wait_transaction_status": TransactionStatus.FINALIZED,
}


def install_transient_rpc_retries():
    """Keep a temporary gateway response from stranding a signed transaction."""
    provider = get_gl_provider()
    original = provider.make_request

    def retried(method, params):
        for attempt in range(6):
            try:
                return original(method, params)
            except GenLayerError as exc:
                message = str(exc).lower()
                transient = any(
                    marker in message
                    for marker in (
                        "invalid json",
                        "bad gateway",
                        "gateway timeout",
                        "request to",
                        "temporarily unavailable",
                        "too many requests",
                    )
                )
                if not transient or attempt == 5:
                    raise
                time.sleep(2 ** attempt)

    provider.make_request = retried


def ok(receipt):
    assert tx_execution_succeeded(receipt), receipt
    assert receipt.get("status_name") == "FINALIZED", receipt


def failed(receipt):
    assert tx_execution_failed(receipt), receipt
    assert receipt.get("status_name") == "FINALIZED", receipt


def verify_chain():
    request = urllib.request.Request(
        RPC,
        data=json.dumps({"jsonrpc": "2.0", "method": "eth_chainId", "params": [], "id": 1}).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "conflictwall-integration/1.0"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.load(response)
    assert int(payload["result"], 16) == CHAIN_ID, payload


def deploy_finalized(factory, account, args=None):
    receipt = factory.deploy_contract_tx(args=args, account=account, **TX_KW)
    ok(receipt)
    address = extract_contract_address(receipt)
    return factory.build_contract(address, account=account), receipt


def test_conflictwall_history_dependent_gate():
    verify_chain()
    install_transient_rpc_retries()
    account = get_default_account()
    candidates = [candidate for candidate in get_accounts() if candidate.address.lower() != account.address.lower()]
    assert candidates, "a second configured account is required for actor-isolation proof"
    actor_b_account = candidates[0]
    wall_factory = get_contract_factory(contract_file_path=WALL)
    wall, wall_deploy = deploy_finalized(wall_factory, account)
    assert wall.address
    registry_factory = get_contract_factory(contract_file_path=REGISTRY)
    registry, registry_deploy = deploy_finalized(registry_factory, account, [wall.address])
    assert registry.address

    evidence = {
        "network": {"rpc": RPC, "chain_id": CHAIN_ID},
        "actors": {"actor_a": account.address, "actor_b": actor_b_account.address},
        "source": {
            "commit_at_deployment": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], text=True
            ).strip(),
            "conflictwall_sha256": hashlib.sha256(
                Path("contracts/conflictwall.py").read_bytes()
            ).hexdigest(),
            "registry_sha256": hashlib.sha256(
                Path("contracts/protected_engagement_registry.py").read_bytes()
            ).hexdigest(),
        },
        "deployments": {
            "conflictwall": {"address": wall.address, "tx": wall_deploy["hash"]},
            "registry": {"address": registry.address, "tx": registry_deploy["hash"]},
        },
        "lifecycle": {},
    }

    evidence_path = os.environ.get("CONFLICTWALL_EVIDENCE_FILE")

    def persist():
        if not evidence_path:
            return
        output = Path(evidence_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        temporary = output.with_suffix(output.suffix + ".tmp")
        temporary.write_text(
            json.dumps(evidence, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temporary.replace(output)

    persist()

    def record(name, receipt, expect_success=True):
        (ok if expect_success else failed)(receipt)
        evidence["lifecycle"][name] = receipt["hash"]
        persist()
        return receipt

    p = wall.create_policy(args=[
        "professional-conflict-wall",
        "Prevent an autonomous professional that has obtained protected client-specific information from accepting protected work for a competing client in the same frozen conflict domain.",
        "Protected exposure includes client-confidential, non-public, strategic, security, financial, customer, operational, fiduciary or privileged work. Public generic work without material client-specific exposure is unprotected.",
    ]).transact(**TX_KW)
    record("policy_creation", p)
    record("banking_domain", wall.add_domain(args=[1, "commercial-banking", "Retail and corporate banks competing for deposits, lending, payments, treasury and related commercial banking business."]).transact(**TX_KW))
    record("airlines_domain", wall.add_domain(args=[1, "airlines", "Commercial passenger airlines competing for routes, pricing, fleet utilisation, loyalty and passenger demand."]).transact(**TX_KW))
    record("alpha_registration", wall.add_client(args=[1, 1, "alpha-bank", "Alpha Bank", "A commercial bank offering retail and corporate banking services."]).transact(**TX_KW))
    record("beta_registration", wall.add_client(args=[1, 1, "beta-bank", "Beta Bank", "A competing commercial bank offering retail and corporate banking services."]).transact(**TX_KW))
    record("aero_registration", wall.add_client(args=[1, 2, "aero-one", "Aero One", "A commercial passenger airline serving domestic and regional routes."]).transact(**TX_KW))
    record("fly_registration", wall.add_client(args=[1, 2, "fly-fast", "Fly Fast", "A competing commercial passenger airline serving domestic and regional routes."]).transact(**TX_KW))
    record("policy_seal", wall.seal_policy(args=[1]).transact(**TX_KW))

    record("alpha_proposal", wall.propose_engagement(args=[1, 1, "alpha-private", "Review Alpha Bank's confidential pricing strategy, internal risk appetite and non-public customer acquisition plan.", registry.address]).transact(**TX_KW))
    record("alpha_protected_allowed", wall.resolve_engagement(args=[1]).transact(**TX_KW))
    alpha = wall.get_engagement(args=[1]).call()
    assert alpha["status_name"] == "ALLOWED"
    assert alpha["classification_name"] == "PROTECTED"

    actor = alpha["actor"]
    record("wrong_consumer_rejected", wall.consume(args=[1]).transact(**TX_KW), expect_success=False)
    record("wrong_actor_rejected", registry.accept(args=[1, 1, actor_b_account.address, "alpha-private"]).transact(**TX_KW), expect_success=False)
    record("wrong_reference_rejected", registry.accept(args=[1, 1, actor, "wrong-reference"]).transact(**TX_KW), expect_success=False)
    record("wrong_policy_rejected", registry.accept(args=[1, 2, actor, "alpha-private"]).transact(**TX_KW), expect_success=False)
    record("alpha_consumer_success", registry.accept(args=[1, 1, actor, "alpha-private"]).transact(**TX_KW))
    for _ in range(12):
        if wall.get_engagement(args=[1]).call()["status_name"] == "CONSUMED":
            break
        time.sleep(5)
    assert wall.get_engagement(args=[1]).call()["status_name"] == "CONSUMED"
    record("permit_replay_rejected", registry.accept(args=[1, 1, actor, "alpha-private"]).transact(**TX_KW), expect_success=False)

    record("beta_protected_proposal", wall.propose_engagement(args=[1, 2, "beta-private", "Advise Beta Bank using its non-public pricing strategy, risk data and confidential customer plans.", registry.address]).transact(**TX_KW))
    record("beta_protected_blocked", wall.resolve_engagement(args=[2]).transact(**TX_KW))
    assert wall.get_engagement(args=[2]).call()["status_name"] == "BLOCKED"
    record("beta_consumer_rejected", registry.accept(args=[2, 1, actor, "beta-private"]).transact(**TX_KW), expect_success=False)

    record("beta_public_proposal", wall.propose_engagement(args=[1, 2, "beta-public", "Copyedit Beta Bank's already-public annual report into a public brochure using only public material and no client-confidential information.", registry.address]).transact(**TX_KW))
    record("beta_unprotected_allowed", wall.resolve_engagement(args=[3]).transact(**TX_KW))
    public_item = wall.get_engagement(args=[3]).call()
    assert public_item["status_name"] == "ALLOWED"
    assert public_item["classification_name"] == "UNPROTECTED"
    assert wall.get_exposure(args=[1, actor, 1]).call()["client_id"] == 1

    record("aero_protected_proposal", wall.propose_engagement(args=[1, 3, "aero-private", "Review Aero One's confidential route profitability, fleet plan and non-public pricing strategy.", registry.address]).transact(**TX_KW))
    record("aero_protected_allowed", wall.resolve_engagement(args=[4]).transact(**TX_KW))
    aero = wall.get_engagement(args=[4]).call()
    assert aero["status_name"] == "ALLOWED"
    assert aero["classification_name"] == "PROTECTED"
    assert wall.get_exposure(args=[1, actor, 1]).call()["client_id"] == 1
    assert wall.get_exposure(args=[1, actor, 2]).call()["client_id"] == 3

    record("ambiguous_proposal", wall.propose_engagement(args=[1, 2, "beta-ambiguous", "Help Beta Bank with a project; the scope and information-access level are not specified.", registry.address]).transact(**TX_KW))
    record("fail_closed_inconclusive", wall.resolve_engagement(args=[5]).transact(**TX_KW))
    ambiguous = wall.get_engagement(args=[5]).call()
    assert ambiguous["status_name"] == "INCONCLUSIVE"
    assert ambiguous["classification_name"] == "AMBIGUOUS"
    assert wall.get_exposure(args=[1, actor, 1]).call()["client_id"] == 1
    record("inconclusive_consumer_rejected", registry.accept(args=[5, 1, actor, "beta-ambiguous"]).transact(**TX_KW), expect_success=False)

    wall_actor_b = wall_factory.build_contract(wall.address, account=actor_b_account)
    record("actor_b_beta_proposal", wall_actor_b.propose_engagement(args=[1, 2, "actor-b-beta", "Review Beta Bank's confidential pricing, risk and customer strategy materials.", registry.address]).transact(**TX_KW))
    record("actor_b_isolation", wall_actor_b.resolve_engagement(args=[6]).transact(**TX_KW))
    actor_b_item = wall.get_engagement(args=[6]).call()
    assert actor_b_item["actor"].lower() == actor_b_account.address.lower()
    assert actor_b_item["status_name"] == "ALLOWED"
    assert actor_b_item["classification_name"] == "PROTECTED"
    assert wall.get_exposure(args=[1, actor_b_account.address, 1]).call()["client_id"] == 2

    print("CONFLICTWALL_LIVE_EVIDENCE=" + json.dumps(evidence, sort_keys=True))
