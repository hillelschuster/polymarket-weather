# ECMWF AIFS public-timing thesis — deep dive

Snapshot: **2026-08-13**

## Verdict

AIFS is the strongest new **reusable information-timing** candidate for international temperature markets.

The useful thesis is not that AIFS is universally a better weather model than IFS.

It is narrower:

> ECMWF currently releases open AIFS data as soon as it is produced, while open IFS data are released only at the end of the real-time dissemination schedule. If early AIFS revisions contain predictive information about the later resolver distribution or later model consensus, AIFS can provide a public information lead before the free IFS release and before some Polymarket repricing.

Official ECMWF sources:

- Open data: https://www.ecmwf.int/en/forecasts/datasets/open-data
- AIFS data: https://www.ecmwf.int/en/forecasts/dataset/aifs-machine-learning-data

This should be tested as a **revision signal**, not as a raw deterministic-temperature oracle.

---

## 1. The timing asymmetry is real, but exact lead must be measured

ECMWF's current open-data documentation states:

- open IFS data are released at the **end** of the real-time dissemination schedule;
- open AIFS data are released **as soon as the data are produced**;
- AIFS deterministic and ensemble forecasts run four times per day: 00/06/12/18 UTC;
- open AIFS contains resolver-relevant surface variables such as 2 m temperature.

This creates a plausible lead window for AIFS relative to the public IFS feed.

However, dissemination is progressive. The exact target lead is not simply `IFS schedule end - AIFS cycle start`.

For a given city/date, the relevant timestamp is:

`aifs_target_field_first_seen(city, valid_time)`

not the cycle headline time.

The first required measurement is therefore a small timestamp logger, not a backtest assumption.

---

## 2. What AIFS needs to predict

The target is the **resolver daily maximum distribution**, not the raw 2 m temperature at one grid point.

For city/station `c`, cycle `r`, and target day `d`, derive an AIFS daily-max feature:

`m_A(c,r,d) = max_h T2m_A(c,r,d,h)`

using the forecast steps covering the resolver local day.

Then calibrate to the exact station:

`Y(c,d) = resolver daily max`.

A first station model is:

`Y = alpha_c,horizon + beta_c,horizon * m_A + epsilon_c,horizon`.

The residual distribution converts the AIFS forecast max into bucket probabilities.

For a Celsius exact ladder with bucket `k`:

`q_A(k) = P(k - 0.5 <= Y < k + 0.5 | AIFS state)`

subject to the contract's actual rounding/precision semantics.

Use explicit resolver rules rather than a universal half-degree assumption where the contract differs.

---

## 3. The key signal is revision, not level

Absolute station bias can be large and stable. Revisions are more promising because they may transfer across models and the market.

Define AIFS revision:

`Delta_A = m_A(r_new) - m_A(r_old)`.

Define later consensus revision:

`Delta_C = m_consensus(later) - m_consensus(prior)`.

The minimum predictive model is:

`E[Delta_C | Delta_A, city, horizon] = alpha + beta * Delta_A`.

If `beta > 0` and predictive residual variance is small enough, the early AIFS change is informative before later guidance arrives.

For the full ladder, estimate the vector transformation:

`Delta q_C ~= B_(city,horizon) * Delta q_A`.

But do not start with a high-dimensional matrix unless the scalar max-revision model leaves obvious value on the table.

---

## 4. AIFS Ensemble should be preferred when timely enough

AIFS ENS produces an ensemble probability object directly.

For each member `j`:

`M_j = max_h T2m_j(h)`.

Apply station bias calibration member-wise or through a calibrated ensemble distribution.

Then:

`q_A(k) = (1/N) * sum_j 1(member j resolver-max falls in bucket k)`

with smoothing/calibration for finite ensemble size.

This gives two useful features:

1. **location shift** — ensemble center moves hotter/colder;
2. **shape change** — dispersion/skew changes even if the mean barely moves.

Exact-temperature markets are especially sensitive to shape because moving 0.5°C of probability mass can shift the modal bucket dramatically.

The relevant comparison is economic timing versus AIFS Single, not theoretical ensemble superiority. If AIFS ENS arrives too late relative to the market, Single may be the useful fast signal.

---

## 5. The profit question is information ordering

For each forecast cycle, record four clocks:

1. `AIFS relevant field first_seen`;
2. `Polymarket ladder first material reprice`;
3. `open IFS relevant field first_seen`;
4. `later independent/consensus guidance first_seen`.

Then ask:

### Did AIFS lead the market?

`L_market = t_market_reprice - t_AIFS`.

Positive values mean the AIFS field arrived before the market reaction.

### Did AIFS correctly anticipate later information?

For bucket vector revisions:

`directional_agreement = sign(Delta q_A) == sign(Delta q_later)`.

More useful:

`R2 / log-loss improvement of later resolver distribution using AIFS revision`.

### Was the market reaction proportional?

Let pre-AIFS executable market probability be `p^-` and calibrated early fair probability be `q_A`.

The economic discrepancy is not raw model revision:

`edge_i = q_A(i) - executable_cost_i`.

Later markout is evidence that the information propagated; final settlement evaluates calibration.

---

## 6. Best historical sample

Do not study every Weather city first.

Use the markets already connected to specialist-wallet/model-release evidence:

- Milan / Malpensa;
- Paris resolver airport under the correct regime;
- London / EGLC;
- Amsterdam / Schiphol;
- Munich / EDDM;
- Helsinki / EFHK.

Reasons:

- international exact-degree ladders create sensitivity to small probability shifts;
- ECMWF is highly relevant to European weather;
- existing repo work already contains Milan revision/wallet alignment;
- the resolver stations and historical market data are already partly mapped.

A Milan re-analysis should answer:

> Was the profitable-wallet/market revision visible first in AIFS, before the later conventional multimodel/IFS state used in the existing research?

If yes, this materially advances the existing T+1 thesis.

---

## 7. Point-in-time historical reconstruction

The dangerous mistake is to download a later archived AIFS field and assign it to cycle initialization time.

Each forecast vintage needs actual availability semantics.

For historical study:

- use ECMWF archive/catalogue data for the forecast field;
- preserve cycle and forecast-step metadata;
- use current live logging to learn dissemination lag structure;
- treat exact historical first-seen time as uncertain unless independently archived.

Therefore historical replay can establish **forecast information value**, while live source logging establishes **latency value**.

Do not conflate the two.

---

## 8. A simple state-space combination with the market

The market itself is informative and should be used as a prior.

Let market probability vector before the new AIFS field be `p_m`.

Let resolver-calibrated AIFS vector be `q_A`.

Instead of replacing the market with AIFS, estimate a likelihood-ratio update from historical forecast skill.

For bucket `i`:

`logit(q_post_i) = logit(p_m_i) + lambda * s_A_i`

where `s_A_i` is a standardized AIFS revision signal and `lambda` is estimated out of sample.

For a mutually exclusive ladder, a softmax formulation is cleaner:

`q_post_i = softmax(log(p_m_i + eps) + lambda * z_A_i)`.

This has two advantages:

- market information remains in the model;
- AIFS only needs to add incremental information, not win an absolute forecasting contest.

The decisive metric is out-of-sample log loss / Brier improvement and subsequent executable markout.

---

## 9. Failure modes that specifically destroy the thesis

The thesis weakens materially if one of these is observed:

1. AIFS target fields reach the public feed no earlier than the relevant market repricing.
2. AIFS revisions do not predict later resolver/consensus revisions after controlling for the market.
3. Station bias/noise is too large relative to 1°C bucket width.
4. The market already follows another source that reacts before AIFS.
5. Incremental forecast skill exists but executable spreads/fees consume it.

These are measurable defects, not generic objections.

---

## 10. Smallest decisive experiment

For 20–50 European city/date forecast cycles:

1. log exact AIFS field first-seen;
2. compute calibrated resolver-max bucket vector;
3. snapshot Polymarket L2 around first-seen;
4. record later free IFS and multimodel state;
5. measure 1m/5m/30m/2h ladder markout;
6. evaluate eventual resolver calibration.

Key table:

| city/date | cycle | AIFS first seen | AIFS max revision | q modal before/after | market price before | +5m | +30m | later IFS revision | final bucket |

### Promotion criterion

AIFS earns a production lane if it repeatedly provides an incremental resolver-probability revision **before** market repricing and that revision predicts later information/final outcomes strongly enough to clear actual executable costs.

## Bottom line

AIFS is attractive because it can improve the most reusable existing Weather mechanism—T+1 forecast-revision timing—without requiring a new category, resolver, or execution architecture.

The first question is not “is AIFS the best model?”

It is:

> **Does the early public AIFS revision tell us where the resolver probability surface is going before the free IFS feed and before Polymarket finishes repricing?**
