# ConflictWall

**A history-dependent conflict-of-interest firewall for autonomous agents and professional workflows.**

ConflictWall implements a semantic form of the **Brewer-Nash / Chinese Wall** security model on GenLayer.

The key property is simple:

> A future engagement can become forbidden because of a legitimate protected engagement the actor already accepted, even though both engagements would be valid in isolation.

```text
Frozen conflict domain: COMMERCIAL BANKING

Actor has no banking exposure
        │
        ├── protected Alpha Bank work → ALLOWED
        │                               wall locks to Alpha
        │
        ├── more protected Alpha work → ALLOWED
        │
        ├── protected Beta Bank work  → BLOCKED
        │
        └── public-only Beta brochure → ALLOWED (no protected exposure)

AIRLINES remains independent and open.
```

## Why GenLayer is necessary

The wall mechanics are deterministic. The hard boundary is semantic: whether the **current engagement** actually creates material protected client exposure under a frozen policy.

The Intelligent Contract therefore gives the model only one bounded job:

```text
PROTECTED | UNPROTECTED | AMBIGUOUS
```

The model never chooses `ALLOWED` or `BLOCKED`. Validators independently reproduce the classification and must agree exactly on the state-relevant class. Deterministic contract code then applies the actor's existing wall history.

## Core invariants

1. **Frozen policy version.** Domains and clients are immutable after `seal_policy`.
2. **Monotonic wall.** Once protected exposure locks an actor to a client inside a conflict domain, there is no LLM-controlled clear/declassification path.
3. **No permit race.** Resolving a protected engagement as allowed is itself the exposure event; the wall locks before a downstream consumer can use the permit.
4. **Same-client continuity.** More protected work for the already-selected client remains allowed.
5. **Competitor block.** Protected work for another client in the same domain is blocked.
6. **Independent domains.** Exposure in banking does not automatically block airlines.
7. **Public work does not contaminate.** A clearly unprotected/public engagement does not create or change exposure.
8. **Ambiguity fails closed.** Ambiguous or malformed semantic output is `INCONCLUSIVE`, never silently allowed as protected work.
9. **Exact consumer binding.** Permits bind policy, actor, engagement reference and consumer contract.
10. **One-time consumption.** A downstream contract can acknowledge a permit once.

## Repository boundary

This is a **standalone Intelligent Contract submission**. It intentionally has **no frontend**, no Next.js application, no backend authority and no product dashboard.

`ProtectedEngagementRegistry` is a tiny second IC used only to prove that another contract can gate a real state transition on a ConflictWall permit.

## Target network

Stable GenLayer Studionet only:

- Chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- Explorer: `https://explorer-studio.genlayer.com`
- repository-local CLI target: `genlayer@0.39.1`

## Layout

```text
contracts/conflictwall.py
contracts/protected_engagement_registry.py
tests/direct/test_conflictwall.py
tests/integration/test_conflictwall_studionet.py
scripts/preflight.py
scripts/run_quality.py
scripts/deploy_studionet.py
scripts/deploy_consumer_studionet.py
docs/CONSENSUS.md
docs/SECURITY.md
docs/INVARIANTS.md
docs/DEPLOYMENT.md
SUBMISSION.md
HANDOFF_TO_LOLA.md
CODEX_FINISH_PROMPT.md
```

## Local verification

```bash
python scripts/preflight.py
pip install -r requirements-test.txt
pytest tests/direct/ -v -s
```

Full local gate:

```bash
pip install -r requirements.txt
python scripts/run_quality.py
```

## Canonical live proof

A finalized Studionet lifecycle on the canonical deployment proves all of these:

1. create and seal a policy with Banking and Airlines conflict domains;
2. Alpha Bank protected engagement resolves `ALLOWED` and locks the actor's Banking wall to Alpha;
3. the tiny consumer accepts the Alpha permit;
4. Beta Bank protected engagement resolves `BLOCKED`;
5. the consumer rejects the blocked Beta engagement;
6. Beta public-only work resolves `ALLOWED` without moving the wall;
7. Aero One protected work resolves `ALLOWED` because Airlines is a separate conflict domain.

It additionally proves exact actor/reference/policy/consumer binding, one-time
consumption, fail-closed ambiguous work, and Actor B's independent wall. See
[`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for addresses, explorer links,
finalized transaction hashes, and deployed-source parity.

## Verification status

The local quality gate passes 44 Direct Mode tests and both GenVM contract
lints. The canonical stable-Studionet integration passes with every recorded
transaction finalized. The final `main` branch is published at
[`lolaaa00/Conflictwall-`](https://github.com/lolaaa00/Conflictwall-), and its
[GitHub Actions quality gate](https://github.com/lolaaa00/Conflictwall-/actions/workflows/quality.yml)
is green.
