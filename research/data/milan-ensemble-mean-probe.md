# Milan ECMWF ensemble mean/spread probe

Generated: **2026-08-12T10:21:25.016879+00:00**

Model: `ecmwf_ifs025_ensemble_mean` via Open-Meteo Ensemble Mean API.

Purpose: test whether the post-18Z wallet actions are more compatible with a distribution-shape update than with the deterministic daily maximum alone.

**Important:** the normal bucket number below is an hourly proxy built from the archived ensemble mean and spread. It is not the probability of the civil-day maximum landing in the Polymarket bucket.

## milan_june25 — target 2026-06-25

### Wallet actions

- `2026-06-25T01:11:47Z` — **SELL 33°C** — 193.780000 @ 0.1142
- `2026-06-25T01:12:02Z` — **BUY 34°C** — 65.217390 @ 0.4600

| Run | Station | Peak ensemble mean | Spread at peak | Max hourly normal proxy for target bucket | Proxy time |
|---|---|---:|---:|---:|---|
| 2026-06-24T12:00 | LIMC | ERROR | ERROR | ERROR | `<HTTPError 400: 'Bad Request'>` |
| 2026-06-24T12:00 | LIML | ERROR | ERROR | ERROR | `<HTTPError 400: 'Bad Request'>` |
| 2026-06-24T18:00 | LIMC | ERROR | ERROR | ERROR | `<HTTPError 400: 'Bad Request'>` |
| 2026-06-24T18:00 | LIML | ERROR | ERROR | ERROR | `<HTTPError 400: 'Bad Request'>` |

## milan_june30 — target 2026-06-30

### Wallet actions

- `2026-06-29T01:55:11Z` — **BUY 35°C** — 102.116000 @ 0.2938

| Run | Station | Peak ensemble mean | Spread at peak | Max hourly normal proxy for target bucket | Proxy time |
|---|---|---:|---:|---:|---|
| 2026-06-28T12:00 | LIMC | ERROR | ERROR | ERROR | `<HTTPError 400: 'Bad Request'>` |
| 2026-06-28T12:00 | LIML | ERROR | ERROR | ERROR | `<HTTPError 400: 'Bad Request'>` |
| 2026-06-28T18:00 | LIMC | ERROR | ERROR | ERROR | `<HTTPError 400: 'Bad Request'>` |
| 2026-06-28T18:00 | LIML | ERROR | ERROR | ERROR | `<HTTPError 400: 'Bad Request'>` |

## Interpretation rule

The useful signal is run-to-run change, not the absolute proxy:

- if the 18Z target-bucket proxy rises in the same direction as the wallet action, ensemble mean/spread contains information absent from the deterministic-max-only view;
- if it does not, do not rescue the hypothesis with storytelling: the next candidate is another forecast source, resolver bias/post-processing, or market-relative-value execution rather than direct ECMWF bucket probability.
