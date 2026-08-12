# Bounded Milan multi-model probe

Generated: **2026-08-12T11:11:24.609963+00:00**

All values are archived deterministic daily maxima at LIMC. Nearest-degree votes and distance are diagnostics, not calibrated settlement probabilities.

## milan_june25 — target 2026-06-25

Wallet: **SELL 33°C** @ 0.1142, **BUY 34°C** @ 0.4600

| Stage | Model | Run | Max | Nearest |
|---|---|---|---:|---:|
| pre_12z | ECMWF IFS | 2026-06-24T12:00 | 33.30°C | 33°C |
| pre_12z | DWD ICON-EU | 2026-06-24T12:00 | ERROR | — |
| pre_12z | DWD ICON Global | 2026-06-24T12:00 | 32.90°C | 33°C |
| pre_12z | ARPEGE Europe | 2026-06-24T12:00 | 32.50°C | 33°C |
| pre_12z | ItaliaMeteo ICON-2I | 2026-06-24T12:00 | ERROR | — |
| post_18z | ECMWF IFS | 2026-06-24T18:00 | ERROR | — |
| post_18z | DWD ICON-EU | 2026-06-24T18:00 | ERROR | — |
| post_18z | DWD ICON Global | 2026-06-24T18:00 | 34.60°C | 35°C |
| post_18z | ARPEGE Europe | 2026-06-24T18:00 | 33.90°C | 34°C |
| post_18z | ItaliaMeteo ICON-2I | 2026-06-24T12:00 | ERROR | — |

12Z mean/median: **32.90/32.90°C**
18Z mean/median: **34.25/34.25°C**
12Z votes: `{"33": 3}`
18Z votes: `{"34": 1, "35": 1}`

### Wallet-bucket movement

| Bucket | Vote Δ | Mean distance Δ | ≤0.75°C Δ | ≤1.25°C Δ |
|---:|---:|---:|---:|---:|
| 33°C | -3 | +0.950°C | -3 | -2 |
| 34°C | +1 | -0.750°C | +1 | +0 |

ICON-EU 21Z candidate: error `HTTP 429: {"reason":"Too many concurrent requests","error":true}`

## milan_june30 — target 2026-06-30

Wallet: **BUY 35°C** @ 0.2938

| Stage | Model | Run | Max | Nearest |
|---|---|---|---:|---:|
| pre_12z | ECMWF IFS | 2026-06-28T12:00 | 34.30°C | 34°C |
| pre_12z | DWD ICON-EU | 2026-06-28T12:00 | 31.80°C | 32°C |
| pre_12z | DWD ICON Global | 2026-06-28T12:00 | 31.60°C | 32°C |
| pre_12z | ARPEGE Europe | 2026-06-28T12:00 | 34.10°C | 34°C |
| pre_12z | ItaliaMeteo ICON-2I | 2026-06-28T12:00 | 34.40°C | 34°C |
| post_18z | ECMWF IFS | 2026-06-28T18:00 | 33.90°C | 34°C |
| post_18z | DWD ICON-EU | 2026-06-28T18:00 | 32.70°C | 33°C |
| post_18z | DWD ICON Global | 2026-06-28T18:00 | 32.60°C | 33°C |
| post_18z | ARPEGE Europe | 2026-06-28T18:00 | ERROR | — |
| post_18z | ItaliaMeteo ICON-2I | 2026-06-28T12:00 | 34.40°C | 34°C |

12Z mean/median: **33.24/34.10°C**
18Z mean/median: **33.40/33.30°C**
12Z votes: `{"32": 2, "34": 3}`
18Z votes: `{"33": 2, "34": 2}`

### Wallet-bucket movement

| Bucket | Vote Δ | Mean distance Δ | ≤0.75°C Δ | ≤1.25°C Δ |
|---:|---:|---:|---:|---:|
| 35°C | +0 | -0.160°C | -1 | -1 |

ICON-EU 21Z candidate: **27.90°C** (nearest 28°C).
