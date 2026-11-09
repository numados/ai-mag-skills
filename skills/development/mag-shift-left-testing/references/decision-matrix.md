# Risk-to-seam decisions

Choose a seam by what it can reliably observe, not by layer name. A seam is a candidate only when it can produce a trustworthy signal for the specific risk; the earliest such seam wins.

## Seam ladder (earliest first)

Ordered by lifecycle position, not quality. Later does not mean better.

1. **Requirement / design review.** Catches ambiguity, impossible contracts, missing acceptance criteria, and risks that should not reach code. Cheapest; verifies intent, not behavior.
2. **Static / compile-time.** Types, contracts, lints, forbidden-pattern checks, schema or API-contract checks. Fast and deterministic; catches only what the tool models.
3. **Unit / component seam.** Smallest boundary that observes one invariant without pinning private details. Best for business rules and edge cases.
4. **Integration seam.** A fake, an in-process host, or a real provider that exercises wiring, contracts, serialization, and lifetime across the boundary.
5. **End-to-end / environment.** Full path through a real or production-like environment. Highest cost and slowest signal; reserve for risks no earlier seam can observe.
6. **CI gate / release.** A reproducible command sequence that fails the pipeline; owns ordering and which failures block.

## Mapping risk to earliest reliable seam

| Risk | Earliest reliable seam | Why not earlier / when to move later |
|---|---|---|
| Ambiguous requirement, impossible acceptance criterion | Design review | No code seam can verify an unstated contract. |
| Business-rule correctness, boundary and error cases | Unit / component | Deterministic and close to the rule; move later only when the rule manifests only across a boundary. |
| Wrong contract, wiring, or lifetime between components | Integration seam | Unit tests of each side cannot observe the mismatch. |
| External dependency semantics (timeout, retry, ordering, recovery) | Contract or recorded fake first; a real provider only if the contract itself is the risk | A live dependency is rarely the earliest reliable seam; its absence or nondeterminism defeats reliability. |
| Concurrency or race | Smallest deterministic reproduction (a controlled scheduler or an explicit interleaving when available) | Wall-clock sleeps and parallel smoke tests are not reliable signals. |
| Data integrity across writes | Integration or end-to-end against a real or equivalent store | In-memory substitutes can hide storage semantics. |
| Compatibility (API, version, platform) | Static or compile-time against the declared contract matrix | Running one configuration proves only that configuration. |
| Security or operational behavior | Design review plus the narrowest check that exercises the control | These are risk domains, not automatic categories; verify only controls the change actually touches. |

Choose the earliest seam that satisfies both conditions in the SKILL — as early as possible and trustworthy for this risk. If a seam cannot produce a reliable signal, move later or change the seam; do not claim "shifted left" just because a test exists.

## Trade-offs when two seams compete

- **Earliness vs reliability.** A fast unit test that asserts the implementation rather than the behavior is later in effect (it will not catch the real failure) than a slightly later integration test that observes the contract. Reliability wins.
- **Cost vs reach.** Move a check later when it needs an environment that is expensive or unavailable, and record that as a gap, not as a completed verification.
- **Determinism.** Prefer controllable time, network, filesystem, and randomness; a test that still depends on the wall clock or a live service is environmental and must be labeled as such.
