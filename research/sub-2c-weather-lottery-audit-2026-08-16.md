# Sub-2c daily-temperature lottery audit — 2026-08-16

**Question:** does buying `YES <= $0.02` (or `NO <= $0.02`) become repeatably +EV when the exact resolver station's running daily extreme is already inside or adjacent to that bucket in the final ~3h of the local day?

**Verdict:** **NO-GO on scaling to $5/$10 tickets. Keep $2 only as an evidence-acquisition ticket until the state-conditioned denominator exists.**

The observed locked-state anchor is spectacular but not decision-grade: **1 win / 3 cases = 33.33%**, versus fee-adjusted break-even probabilities of only **0.105% at 0.1c, 1.0495% at 1c, and 2.098% at 2c**. But the three cases are a hand-detected/non-uniform sample and the repo does not contain the historical quote + resolver-state snapshots needed to measure the requested 30–60 day frequency or class calibration without look-ahead. The exact 95% Clopper-Pearson interval for 1/3 is **0.84%–90.57%**; even ignoring sample-selection bias, its lower bound does **not** clear 1c or 2c break-even.

A separate wallet audit finds **13 identifiable <=2c weather YES positions across three repeat cheap-tail buyers; all 13 selected buckets ultimately lost**. That sample is **not state-aligned** to the running-extreme rule and therefore must not be used as its calibration. It does show that `price <=2c` by itself is not the edge.

Labels below:

- **MEASURED** = directly supported by repo/API/profile/settlement evidence.
- **INFERRED** = arithmetic or interpretation from measured inputs.
- **NOT MEASURED** = required point-in-time field was not recoverable; no estimate substituted.

---

## 1. Frequency — requested 30–60 day denominator

| Quantity | Result | Status |
|---|---:|---|
| Resolved high/low events with a point-in-time final-3h resolver extreme **and** contemporaneous `<=2c` executable ask archived | **not available as a systematic sample** | NOT MEASURED |
| State-aligned lottery detections preserved in the repo evidence ledger | **3** | MEASURED |
| Wins | **1** | MEASURED |
| Losses | **2** | MEASURED |
| Naive hit rate on those detections | **33.33%** | MEASURED |

Why the requested frequency cannot be honestly supplied from the current archive:

1. `research/CHANGES-2026-08-16.md` preserves only three locked-state lottery outcomes, not every eligible quote/state observation.
2. The repo contains historical price/markout work, but no 30–60 day archive of full L2 ask snapshots joined to resolver-station running extrema at the same timestamps.
3. The one-shot GitHub backfill workflow that ran on 2026-08-12 was a **wallet trade backfill** and left no workflow artifact containing historical books.
4. Current/resolved Polymarket pages cannot be substituted for the historical final-3h ask: doing so would be look-ahead.

Therefore the true denominator

`eligible <=2c state quotes / all resolved high-low event-windows`

is **not identified** in the present data.

---

## 2. Calibration and EV

### State-aligned calibration table

| State class | n | wins | empirical q | 95% exact CI | EV conclusion |
|---|---:|---:|---:|---:|---|
| All preserved locked-state lotto cases | 3 | 1 | **33.33%** | **0.84%–90.57%** | large plug-in edge, but non-uniform/selected sample; not scale-grade |
| Low vs high | — | — | — | — | NOT MEASURED: the change ledger identifies HK as a low win but does not preserve the side/class of both Paris losses |
| Minutes-to-lock bands | — | — | — | — | NOT MEASURED |
| Boundary distance bands | — | — | — | — | NOT MEASURED |
| Precip present/absent | — | — | — | — | NOT MEASURED |
| `NO <=2c` state cases | 0 demonstrated | — | — | — | NOT MEASURED / no calibration |

**Measured anchor from `research/CHANGES-2026-08-16.md`:**

- Hong Kong low, 16 Aug: HKO running state at **29C**, 29C bucket offered **0.1–0.2c**, final minimum **29.0C**, win; repo paper accounting reports **+$1,998 at a $2 raw stake at 0.1c**.
- Paris: **2 losses**, recorded entry prices **1.0–1.9c**, repo ledger records losses of roughly **$4–$6**. The ledger does not retain the decision-time precipitation, exact minutes-to-lock, boundary distance, or enough event identity to reconstruct those strata without guessing.

### Fee-adjusted break-even probability

User-specified taker fee per share:

`fee(p) = 0.05 * p * (1-p)`

For a YES share bought at ask `p`, break-even is:

`q_BE = p + fee(p)`

| Ask | fee/share | q break-even | one win per N equal-price tickets |
|---:|---:|---:|---:|
| 0.1c | 0.004995c | **0.104995%** | 952.43 |
| 0.2c | 0.009980c | **0.209980%** | 476.24 |
| 0.5c | 0.024875c | **0.524875%** | 190.52 |
| 1.0c | 0.049500c | **1.049500%** | 95.28 |
| 1.5c | 0.073875c | **1.573875%** | 63.54 |
| 2.0c | 0.098000c | **2.098000%** | 47.66 |

This is the core economic fact: the strategy does **not** need a high hit rate. At 2c it needs a calibrated state-conditioned win rate above ~2.10%; at 0.1c only ~0.105%.

### Plug-in arithmetic from the current 1/3 anchor — **not a forecast**

For raw ticket dollars `S`, assuming a true win probability `q` and ask `p`:

`EV_ticket = S * (q/p - 1 - 0.05*(1-p))`

If one mechanically plugs in `q = 1/3` from the selected n=3 anchor:

| Ask | $2 ticket EV | $5 ticket EV | $10 ticket EV |
|---:|---:|---:|---:|
| 0.1c | +$664.57 | +$1,661.42 | +$3,322.83 |
| 1.0c | +$64.57 | +$161.42 | +$322.84 |
| 1.9c | +$32.99 | +$82.47 | +$164.95 |
| 2.0c | +$31.24 | +$78.09 | +$156.18 |

Those numbers explain the attraction but **must not be annualized**: both `q` and the weekly qualified-opportunity count are unmeasured on an unbiased 30–60 day sample.

Expected dollars/week therefore remain:

`EV_week = N_qualified_week * EV_ticket`

with both `N_qualified_week` and unbiased class `q` **not identified** yet. Reporting a dollar/week number would manufacture the two missing quantities.

---

## 3. Failure modes — Paris-type losses

### What is measured

The repo already found one concrete, money-relevant state bug in a neighboring strategy family: using **current observation** instead of **running daily extreme** made previously achieved tropical peaks appear dead after showers cooled the station. Singapore/Taipei/Guangzhou losses exposed it; `supervisor.py` v4 changed the state anchor to running max/min. This is a valid failure separator for any extrema strategy: **current temp is not sufficient state**.

The two Paris lotto losses prove a second point: **running-extreme-in/adjacent-bucket is not itself a lock**. The exact observable separator is not recoverable from the preserved ledger because the following decision-time fields were not stored for those two cases:

- minutes remaining in the relevant local extreme window;
- distance from running extreme to nearest bucket boundary;
- current observation versus running extreme;
- precipitation/convective flag;
- last observation timestamp / reporting cadence;
- post-entry station updates before lock.

### Failure variables to measure next — not conclusions

These are the minimum features required to separate future winners/losses without changing trading logic:

`{market_side, minutes_to_lock, run_extreme, current_temp, boundary_distance, precip_since_state, last_obs_age, next_obs_arrival}`

No precipitation rule is justified by the present sample. `precip=present` and `precip=absent` remain uncalibrated strata.

---

## 4. Capacity

### Historical displayed depth

**NOT MEASURED.** No systematic historical L2 snapshot archive was found for the final-3h 30–60 day window. Current books and resolved-page prices cannot reconstruct past displayed shares at a given ask.

### Executed/held cheap-tail dollars — lower bound only

These wallet positions demonstrate that at least these raw dollars were acquired/held at the quoted average prices; they are **not displayed depth estimates**:

| Wallet/sample | largest identified <=2c position cost | total identified <=2c raw cost | interpretation |
|---|---:|---:|---|
| ColdMath | **$7.92** | **$9.85** across 2 | executed/held demand lower bound |
| WeatherHK2 | **$4.48** | **$5.83** across 3 | executed/held demand lower bound |
| anon `0xbb7a...ded18` | **$3.00** | **$14.30** across 8 | broad dust-tail basket |
| `samhain4ik` visible Aug-3 basket | **$2.51** | **~$17.00** across 17 | broad dust-tail basket; not settlement-audited here |

Observed wallet ticket sizes therefore support **$2** as routinely executable in at least some cheap tails. They do **not** establish that **$10 can be filled at <=2c without walking the book** in the target state. Scaling to $10 needs actual contemporaneous L2 depth capture.

---

## 5. Wallet fingerprints — primary audit

Important separation: the table below audits **cheap weather tails**, not the running-extreme state. A wallet only counts as evidence for the target edge if its entry can be timestamp-joined to the exact resolver state. Public profile snapshots expose average entry/size but not maker/taker role or exact entry timestamp, so those fields are left unfilled rather than inferred.

| Wallet | identifiable <=2c weather sample | settled selected buckets | hit rate | raw entry cost | hold-to-resolution payoff/PnL if no exit | entry clock / state lock | maker/taker | fingerprint |
|---|---:|---:|---:|---:|---:|---|---|---|
| **ColdMath** `0x594e...1c11` | 2 London daily-low YES: 13C @0.7c, 12C @1.3c | **0W / 2L**; final low was 15C | **0%** | **$9.8463** | $0 payout / **-$9.8463 pre-fee** | NOT MEASURED | NOT MEASURED | concentrated adjacent cheap-low tails |
| **WeatherHK2** `0xdadb...1870` | HK high 26C @2c; Guangzhou high 29C @2c; 28C @0.3c | **0W / 3L**; HK winner 27C, Guangzhou winner 31C | **0%** | **$5.8270** | $0 payout / **-$5.8270 pre-fee** | NOT MEASURED | NOT MEASURED | profitable regional weather specialist overall, but these cheap tails lost |
| **anon** `0xbb7a...ded18` | 8 cheap highs across Chicago/Wellington/Paris/Ankara | **0W / 8L** | **0%** | **$14.3011** | $0 payout / **-$14.3011 pre-fee** | NOT MEASURED | NOT MEASURED | broad dust-tail basket, many cities/outcomes |
| **Combined settled cheap-tail sample** | **13** | **0W / 13L** | **0%** | **$29.9744** | $0 / **-$29.9744 pre-fee** | — | — | **not state-conditioned** |

For the combined 0/13 sample, the exact two-sided 95% binomial upper bound on win probability is **24.71%**. That wide interval is another reminder that even 13 cheap-tail outcomes do not estimate a 0.1–2c edge precisely, and—more importantly—these 13 are selected wallet holdings rather than eligible-state observations.

### Supplied specialist wallet

Repo file `research/data/target-wallet-enriched-trades.csv` contains **1,766 official Data API fills** for supplied wallet `0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f` and shows a dominant modal/near-modal strategy. Low-price searches of the full enriched trade response surfaced cheap **SELLs** rather than demonstrated <=2c BUYs. I therefore find **no evidence that the supplied specialist is a sub-2c lottery exploiter**; I do not convert that into an asserted exact zero because this audit did not run a local machine-filter over the CSV bytes.

### Who is actually exploiting this exact state?

**Not established.** The data found repeat cheap-tail buyers, including profitable weather specialists, but no wallet for which this audit can demonstrate all three simultaneously:

1. repeated `<=2c` BUY fills;
2. entry **after** the exact resolver running extreme moved inside/adjacent to the bucket;
3. positive realized PnL on that state-conditioned subset.

That distinction matters. WeatherHK2 can be profitable in weather overall while going 0/3 in its identifiable <=2c tails; the edge may be elsewhere in its book.

---

## 6. Exact buy/no-buy rule from current evidence

### Buy at research size only

A candidate qualifies only when all of these are recorded at decision time:

1. exact resolver station/source, unit, rounding and local-day convention verified;
2. latest observation timestamp `<= decision_timestamp`;
3. running max (high) or running min (low) reconstructed only from observations available by then;
4. bucket contains the running extreme or is the immediately adjacent bucket under resolver precision;
5. decision timestamp is inside the final 3h local window;
6. actual executable average entry price after book walking is `<=2c`;
7. the class has a measured lower confidence bound `q_L` satisfying
   `q_L > p + 0.05*p*(1-p)`;
8. requested shares fit observed book depth at/under the calibrated price ceiling.

**Current consequence:** condition 7 is not established for any requested class on an unbiased sample. Therefore use **$2 only for measurement**, not because $2 is intrinsically optimal, but because it is the smallest existing ticket that cheaply converts missing calibration/depth into higher-grade evidence.

### Never buy / never scale

- never use current temperature as a substitute for running daily max/min;
- never use a city proxy when the contract resolves on a different exact station/source;
- never use an observation published after the decision timestamp;
- never call an adjacent bucket a lock if the resolver's rounding/bucket boundary does not actually make it adjacent;
- never scale a class whose empirical lower-bound `q` does not exceed fee-adjusted break-even;
- never size above contemporaneously displayed depth while still modeling the fill at the top ask;
- never infer a precipitation filter until precip-present/absent calibration exists.

---

## 7. Scaling verdict

| Ticket | Verdict now | Reason |
|---:|---|---|
| **$2** | **GO only as measurement ticket** | demonstrated cheap-tail executability in wallet samples; maximizes information per dollar while calibration is missing |
| **$5** | **NO-GO for systematic scaling** | state q and final-3h frequency not identified; depth not systematically archived |
| **$10** | **NO-GO** | same calibration gap plus observed cheap-tail wallet tickets often below $10; no historical L2 support |

The highest-value next measurement is not another forecast model. It is a **point-in-time event log** for every eligible quote: station observation timestamp, running extreme, boundary distance, precip flag, quote/depth, side, local minutes-to-lock, and eventual settlement. Once ~50–100 *eligible-state* cases exist, the requested class table and $/week estimate become directly estimable.

---

## Sources / evidence trail

### Repository

- `AGENTS.md`
- `research/CHANGES-2026-08-16.md`
- `research/data/target-wallet-enriched-trades.csv`
- `research/data/target-wallet-structure-analysis.md`
- `research/specialist-archetypes.md`
- `research/data/t0-observation-markout-sample.md`
- `.github/workflows/research-backfill-once.yml`

### Official/public Polymarket pages used for wallet positions and final outcomes

- ColdMath: `https://polymarket.com/profile/0x594edb9112f526fa6a80b8f858a6379c8a2c1c11`
- WeatherHK2: `https://polymarket.com/profile/0xdadbf9e1df1b8d7a184a0d6ab9c83b2337b61870`
- anon cheap-tail basket: `https://polymarket.com/profile/0xbb7a6e5b0d5b6a2fe797c00c5c7b8b11772ded18`
- London low Jul-21 resolver: `https://polymarket.com/event/lowest-temperature-in-london-on-july-21-2026`
- Hong Kong high Jul-29: `https://polymarket.com/event/highest-temperature-in-hong-kong-on-july-29-2026`
- Guangzhou high Jul-28: `https://polymarket.com/event/highest-temperature-in-guangzhou-on-july-28-2026`
- Paris high Jul-22: `https://polymarket.com/event/highest-temperature-in-paris-on-july-22-2026`
- Paris high Jul-23: `https://polymarket.com/event/highest-temperature-in-paris-on-july-23-2026`
- Chicago high Jul-22: `https://polymarket.com/event/highest-temperature-in-chicago-on-july-22-2026`
- Ankara high Jul-22: `https://polymarket.com/event/highest-temperature-in-ankara-on-july-22-2026`

### API semantics

- Public Data API trades endpoint documentation: `https://docs.polymarket.com/api-reference/core/get-trades-for-a-user-or-markets`
- Public closed-position endpoint documentation: `https://docs.polymarket.com/api-reference/core/get-closed-positions-for-a-user`

No trading logic or source code was modified in this audit.