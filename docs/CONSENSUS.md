# Consensus design

ConflictWall deliberately keeps nondeterminism narrow.

## What validators decide

For one frozen engagement, validators independently classify whether the current work is:

- `PROTECTED`
- `UNPROTECTED`
- `AMBIGUOUS`

The prompt contains only frozen policy scope, frozen protected-exposure criteria, the already-registered conflict domain/client profile and the exact engagement description.

The leader does not decide the conflict domain. The policy owner froze domain/client membership before sealing.

## What validators do not decide

The LLM never decides:

- allowed vs blocked;
- which client currently owns the actor's wall;
- whether a policy is sealed;
- consumer identity;
- permit consumption;
- whether two clients share a domain;
- whether an exposure can be cleared.

All of those are deterministic state.

## Equivalence boundary

The classification is state-relevant and must match exactly between leader and validator.

The natural-language `reason` is diagnostic only and is intentionally not compared. Different wording cannot change shared state.

Malformed output is represented as `parse_ok = False`; deterministic execution then records `INCONCLUSIVE` and does not create an exposure.

## Why the wall locks at resolution

A tempting design is to wait until a downstream consumer calls `consume()` before creating exposure. That permits a race:

```text
Alpha protected permit → ALLOWED
Beta protected permit  → ALLOWED
(first permit not consumed yet)
```

ConflictWall avoids this. For protected engagements, resolving `ALLOWED` atomically creates or confirms the actor's domain exposure. Therefore the second competing resolution observes the wall and is blocked.
