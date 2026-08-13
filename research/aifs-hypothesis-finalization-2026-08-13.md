# ECMWF AIFS timing hypothesis — final research specification

Snapshot: **2026-08-13**

## Verdict

The AIFS thesis remains attractive, but deeper source inspection materially narrows it.

The strong fact is a **public dissemination asymmetry**: ECMWF says open IFS data are released at the end of the real-time dissemination schedule, while open AIFS data are released as soon as the forecast is produced.

The important correction is that the current free AIFS open-data subset exposes **6-hourly instantaneous 2m temperature (`2t`)**, not the IFS-style interval-maximum fields (`mx2t3` / `mx2t6`) that would map more directly to a daily-high contract.

Therefore AIFS should be researched as an **early probability-revision feature**, not as a direct daily-maximum oracle.

---

## 1. Official dissemination facts

ECMWF Open Data currently states:

- IFS open data are released at the end of the real-time dissemination schedule;
- AIFS open data are released as soon as they are produced;
- AIFS Single and Ensemble run at 00/06/12/18 UTC;
- the open-data grid is 0.25 degrees in GRIB2;
- only the most recent rolling set of runs is kept on the real-time open endpoint/cloud mirrors.

Official source:

- https://www.ecmwf.int/en/forecasts/datasets/open-data
- https://www.ecmwf.int/en/forecasts/datasets/aifs-machine-learning-data

This means any timing study must save each relevant AIFS vintage when first observed rather than assume the real-time endpoint provides a historical archive indefinitely.

---

## 2. Material parameter limitation

The current AIFS open-data parameter list includes instantaneous 2m temperature and related state variables on 6-hour steps, but does not list `mx2t3` or `mx2t6` interval extrema.

By contrast, the IFS open-data parameter list includes interval maximum/minimum 2m-temperature fields.

Official source:

- https://www.ecmwf.int/en/forecasts/datasets/open-data

ECMWF visual products can display maximum/minimum 2m temperature over previous 6-hour intervals, but the existence of a chart product should not be silently equated with the public machine-readable AIFS subset.

Research consequence:

> AIFS timing can lead the market only through information contained in its sampled temperature/state trajectory and ensemble, not through a free exact daily-max field unless that data path is separately verified.

---

## 3. Minimal station-level transformation

For resolver station/day `d`, let AIFS sampled 2m temperatures be:

`T_00, T_06, T_12, T_18, ...`

A first resolver-max proxy can be deliberately small:

`M_AIFS = max(sampled_2t) + c_station(month, lead, regime)`.

The correction distribution captures the unobserved diurnal peak between 6-hour steps plus station/grid basis.

A better probabilistic version uses the AIFS ensemble:

for each member `m`:

`M_m = max(sampled_2t_m) + epsilon_station`.

Then construct a member-based distribution over the resolver maximum and calibrate to historical resolver outcomes.

Useful compact additional AIFS state may include variables that explain the missing peak:

- cloud cover / radiation-related state where available;
- wind;
- humidity/dew-point proxies;
- boundary-layer regime.

Do not add variables unless they reduce out-of-sample resolver error.

---

## 4. The correct timing signal is a revision, not the absolute forecast

For consecutive AIFS vintages:

`Delta_A = M_AIFS,new - M_AIFS,old`.

For resolver bucket vector:

`Delta_q_A = q_AIFS,new - q_AIFS,old`.

The first question is whether the early AIFS revision predicts a later revision in a stronger information set:

`E[Delta_consensus | Delta_A] = alpha + beta * Delta_A`.

Or at the probability-vector level:

`Delta_q_later ~= B * Delta_q_A`.

AIFS does not need to be the best final forecast. It needs positive **incremental information** while the market still reflects an older information set.

---

## 5. Condition on the market itself

To avoid rediscovering information already priced, evaluate AIFS after conditioning on current Polymarket probabilities.

One simple research form is:

`q_post = softmax(log(p_market + eps) + lambda * z_AIFS)`

where `z_AIFS` is a standardized vector representing the AIFS revision across buckets.

Compare resolver log loss/Brier score of:

- market alone;
- AIFS alone;
- market + AIFS.

The useful quantity is the improvement of `market + AIFS` over `market` during the window before later consensus/model information arrives.

---

## 6. Exact first-seen latency must be logged

Do not use a nominal model cycle schedule as the information timestamp.

For every target city/date field record:

- cycle initialization time;
- target forecast step;
- first successful availability from ECMWF direct open data;
- first successful availability from AWS/Azure/GCP mirrors if tested;
- local receive timestamp;
- first later IFS/consensus availability for the comparable target;
- Polymarket price/book response time.

Cloud mirrors may have different replication lag. Select an access path empirically; do not assume a particular mirror is fastest.

---

## 7. Best first city set

Start with international exact-temperature airport markets already represented in project research:

- Milan;
- London;
- Paris;
- Amsterdam;
- Munich;
- Helsinki.

Milan is especially valuable because the repo already contains specialist-wallet/model-revision evidence. AIFS can be tested as an earlier feature against a market where model-cycle sensitivity is already plausible.

---

## 8. Decisive dataset

For 20–50 AIFS cycles across active/recent city markets preserve:

### Model

- city/station/date;
- AIFS cycle;
- first-seen time;
- sampled 2t path;
- ensemble member paths if available;
- station-calibrated max distribution;
- probability-vector revision.

### Later information

- comparable IFS/other-model arrival time;
- later consensus probability revision;
- final resolver outcome.

### Market

- market probability/book state at AIFS first seen;
- 1m/5m/15m/30m/60m price response;
- next major model-arrival response.

Historical first-seen timestamps cannot safely be reconstructed from model initialization alone. The cleanest test is prospective logging.

---

## 9. Falsification / downgrade criteria

Downgrade the AIFS timing thesis if:

1. actual Polymarket repricing usually precedes public AIFS target-field availability;
2. 6-hour instantaneous sampling creates too much daily-max uncertainty for narrow resolver buckets;
3. `beta` for AIFS revision -> later consensus revision is near zero after conditioning on current market information;
4. station/grid basis overwhelms the revision signal;
5. AIFS adds no out-of-sample resolver probability skill over market + existing model state;
6. observed timing advantage is only nominal schedule lead and disappears using actual first-seen timestamps.

---

## 10. Final research deliverable

The hypothesis is finalized when the project has:

- an empirical first-seen latency distribution for relevant AIFS fields;
- a station-calibrated transformation from open AIFS sampled 2t to resolver bucket probabilities;
- evidence on whether AIFS revisions predict later consensus/resolver revisions after conditioning on market state;
- synchronized market response measurements from AIFS first seen through later model release.

At that point we will know whether AIFS is a genuinely early public signal or merely an interesting model with no monetizable information-order advantage.