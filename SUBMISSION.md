# ConflictWall submission

## Contribution type

Standalone Intelligent Contract.

## Submission notes

ConflictWall is a history-dependent conflict-of-interest firewall implementing a semantic Brewer-Nash / Chinese-Wall model for autonomous agents. A policy owner freezes conflict domains and registered clients, then seals the version. For each proposed engagement, GenLayer validators independently classify only whether that exact work creates protected client exposure (`PROTECTED`, `UNPROTECTED`, or `AMBIGUOUS`). The model never decides access. Deterministic contract state owns the wall: once an actor receives protected access for one client inside a domain, later protected work for another client in that same domain is blocked, while same-client work, unprotected public work, and protected work in independent domains can remain available. Protected access locks at resolution rather than consumption, preventing competing-permit races. A tiny consumer IC demonstrates exact policy/actor/reference/consumer binding plus one-time finalized acknowledgement. No frontend is included.

## Evidence

- Repository: `https://github.com/lolaaa00/conflictwall`
- Stable Studionet chain: `61999`
- Core address: [`0xbB7a6EED169F6F13A6CcAFf0B72b4dCDb5513ca5`](https://explorer-studio.genlayer.com/address/0xbB7a6EED169F6F13A6CcAFf0B72b4dCDb5513ca5)
- Consumer address: [`0x3920e63E2b387DbBF5e12Dd38Ae56C7680002045`](https://explorer-studio.genlayer.com/address/0x3920e63E2b387DbBF5e12Dd38Ae56C7680002045)
- Deployment/finality evidence: both deployment receipts reached `FINALIZED`; hashes are recorded in `docs/DEPLOYMENT.md`.
- Direct Mode result: **44 passed**.
- GenVM lint result: **PASS**, 3 checks/16 methods for ConflictWall and 3 checks/3 methods for ProtectedEngagementRegistry.
- Live lifecycle evidence: **1 passed in 1426.66s**, with 28 finalized lifecycle/adversarial transactions recorded in `docs/DEPLOYMENT.md`.
- Deployment source commit: `10276739337f9fee10dab1a87cda93245a786688`.
- Source parity: `gen_getContractCode` returned byte-for-byte matches for both local files; SHA-256 digests are recorded in `docs/DEPLOYMENT.md`.

Repository publication and the GitHub Actions result remain pending until the
owner creates `lolaaa00/conflictwall` and pushes this finished local history.
