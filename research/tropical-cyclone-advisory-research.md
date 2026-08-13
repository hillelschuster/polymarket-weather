# Tropical cyclone advisory timing and contract semantics

Snapshot: **2026-08-13**

## Purpose

This note records a Weather-market research hypothesis around National Hurricane Center (NHC) advisory timing and exact Polymarket resolution rules.

The important distinction is between:

- predicting future cyclone intensity/track;
- knowing when an official NHC product first establishes a rule-relevant state;
- knowing whether the Polymarket contract uses that initial state or a later revised analysis.

These should be studied separately.

---

## 1. NHC has structured scheduled and special publication cycles

NHC's Tropical Weather Outlook is normally issued every six hours during the Atlantic season at 0000, 0600, 1200 and 1800 UTC. Special outlooks can be issued between scheduled cycles when meaningful changes occur.

Official source:

- https://www.nhc.noaa.gov/aboutgtwo.php

NHC verification documentation states that official tropical-cyclone forecasts are issued every six hours and include center position and maximum one-minute sustained surface wind forecasts.

Source:

- https://www.nhc.noaa.gov/verification/verify2.shtml

This gives a well-defined point-in-time publication structure for historical and live research.

---

## 2. ATCF contains real-time storm state

NHC's ATCF documentation describes storm-history data as real-time storm position, intensity and structure used for warning generation and objective forecast aids.

Official source:

- https://ftp.nhc.noaa.gov/atcf/docs/NRL_doc_ATCFdatabase.html

A useful source-latency study should compare the first-seen times of:

- ATCF storm-history changes;
- NHC text advisories;
- NHC graphical/web products;
- Polymarket price changes.

The goal is to establish which public representation exposes the rule-relevant state first.

---

## 3. Some Polymarket contracts explicitly depend on initial NHC advisory state

The current Polymarket market for the first Atlantic hurricane name states that a storm qualifies once it is categorized as a hurricane after market creation, and that an initial NHC advisory may determine the market even if later advisory/reanalysis revises the intensity downward.

Example:

- https://polymarket.com/event/what-will-be-the-name-of-the-first-hurricane-in-the-atlantic-for-the-2026-hurricane-season-20260723184627863

The current Category 5 U.S. landfall market similarly states that an initial NHC advisory reporting a qualifying Category 5 landfall may determine the event even if later analysis changes.

Example:

- https://polymarket.com/event/will-any-category-5-hurricane-make-landfall-in-the-us-in-before-2027

This means historical research must label the contract outcome using the exact rule-defined advisory state, not automatically substitute the eventual best-track dataset.

---

## 4. Threshold-state research

Relevant rule thresholds can include:

- hurricane designation at 74 mph or greater;
- Category 5 intensity at 157 mph or greater;
- landfall semantics based on center/coastline intersection;
- contract-specific counting windows that begin at market creation.

A historical event record should therefore store:

- contract creation time;
- exact rule text/version;
- advisory number and issuance time;
- reported status/intensity;
- track/landfall state where applicable;
- any later correction/reanalysis;
- whether the initial state already satisfied the Polymarket rule.

This prevents hindsight from changing the settlement object.

---

## 5. Predictive and publication-latency evidence must be separated

Two different hypotheses can be tested with the same dataset:

### Predictive hypothesis

Information available before an advisory may estimate the probability that the next NHC advisory crosses a rule threshold.

Potential inputs include latest official intensity/trend, reconnaissance, satellite analysis, environmental shear, SST/ocean heat, official forecast guidance and model aids.

### Publication-timing hypothesis

Once the official NHC product changes the rule state, the Polymarket market may or may not immediately reflect that new public information.

Do not combine these evidence classes. One is forecasting; the other is publication/market-response timing.

---

## 6. Cross-market rule graph

A single cyclone can affect multiple Polymarket contracts, but payoff relationships must be derived from exact rules.

Potentially related families include:

- first hurricane name;
- hurricane counts;
- major-hurricane counts;
- U.S. landfall;
- category-at-landfall markets;
- storm-specific track/intensity events.

Important semantic differences include:

- exact intensity band versus at-least threshold;
- market-creation cutoff;
- peak intensity versus intensity at landfall;
- initial advisory versus later analysis.

Similarity of titles is not enough to establish a deterministic relationship.

---

## 7. Research dataset

For each advisory transition:

- storm ID/name;
- advisory cycle and number;
- nominal valid time;
- first-seen ATCF timestamp;
- first-seen NHC text timestamp;
- first-seen graphical/web timestamp where measurable;
- old/new status;
- old/new maximum sustained wind;
- position and landfall state;
- related Polymarket market IDs/rules;
- market price timestamps before/after;
- later corrections or best-track changes.

Primary statistics:

- source-order/latency distribution;
- frequency of rule-relevant state transitions;
- market response after those transitions;
- forecast calibration before transitions;
- consistency across related contracts.

---

## 8. Capacity and research priority

The current Category 5 U.S. landfall market has shown more than $100k of volume in indexed Polymarket snapshots, so cyclone markets can have materially higher per-event capacity than many smaller Weather subfamilies.

The drawback is low event frequency and likely intense attention during major storms.

Current priority: **medium-high as an episodic/high-capacity research lane**.

The first useful result should simply answer:

> Which NHC/ATCF public product first exposes contract-relevant state, and how quickly do related Polymarket probabilities change after that state appears?

Only after measuring that should more complex cyclone-intensity forecasting be prioritized.