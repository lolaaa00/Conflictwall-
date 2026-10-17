# ConflictWall submission draft

## Contribution type

Standalone Intelligent Contract.

## Submission notes draft

ConflictWall is a history-dependent conflict-of-interest firewall implementing a semantic Brewer-Nash / Chinese-Wall model for autonomous agents. A policy owner freezes conflict domains and registered clients, then seals the version. For each proposed engagement, GenLayer validators independently classify only whether that exact work creates protected client exposure (`PROTECTED`, `UNPROTECTED`, or `AMBIGUOUS`). The model never decides access. Deterministic contract state owns the wall: once an actor receives protected access for one client inside a domain, later protected work for another client in that same domain is blocked, while same-client work, unprotected public work, and protected work in independent domains can remain available. Protected access locks at resolution rather than consumption, preventing competing-permit races. A tiny consumer IC demonstrates exact policy/actor/reference/consumer binding plus one-time finalized acknowledgement. No frontend is included.

## Evidence to insert after final deployment

- Repository: `https://github.com/lolaaa00/conflictwall`
- Stable Studionet chain: `61999`
- Core address: `TBD`
- Consumer address: `TBD`
- Deployment/finality evidence: `TBD`
- Direct Mode result: `TBD`
- GenVM lint result: `TBD`
- Live lifecycle evidence: `TBD`
- final commit/source-parity evidence: `TBD`
