# Security model

## Threat model

ConflictWall assumes policy owners deliberately define conflict domains and registered clients. The primitive protects against later semantic engagement requests bypassing a previously acquired protected-client wall.

It does not prove that a client belongs to a real-world industry, discover undisclosed aliases, or infer secret corporate ownership. Those would require a separate identity/authority primitive.

## Fail-closed cases

- malformed model output;
- unknown classification;
- leader/validator disagreement on classification;
- ambiguous engagement description;
- wrong policy/client binding;
- wrong consumer;
- wrong actor/reference;
- replayed consumer acceptance;
- blocked or consumed permit reuse.

## Prompt injection

Policy and engagement text are explicitly treated as untrusted data in the classifier prompt. Instructions embedded in those fields must not redefine the task.

## Monotonicity

There is intentionally no `clear_exposure`, `switch_client`, or model-controlled declassification call. A sealed policy is a versioned safety boundary. A materially different wall policy should be represented by a new policy ID rather than silently rewriting existing history.

## Scope limitation

`UNPROTECTED` means the proposed engagement itself does not create material protected exposure under the frozen criteria. It is not a general statement that the client, actor or future activity is risk-free.
