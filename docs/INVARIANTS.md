# Protocol invariants

1. A sealed policy cannot add or modify domains or clients.
2. Every sealed conflict domain contains at least two registered clients.
3. An actor has at most one locked client per `(policy, conflict domain)`.
4. A protected allowed engagement creates/confirms that lock before returning.
5. A protected engagement for a different client in the same locked domain cannot become `ALLOWED`.
6. An unprotected engagement never creates or changes exposure.
7. `AMBIGUOUS` and parse failure never create exposure.
8. The state-relevant semantic classification is independently matched by validators.
9. A permit is bound to exact policy, actor, reference and consumer.
10. An allowed permit is consumable at most once.
11. A blocked, inconclusive, cancelled or already-consumed engagement cannot be consumed.
12. Different actors maintain independent walls.
13. Different domains maintain independent walls.
14. There is no declassification/clear path inside a policy version.
15. Consumer acknowledgement is emitted only after the consumer transaction finalizes.
