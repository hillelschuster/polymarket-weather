# Milan multi-model revision alignment with target wallet

Snapshot: **2026-08-12**

Target wallet:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

## Verdict

The June 25 Milan case is now the strongest recovered event-level evidence that the supplied wallet reacts to fresh forecast revisions.

Immediately before the wallet rotated from **33°C YES into 34°C YES**, independent resolver-site deterministic guidance underwent a broad upward revision:

- DWD ICON-EU: **33.2 → 35.2°C** from 12Z to 18Z;
- DWD ICON Global: **32.9 → 34.6°C**;
- Météo-France ARPEGE Europe: **32.5 → 33.9°C**;
- ECMWF IFS: **33.3 → 32.8°C** (the one colder outlier);
- ItaliaMeteo ICON-2I: **35.3°C** at 12Z and unchanged in the clean comparison because it is 12-hourly.

Across those five provider/model inputs, the simple daily-max mean moved from **33.44°C to 34.36°C** (+0.92°C), while the median moved from **33.2°C to 34.6°C** (+1.4°C).

Nearest-degree diagnostic votes changed from:

`12Z: 33°C ×4, 35°C ×1`

to:

`18Z/latest: 33°C ×1, 34°C ×1, 35°C ×3`.

That is directionally consistent with the exact wallet actions at approximately 01:12 UTC:

- **SELL 33°C YES** — 193.78 shares @ ~11.42¢;
- **BUY 34°C YES** — 65.217 shares @ ~46¢.

The strongest claim supported by the data is therefore:

> A broad multi-provider upward forecast revision preceded and aligns with the wallet's removal of 33°C exposure and upward reallocation.

This is materially stronger than the earlier ECMWF-only timing hypothesis because the causal weather-side signal is visible across independent providers, not just one forecast model.

It is **not** proof that the wallet directly consumed any particular API or model.

---

# 1. Data recovered in this pass

Primary generated files:

- `research/data/milan-multimodel-fast.json`
- `research/data/milan-multimodel-fast.md`
- `research/data/milan-multimodel-retry.json`
- `research/data/milan-multimodel-retry.md`
- earlier ECMWF baseline: `research/data/milan-forecast-revision-probe.json`

Archived forecasts were fetched from Open-Meteo's Single Runs API at the LIMC / Malpensa resolver-site proxy.

Open-Meteo documents that `run=` selects an exact model initialization and that most non-ECMWF model runs are archived from 2026-04-02, so these June 2026 runs are inside the documented archive range:

https://open-meteo.com/en/docs/single-runs-api

DWD independently documents the relevant ICON cycles:

- ICON Global: 00/06/12/18 UTC;
- ICON-EU full runs: 00/06/12/18 UTC;
- ICON-EU short runs: 03/09/15/21 UTC, with the 21Z cycle extending +30h.

Official DWD source:

https://www.dwd.de/EN/ourservices/nwp_forecast_data/nwp_forecast_data.html

The 21Z ICON-EU June 24 run returned a complete 24-hour June 25 local-day series and a daily max of **35.4°C**. It is kept as additional evidence rather than silently included in the clean 12Z→18Z comparison because this research pass did not recover its exact historical public availability timestamp.

---

# 2. June 25 raw resolver-site model maxima

Target date: **2026-06-25**.

Wallet rotation: **2026-06-25 ~01:12 UTC**.

| Model | 12Z daily max | 18Z/latest comparable max | Revision |
|---|---:|---:|---:|
| ECMWF IFS | 33.3°C | 32.8°C | -0.5°C |
| DWD ICON-EU | 33.2°C | 35.2°C | **+2.0°C** |
| DWD ICON Global | 32.9°C | 34.6°C | **+1.7°C** |
| ARPEGE Europe | 32.5°C | 33.9°C | **+1.4°C** |
| ItaliaMeteo ICON-2I | 35.3°C | 35.3°C carried | 0.0°C |

Cross-provider revision breadth is the important feature:

- **3 independent model families moved upward by at least +1.4°C**;
- one model was already hot at 35.3°C;
- ECMWF alone moved colder.

So an ECMWF-only strategy would have seen conflicting information. A multi-model state would have seen a strong upward revision shock.

## Bucket-distance diagnostics

These are deliberately not called probabilities.

For **33°C**:

- mean absolute model distance: **0.68 → 1.44°C**;
- nearest-degree votes: **4 → 1**;
- models within 0.75°C: **4 → 1**.

For **34°C**:

- mean absolute model distance: **1.08 → 0.88°C**;
- nearest-degree votes: **0 → 1**;
- models within 1.25°C: **3 → 4**.

The 33°C deterioration is especially large and directly matches the wallet's sell.

---

# 3. Why the 34°C buy does not mean the wallet thought 34°C was the mode

Post-update deterministic guidance was centered roughly between 34°C and 35°C, with three of five nearest-degree diagnostics at 35°C.

Yet the wallet bought 34°C at ~46¢.

That is not contradictory to a probability/price strategy.

The correct decision variable is not:

`argmax model_temperature == bucket`.

It is approximately:

`q(bucket) - executable_all_in_price`.

A trader can rationally buy 34°C even if 35°C is the modal deterministic region when 34°C retains substantial probability and is cheaper relative to its fair probability.

At a raw 46¢ taker price under the current Weather fee formula, the approximate all-in cost would be about **47.24¢/share** before any other execution effects. Therefore a pure value entry requires internal `q_34` above roughly 47.2% if crossed as a taker.

The deterministic pseudo-ensemble recovered here cannot estimate that calibrated probability. It only establishes that the weather information moved materially upward and away from 33°C.

The event ultimately resolved **35°C**, so the 34°C purchase loses if held unchanged to settlement. The wallet may have subsequently revalued or exited; that history is still incomplete.

---

# 4. June 30 is a useful negative control

Target date: **2026-06-30**.

Wallet action at **2026-06-29 01:55:11 UTC**:

- **BUY 35°C YES** — 102.116 shares @ raw ~29.38¢.

Recovered LIMC model state:

| Model | 12Z | 18Z/latest comparable |
|---|---:|---:|
| ECMWF IFS | 34.3°C | 33.9°C |
| DWD ICON-EU | 31.8°C | 32.7°C |
| DWD ICON Global | 31.6°C | 32.6°C |
| ARPEGE Europe | 34.1°C | 32.2°C |
| ItaliaMeteo ICON-2I | 34.4°C | 34.4°C carried |

Combined mean:

- 12Z: **33.24°C**;
- post update: **33.16°C**.

Mean distance from 35°C:

- 12Z: **1.76°C**;
- post update: **1.84°C**.

Nearest-degree 35°C votes remained **zero**.

So this simple deterministic multi-model revision does **not** explain the June 30 35°C buy.

That is important evidence, not a failure to be narrated away.

Plausible remaining explanations that require separate measurement are:

1. 35°C still carried enough calibrated tail probability to be worth >30.4% all-in even when point forecasts were lower;
2. resolver-specific residual/bias calibration shifted the distribution upward relative to raw grid-cell maxima;
3. another forecast source or ensemble product supplied materially different information;
4. the market price was sufficiently cheap that a non-modal bucket still had positive EV;
5. this was simply a losing probabilistic trade.

The event resolved **34°C**, so a 35°C position held to settlement lost.

---

# 5. Correction: June 30 ICON-EU 21Z value must not be used

The bounded probe initially displayed a June 28 21Z ICON-EU value of 27.9°C for the June 30 target date.

That must **not** be interpreted as a June 30 daily-maximum forecast.

DWD documents that ICON-EU 21Z is a short +30h run. It does not cover the full June 30 daytime heating period from a June 28 21Z initialization. The API returned only the early part of the target date, so taking its maximum creates a partial-day artifact.

This is exactly the type of look-ahead/data-shape defect that must be removed from future event studies.

Rule for the research pipeline:

> Never calculate a civil-day forecast maximum unless the archived run covers the relevant full local-day peak window.

`target_hours` is now retained in the retry output for this reason.

---

# 6. Economic interpretation

The strongest usable signal from this pass is not a generic ensemble average.

It is **revision breadth**:

`how many independent forecast systems materially change the same event distribution in the same direction before the market fully reprices?`

June 25 has the structure desired for a potentially monetizable release signal:

1. several independent models revise upward strongly;
2. the old 33°C bucket loses cross-model support;
3. the wallet materially sells 33°C shortly after the overnight information window;
4. the wallet reallocates upward;
5. settlement ultimately lands even higher at 35°C.

A minimal live feature worth testing is therefore something like:

`revision_breadth(bucket) = weighted count of fresh provider updates that move probability mass away from/toward bucket`.

Do **not** hard-code a +1°C threshold or provider weights from this one case. The next measurement should determine whether revision breadth predicts market markout and wallet direction across more events.

---

# 7. Highest-value next measurement

The weather side of June 25 is now sufficiently reconstructed.

The next smallest measurement with direct PnL value is the **market side**:

recover the Milan June 25 ladder immediately before and after the 18Z-derived information became actionable, especially 33°C / 34°C / 35°C prices and depth.

Desired timestamps:

- pre-release / stale-market snapshot;
- around 00:15 UTC;
- 00:30 UTC;
- 01:00 UTC;
- wallet fills around 01:12 UTC;
- +30m and +2h markout.

Then calculate, for each bucket:

`weather_revision -> fair-value change -> executable price -> wallet action -> subsequent market markout`.

If the market lagged the broad upward revision and the wallet traded before repricing, that is the direct replicable edge.

If the market had already fully repriced, the wallet evidence is less useful for latency alpha and more useful for calibration/relative-value inference.

---

# Bottom line

This bounded research pass produced one strong positive case and one negative control.

**June 25:** multi-provider weather guidance shifted sharply upward, especially ICON-EU, ICON Global and ARPEGE; 33°C support collapsed immediately before the wallet sold 33°C and bought higher. This materially strengthens the forecast-revision hypothesis.

**June 30:** the same simple multi-model revision signal does not explain the wallet's 35°C buy. Preserve that contradiction and test calibrated distribution/price explanations rather than forcing the model to fit.

The highest-value next step is now historical **order-book/price reconstruction around the June 25 overnight revision**, not more broad weather-source research.