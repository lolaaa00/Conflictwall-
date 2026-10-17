# Canonical stable-Studionet evidence

All addresses and transaction hashes below are from stable GenLayer Studionet,
chain `61999`, RPC `https://studio.genlayer.com/api`. The integration harness
waited for `TransactionStatus.FINALIZED` and asserted execution success or
expected execution failure for every recorded transaction.

## Canonical deployments

- ConflictWall: [`0xbB7a6EED169F6F13A6CcAFf0B72b4dCDb5513ca5`](https://explorer-studio.genlayer.com/address/0xbB7a6EED169F6F13A6CcAFf0B72b4dCDb5513ca5)
- ConflictWall deployment: [`0x5f84d5752748bde4d1d2672d8a44bde59cfc232afa613e89f172db28ac8e1348`](https://explorer-studio.genlayer.com/tx/0x5f84d5752748bde4d1d2672d8a44bde59cfc232afa613e89f172db28ac8e1348)
- ProtectedEngagementRegistry: [`0x3920e63E2b387DbBF5e12Dd38Ae56C7680002045`](https://explorer-studio.genlayer.com/address/0x3920e63E2b387DbBF5e12Dd38Ae56C7680002045)
- Registry deployment: [`0xe04657e36e0b11853ee7f8cc2e1e43c11284af0c77d576b5e4a01cea32ee163a`](https://explorer-studio.genlayer.com/tx/0xe04657e36e0b11853ee7f8cc2e1e43c11284af0c77d576b5e4a01cea32ee163a)
- Actor A: `0xBf1512Be473bA180eD08E1A8D2Ad97584F4c669a`
- Actor B: `0xA5117FF734026402707E903BF664FEa2048aeC5f`
- source commit at deployment: `10276739337f9fee10dab1a87cda93245a786688`

## Finalized canonical lifecycle

| Proof step | Expected result | Finalized transaction |
|---|---|---|
| Create policy | success | [`0x324aa8a18a8f1010d5b850e02d33364d46ea2dfaa9ced312dcb8bfd872d792ae`](https://explorer-studio.genlayer.com/tx/0x324aa8a18a8f1010d5b850e02d33364d46ea2dfaa9ced312dcb8bfd872d792ae) |
| Add Banking domain | success | [`0xa14344d5ef6f700b40237b35bb022b87242e2bd420ef32d75d6ae4eba2b22310`](https://explorer-studio.genlayer.com/tx/0xa14344d5ef6f700b40237b35bb022b87242e2bd420ef32d75d6ae4eba2b22310) |
| Add Airlines domain | success | [`0x13f28a0e72863e6cfd17f94e5083b6a1a3df18fc8e169cfe5797fc9124b4cf7b`](https://explorer-studio.genlayer.com/tx/0x13f28a0e72863e6cfd17f94e5083b6a1a3df18fc8e169cfe5797fc9124b4cf7b) |
| Register Alpha | success | [`0x04d9fc0ceed63d0b75b27fb07a42bce57ffbf54d6e2d9bffedbbeca7ca4b29ef`](https://explorer-studio.genlayer.com/tx/0x04d9fc0ceed63d0b75b27fb07a42bce57ffbf54d6e2d9bffedbbeca7ca4b29ef) |
| Register Beta | success | [`0x5bef749f1b5ce7b6fbcbd90975b2505d372c55d3d75ea239d6240b03b1b0800a`](https://explorer-studio.genlayer.com/tx/0x5bef749f1b5ce7b6fbcbd90975b2505d372c55d3d75ea239d6240b03b1b0800a) |
| Register Aero | success | [`0xa00ad9186f8615eaf9be6756dba99bfb9d2b0119b1f9cac0d6417f8b17c807d1`](https://explorer-studio.genlayer.com/tx/0xa00ad9186f8615eaf9be6756dba99bfb9d2b0119b1f9cac0d6417f8b17c807d1) |
| Register Fly | success | [`0x5aab6a6eb82d49396fed8ac71c05062e6302dbcf2cf7a65322570fe7f28eb2c5`](https://explorer-studio.genlayer.com/tx/0x5aab6a6eb82d49396fed8ac71c05062e6302dbcf2cf7a65322570fe7f28eb2c5) |
| Seal policy | success | [`0x8ae6fe569cf1d93340c9d2c80b9f0a592616927deae5ab5dec13c70e26aa8178`](https://explorer-studio.genlayer.com/tx/0x8ae6fe569cf1d93340c9d2c80b9f0a592616927deae5ab5dec13c70e26aa8178) |
| Propose Alpha protected work | success | [`0xdba169d3e63ccea5773548853dd99a0332db033ae3cc4b4fc2fe1dbec9fa6172`](https://explorer-studio.genlayer.com/tx/0xdba169d3e63ccea5773548853dd99a0332db033ae3cc4b4fc2fe1dbec9fa6172) |
| Resolve Alpha | `PROTECTED`, `ALLOWED`; lock exposure | [`0x1140f38892d7e9e16249e7ddb695fc282858604101824719feeb97020375b9e2`](https://explorer-studio.genlayer.com/tx/0x1140f38892d7e9e16249e7ddb695fc282858604101824719feeb97020375b9e2) |
| Direct wrong consumer | expected failure | [`0x1fe700d4e7e218426193ee1d1740a91ba3ce319b589b8ef0c5f97f3df6347d10`](https://explorer-studio.genlayer.com/tx/0x1fe700d4e7e218426193ee1d1740a91ba3ce319b589b8ef0c5f97f3df6347d10) |
| Wrong actor binding | expected failure | [`0xebb66304edc4a89d7696037cc7905ea28b5838a9a715693f798ebf415039503e`](https://explorer-studio.genlayer.com/tx/0xebb66304edc4a89d7696037cc7905ea28b5838a9a715693f798ebf415039503e) |
| Wrong reference binding | expected failure | [`0xbd13ffc12d5a0ac5ca6fe91dc838c33994e05ea73daa2fb06462dc96a72dd85e`](https://explorer-studio.genlayer.com/tx/0xbd13ffc12d5a0ac5ca6fe91dc838c33994e05ea73daa2fb06462dc96a72dd85e) |
| Wrong policy binding | expected failure | [`0x54bb68e08fe1d82f727e8b42f2feab3c68b049ea5fb3219d9c512276c59cbdef`](https://explorer-studio.genlayer.com/tx/0x54bb68e08fe1d82f727e8b42f2feab3c68b049ea5fb3219d9c512276c59cbdef) |
| Legitimate Alpha consumer | success; `CONSUMED` | [`0x17fbb46a88b58f2f3576ceafcc68d68b1756e80ecfa5840fba16586b5e13a5d1`](https://explorer-studio.genlayer.com/tx/0x17fbb46a88b58f2f3576ceafcc68d68b1756e80ecfa5840fba16586b5e13a5d1) |
| Replay Alpha permit | expected failure | [`0x0c085e3b1ea279f204fc3514988af9d3ad8ad142cb9929a7a928e476d097970d`](https://explorer-studio.genlayer.com/tx/0x0c085e3b1ea279f204fc3514988af9d3ad8ad142cb9929a7a928e476d097970d) |
| Propose Beta protected work | success | [`0x4dbe393ac2dfa67126a262650c2b8dff3af5f404f80c714a9841bf0edbb8992f`](https://explorer-studio.genlayer.com/tx/0x4dbe393ac2dfa67126a262650c2b8dff3af5f404f80c714a9841bf0edbb8992f) |
| Resolve Beta protected work | `PROTECTED`, `BLOCKED` | [`0x87188fc596893d919c2b63496cea7d156078c48c84431eacc6affc52a19d5a05`](https://explorer-studio.genlayer.com/tx/0x87188fc596893d919c2b63496cea7d156078c48c84431eacc6affc52a19d5a05) |
| Consume blocked Beta permit | expected failure | [`0xde8155ad73ea52b17373c80862a89b6c310288481a0491465834ffc8dba409a2`](https://explorer-studio.genlayer.com/tx/0xde8155ad73ea52b17373c80862a89b6c310288481a0491465834ffc8dba409a2) |
| Propose public Beta work | success | [`0x38bcbd3ee3c0df12197572a2467dc29af0434b663b352fe77f89ef3084483294`](https://explorer-studio.genlayer.com/tx/0x38bcbd3ee3c0df12197572a2467dc29af0434b663b352fe77f89ef3084483294) |
| Resolve public Beta work | `UNPROTECTED`, `ALLOWED`; wall unchanged | [`0x0816f7a702c1eb4f0ed697f1d915861245ebe2577aeee960be5f6f4fd4fb879c`](https://explorer-studio.genlayer.com/tx/0x0816f7a702c1eb4f0ed697f1d915861245ebe2577aeee960be5f6f4fd4fb879c) |
| Propose Aero protected work | success | [`0x4071ed1274d5b8915d6070ce88daf3a3b3e0857db77e2fae80293ab7e81f0482`](https://explorer-studio.genlayer.com/tx/0x4071ed1274d5b8915d6070ce88daf3a3b3e0857db77e2fae80293ab7e81f0482) |
| Resolve Aero protected work | `PROTECTED`, `ALLOWED`; independent domain | [`0xbbfce49196266287e39f5f616b2744d4aee30b5e48200299e7e7f3afca59ea49`](https://explorer-studio.genlayer.com/tx/0xbbfce49196266287e39f5f616b2744d4aee30b5e48200299e7e7f3afca59ea49) |
| Propose underspecified Beta work | success | [`0x0017f584d8cc6e9a900a5a64e196a4298dd1881bc4be88e3b596f92a38a04fc4`](https://explorer-studio.genlayer.com/tx/0x0017f584d8cc6e9a900a5a64e196a4298dd1881bc4be88e3b596f92a38a04fc4) |
| Resolve underspecified Beta work | `AMBIGUOUS`, `INCONCLUSIVE` | [`0x1a5a7c9b253b7114f592eec19e0274140b92ae36dd23d8f38e640e0207f0035f`](https://explorer-studio.genlayer.com/tx/0x1a5a7c9b253b7114f592eec19e0274140b92ae36dd23d8f38e640e0207f0035f) |
| Consume inconclusive permit | expected failure | [`0x45143b4d3eadecfece93d9b8587897a35fdadf7f48022bbe2f9c3d21071048a2`](https://explorer-studio.genlayer.com/tx/0x45143b4d3eadecfece93d9b8587897a35fdadf7f48022bbe2f9c3d21071048a2) |
| Actor B proposes protected Beta work | success | [`0xc770bcce0727e74677bdf90d720404b0a03023f5028da59935f79215e5962f84`](https://explorer-studio.genlayer.com/tx/0xc770bcce0727e74677bdf90d720404b0a03023f5028da59935f79215e5962f84) |
| Resolve Actor B's Beta work | `PROTECTED`, `ALLOWED`; independent actor | [`0xb778dc0681dd117756844c8124894e67d02679bf0bb39a4bb270658c0266836b`](https://explorer-studio.genlayer.com/tx/0xb778dc0681dd117756844c8124894e67d02679bf0bb39a4bb270658c0266836b) |

## Source parity

After the lifecycle completed, both deployed sources were retrieved directly
from the stable RPC with the official `gen_getContractCode` method, base64
decoded, and compared byte-for-byte with the local contract files:

| Contract | Bytes | Deployed and local SHA-256 | Exact bytes |
|---|---:|---|---|
| `contracts/conflictwall.py` | 32433 | `04e487f9a220962d7a721d481f879727376f82a6a6b0567412998002500909bd` | yes |
| `contracts/protected_engagement_registry.py` | 3858 | `ec0d94faacd9732cdcdc8bb97a330cd244d3a80289ab5c889a29220550f83949` | yes |

The deployment source commit precedes evidence-only test-harness and
documentation changes. The contract files were not modified afterward; the
recorded digest and direct RPC byte comparison establish parity.
