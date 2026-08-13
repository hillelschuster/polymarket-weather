# U.S. Drought Monitor publication-basis research

Snapshot: **2026-08-13**

## Research verdict

The new Polymarket U.S. Drought Monitor markets expose a clean delayed-publication forecasting problem.

The official U.S. Drought Monitor (USDM) uses a weekly process in which:

- the data cutoff is Tuesday at 8:00 AM Eastern;
- the map is released Thursday at 8:30 AM Eastern;
- the final map is a human synthesis of many physical indicators rather than one mechanical index.

Official sources:

- https://droughtmonitor.unl.edu/
- https://droughtmonitor.unl.edu/About/WhatistheUSDM.aspx
- https://droughtmonitor.unl.edu/ConditionsOutlooks/Inputs.aspx

This creates a roughly two-day interval during which much of the underlying weekly evidence has already been fixed while the contractual weekly USDM state has not yet been published.

The research target is therefore:

> estimate the next published categorical percent-area value from the point-in-time inputs and previous map, then compare that estimate with the market probability surface.

---

## 1. Current Polymarket rule is publication-date specific

The current Virginia market asks whether D4 Exceptional Drought reaches at least 1.00% of Virginia in any weekly USDM release published through August 31, 2026.

The rule explicitly says eligibility is determined by the **release publication date**, not the Tuesday “data valid” date.

Official Polymarket example:

- https://polymarket.com/event/will-virginia-reach-d4-exceptional-drought-by-august-31-2026-20260721193543607

The settlement statistic is the official USDM weekly **Categorical Percent Area** table for the state.

This matters because the natural forecast object is the next official polygon/area result, not a generic drought index.

---

## 2. USDM is intentionally not a deterministic model

USDM documentation says authors synthesize many inputs, including:

- precipitation;
- streamflow;
- reservoir levels;
- temperature and evaporative demand;
- soil moisture;
- vegetation health;
- local impact reports and expert input.

The lead author makes judgement calls when indicators disagree.

Therefore a perfect reconstruction cannot simply apply one threshold to SPI/PDSI/soil moisture.

The useful model is closer to:

`next_map = previous_map + expected analyst boundary changes given current evidence`

This suggests a spatial transition model rather than an independent state-level classification model.

---

## 3. Previous map provides a very strong prior

Drought polygons usually evolve geographically rather than redraw randomly each week.

For a state currently near a D4 threshold, the most informative variables are likely:

- existing D4 polygon location/area;
- D3 area adjacent to D4;
- week-over-week precipitation deficits/surpluses near the boundary;
- soil moisture/streamflow/evaporative stress changes;
- local author notes/impacts;
- persistence duration;
- neighboring-state polygon evolution.

For a threshold market such as `D4 >= 1.00%`, the model does not need to predict the entire national map perfectly. It only needs the distribution of the target state's categorical area around the threshold.

---

## 4. Publication interval creates a point-in-time dataset

For every weekly release store:

1. previous Thursday USDM map/table;
2. every input dataset version available by Tuesday 8 AM cutoff;
3. Tuesday cutoff timestamp;
4. any author/impact information available point-in-time;
5. Thursday publication timestamp;
6. final state categorical percentages;
7. related Polymarket price history.

This provides a clean no-lookahead training row:

`X_tuesday -> Y_thursday`

The approximately two-day publication gap makes this a slower research problem than T+0 temperature observations and should allow careful probability computation without latency-focused infrastructure.

---

## 5. Official USDM exposes many of its research inputs

The USDM Inputs page publishes downloadable weekly source layers and authoring files, including examples such as:

- precipitation/SPI/SPEI;
- CPC and WWDT products;
- NLDAS2;
- NASA GRACE soil moisture;
- CPC soil moisture;
- USGS streamflow/well information;
- evaporative-demand indices;
- vegetation health and drought-response indices.

Official source:

- https://droughtmonitor.unl.edu/ConditionsOutlooks/Inputs.aspx

This is unusually useful because the target product openly identifies much of the evidence its authors use.

The research should start with a minimal subset rather than ingest every layer:

- previous USDM category polygons;
- 7/30/60/90-day precipitation percentiles;
- soil moisture percentile;
- streamflow percentile;
- evaporative demand;
- recent heavy precipitation;
- season/state fixed effects.

Add additional layers only if they improve out-of-sample threshold probability.

---

## 6. Spatial boundary model

For each grid/polygon cell near the previous D3/D4 boundary, estimate a transition probability such as:

`P(category_next >= D4 | category_prev, indicators, local trend)`

Then aggregate simulated cells/polygons to state percent area.

This preserves the spatial nature of the USDM better than directly regressing one statewide percentage.

A simpler first model can operate on historical state-level transitions:

`Delta_D4_area = f(previous D4 area, D3 area, precipitation anomaly, soil moisture, streamflow, season)`

The simple model is preferable until spatial detail demonstrates incremental value.

---

## 7. Threshold-event hazard across multiple weekly releases

The Virginia contract is not simply “will the next map have D4 >=1%?” It asks whether **any eligible weekly release** through the deadline reaches the threshold.

Let `A_j` be the event that release `j` has D4 area >= 1.00%.

The contract event is:

`E = union_j A_j`

so the probability depends on the entire remaining weekly path.

A compact simulation can propagate weekly drought-state transitions through the remaining releases and estimate:

`P(max_j D4_area_j >= 1.00%)`

The same framework naturally handles different thresholds, states and dates.

---

## 8. Human-author effect is a feature, not merely noise

USDM lead authors rotate, and the map is explicitly judgement-based.

Research should test whether transition behavior differs by:

- lead author;
- region;
- season;
- fast-onset/flash-drought regime;
- recovery versus deterioration regime.

Do not overfit author identities with a small sample, but preserve the field because human synthesis is part of the contractual publication process.

The most durable predictor may be the **previous map plus input changes**, with author identity only a modest residual feature.

---

## 9. Current capacity is small, mechanism quality is high

The first Virginia/Oregon D4 markets are new and currently much smaller than flagship daily-temperature or climate markets.

That lowers immediate dollar priority but does not reduce the structural quality of the research problem.

The family can become more attractive if Polymarket lists:

- more states;
- national/region drought percentages;
- lower categories such as D2/D3 with more frequent transitions;
- longer-duration thresholds;
- crop-region or seasonal drought markets.

The same weekly model would transfer across these contracts.

---

## 10. Evidence plan

Historical backfill:

- 10+ years of weekly USDM state percentages/polygons;
- point-in-time weekly input layers where recoverable;
- previous-map state;
- publication/cutoff dates;
- author metadata.

First benchmarks:

1. persistence-only: next map = current map;
2. historical transition frequency conditioned on current category/area;
3. simple state-level indicator model;
4. spatial boundary model.

Primary metrics:

- probability calibration near threshold;
- Brier/log loss;
- state-percent-area error;
- first-threshold-cross timing;
- incremental information beyond persistence.

---

## 11. Economic priority

Evidence grade:

- publication clock: **strong/official**;
- resolver statistic: **explicit**;
- input availability: **strong**;
- forecastability: plausible but human-synthesis basis must be measured;
- current Polymarket capacity: low/new.

Priority: **medium strategic research**, with a strong option value if the market family expands.

The key attraction is unusual:

> most of the physical evidence feeding Thursday's contractual map is already known by Tuesday, and the official process publishes many of the same inputs used by its human authors.

That is exactly the kind of resolver-publication transformation this project is designed to exploit.