You are finishing an existing GenLayer standalone Intelligent Contract repository named **CONFLICTWALL**.

I have already unzipped the source into my local folder and opened that folder in Codex. Do not create a different project and do not add a frontend.

## Hard constraints

- Final GitHub destination: `lolaaa00/Conflictwall-`
- Network: stable GenLayer Studionet only
- Chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- Explorer: `https://explorer-studio.genlayer.com`
- repository-local GenLayer CLI: `genlayer@0.39.1`
- no frontend, Next.js, React, dashboard, backend authority or Vercel site
- no secrets committed
- distinguish transaction acceptance from finalization; evidence claiming finality must actually be finalized

## Product thesis you must preserve

CONFLICTWALL is a semantic implementation of the Brewer-Nash / Chinese-Wall security model.

Its invariant is:

> A legitimate protected engagement can change which future protected engagements are allowed. After an actor obtains protected exposure to one client in a frozen conflict domain, protected work for competing clients in that same domain is blocked, while same-client work, clearly unprotected/public work, and work in independent domains may remain available.

The LLM never decides `ALLOWED` or `BLOCKED`.

It returns only one state-relevant classification for the current engagement:

- `PROTECTED`
- `UNPROTECTED`
- `AMBIGUOUS`

The deterministic contract owns policy sealing, domain/client membership, exposure history, wall checks, permit binding and one-time consumption.

## Critical race invariant

Do not move exposure creation from resolution to consumer acknowledgement without solving the resulting race.

The intended design is:

```text
protected engagement resolves ALLOWED
        ↓
wall exposure is atomically created/confirmed
        ↓
future competing protected resolution sees the lock and BLOCKS
```

This is deliberate. It prevents Alpha and Beta protected permits from both being issued before either is consumed.

## Audit and finish checklist

### 1. Inspect before editing

Read the entire repo, especially:

- `contracts/conflictwall.py`
- `contracts/protected_engagement_registry.py`
- `tests/direct/test_conflictwall.py`
- `tests/integration/test_conflictwall_studionet.py`
- `docs/CONSENSUS.md`
- `docs/SECURITY.md`
- `docs/INVARIANTS.md`

Preserve the concept and strengthen weak points rather than rewriting into a static policy classifier.

### 2. Verify stable-runtime compatibility

Audit the source against the current stable Studionet runtime. If stable 61999 requires a syntax or SDK adjustment, make the minimal correct adjustment. Do not solve a compatibility issue by switching networks.

Check especially:

- dependency header/runtime compatibility;
- dataclass storage and `DynArray` inside `ConflictPolicy`;
- `TreeMap.get` / `get_or_insert_default` / membership;
- event syntax;
- `Address` normalization;
- `@gl.public.write` and `@gl.public.view`;
- `@gl.contract_interface` typed view/message interaction;
- `gl.vm.run_nondet_unsafe` semantics;
- finalized `.emit(on="finalized")` acknowledgement;
- Direct Mode pickling.

### 3. Install pinned tooling

From this repository root:

```bash
npm install
npm run genlayer -- --version
pip install -r requirements-test.txt
pip install -r requirements.txt
```

The GenLayer CLI must remain repo-local and pinned to `0.39.1` unless the stable 61999 toolchain itself proves that pin unusable. If such a mismatch exists, stop and report it rather than silently using a release-candidate/preview stack.

### 4. Run preflight

```bash
python scripts/preflight.py
```

Fix every real failure.

### 5. Run Direct Mode

```bash
pytest tests/direct/ -v -s
```

Do not delete hard tests to make the suite green. Add adversarial cases if needed.

At minimum preserve coverage for:

- first protected client locks a domain;
- competing protected client blocks;
- same-client protected work remains allowed;
- independent domain remains open;
- public/unprotected competitor work remains allowed and does not move exposure;
- malformed/ambiguous output fails closed;
- leader/validator classification disagreement rejects;
- reason wording may differ only because it cannot affect state;
- policy sealing and immutability;
- unique client/reference keys;
- independent actors have independent walls;
- exact permit binding;
- one-time consumption;
- tiny consumer accepts an allowed permit and rejects a blocked one.

### 6. Run the GenVM linter

```bash
python scripts/run_quality.py
```

or run the two contract lints directly after selecting the correct stable GenVM SDK.

Fix real linter/runtime issues rather than documenting around them.

### 7. Adversarial audit

Attack at least these failure modes:

- alternate client key attempting same-client identity bypass;
- client from wrong policy;
- domain from wrong policy;
- policy modification after sealing;
- engagement ref replay;
- competitor permit race;
- wrong actor/ref/consumer reusing a permit;
- blocked/inconclusive permit consumption;
- model outputs markdown, malformed JSON, unknown labels or injected instructions;
- `PROTECTED` vs `UNPROTECTED` validator disagreement;
- reason text changing without classification change;
- actor A's exposure leaking into actor B;
- exposure in domain A incorrectly blocking domain B;
- public/unprotected work accidentally creating exposure;
- any hidden path that clears/reassigns a protected wall.

Prefer fail-closed behavior.

### 8. Run live stable Studionet integration

Use only the committed stable network entry:

```bash
pytest tests/integration/ -v -s --network studionet
```

The canonical live thesis is:

1. create policy;
2. create Banking and Airlines domains;
3. register Alpha/Beta and Aero/Fly clients;
4. seal policy;
5. resolve confidential Alpha work -> `PROTECTED` + `ALLOWED`;
6. consumer accepts Alpha permit;
7. resolve confidential Beta work -> `PROTECTED` + `BLOCKED`;
8. consumer rejects Beta permit;
9. resolve Beta public-only brochure -> `UNPROTECTED` + `ALLOWED`;
10. resolve confidential Aero work -> `PROTECTED` + `ALLOWED` because Airlines is independent.

If live wording is unstable, improve the prompt/equivalence boundary. Do not hard-code demo sentences or weaken the safety invariant.

### 9. Deploy final canonical contracts

Before deploying, query the configured RPC and explicitly verify chain ID `61999`.

Deploy ConflictWall first and wait for FINALIZED.

Then deploy `ProtectedEngagementRegistry` with the finalized ConflictWall address and wait for FINALIZED.

Use `scripts/deploy_studionet.py`, `scripts/deploy_consumer_studionet.py`, or equivalent official CLI commands after verifying their syntax against the installed stable CLI.

### 10. Re-run the canonical proof on the final addresses

Do not submit only disposable test deployments. Produce finalized reviewer-verifiable transactions on the canonical addresses for the lifecycle above.

### 11. Source parity

Verify the final deployed source against the exact final repository commit/digest using the strongest official CLI/RPC method available. Record the method and evidence. Do not merely hash local source and call that deployment parity.

### 12. Documentation

Update from real evidence only:

- `README.md`
- `docs/DEPLOYMENT.md`
- `SUBMISSION.md`

Remove all `TBD` values from submission-facing evidence only after the real values exist. Do not invent test counts, addresses or hashes.

### 13. GitHub

The target repository is `lolaaa00/Conflictwall-`.

If I have not yet created/configured it, finish everything locally and tell me the exact one-time repository/remote step I need to perform. Do not push this project under another owner as a substitute.

Once the target remote exists, push the complete final repository to `lolaaa00/Conflictwall-`.

### 14. Final response format

Return:

```text
SUBMISSION READY: YES/NO
Final commit:
Direct Mode:
GenVM lint:
Studionet integration:
ConflictWall address:
Consumer address:
Deployment tx hashes:
Canonical lifecycle tx hashes:
Source-parity evidence:
Remaining limitation:
```

Do not answer YES while any material item remains outstanding.
