# New weather information sources and hypotheses — 2026-08-13

This note records additional Weather-market research directions discovered after the existing T+0 observation, T+1 model revision, resolver-precursor, climate-index and market-structure work.

## 1. ECMWF AIFS availability timing

ECMWF currently states that IFS open data are released at the end of the real-time dissemination schedule, while AIFS open data are released as soon as forecast data are produced.

Sources:
- https://www.ecmwf.int/en/forecasts/datasets/open-data
- https://www.ecmwf.int/en/forecasts/datasets/aifs-machine-learning-data

Research question: does earlier AIFS guidance contain useful information about later daily-extreme forecast revisions before comparable changes appear in Polymarket prices?

Suggested measurement fields are model cycle, exact file first-seen time, relevant local forecast hours, later IFS/local-model values, Polymarket price timestamps and final resolver outcome.

## 2. Station-native aviation forecast guidance

The Aviation Weather Center provides worldwide METAR and TAF access. Its cache files currently update all METARs once per minute and all TAFs every ten minutes. TAF issuance timestamps represent the time a forecast is completed and ready for transmission; amendments supersede the previous TAF immediately.

Sources:
- https://aviationweather.gov/data/api/
- https://aviationweather.gov/help/data/

Some international TAF regimes include explicit maximum/minimum temperature forecasts and timing. Coverage should be catalogued by resolver airport rather than assumed globally.

Research question: do changes in airport-specific operational forecasts add information beyond the global/regional model stack for exact-airport daily extrema?

## 3. U.S. LAMP station guidance

NOAA's Localized Aviation MOS Program updates most guidance hourly for more than 2,000 stations and provides station 2-meter temperature guidance out to 38 hours. Current documentation says temperature guidance is issued hourly and incorporates recent station observations plus model/MOS information.

Sources:
- https://vlab.noaa.gov/web/mdl/lamp
- https://vlab.noaa.gov/web/mdl/lamp-elements
- https://vlab.noaa.gov/web/mdl/lamp-nws-webservices

Research question: for U.S. airport resolvers, does LAMP improve remaining-heating / remaining-cooling probabilities relative to a simpler HRRR/global-model plus observation baseline?

## 4. Market-opening information state

Resolved London daily-temperature pages show a recurring pattern of markets opening around two days before their target dates, with eventual event volume commonly above $100k in the examples inspected.

Examples:
- https://polymarket.com/event/highest-temperature-in-london-on-july-1-2026
- https://polymarket.com/event/highest-temperature-in-london-on-july-7-2026
- https://polymarket.com/event/highest-temperature-in-london-on-july-12-2026
- https://polymarket.com/event/highest-temperature-in-london-on-july-17-2026
- https://polymarket.com/event/highest-temperature-in-london-on-july-18-2026

Research question: how efficient are the first minutes and hours of a newly listed ladder when several useful forecast cycles already exist before listing?

The useful dataset is creation timestamp, first available market prices, pre-list forecast probability surface and subsequent short-horizon price changes.

## 5. Weather maker subsidy as a measurement variable

Current Polymarket documentation states that Weather makers pay zero platform trading fee and Weather maker rebates receive 25% of eligible taker-fee pools. Rebate competition is calculated per market.

Sources:
- https://docs.polymarket.com/trading/fees
- https://docs.polymarket.com/market-makers/maker-rebates

Polymarket also documents a separate Liquidity Rewards methodology, with per-market incentive size/spread settings. Do not assume a Weather market has a separate reward allocation without checking its current market metadata.

Source:
- https://docs.polymarket.com/market-makers/liquidity-rewards

Research question: after conditioning on fill quality and adverse-selection markout, are there Weather markets where spread capture plus measured rebates/rewards materially changes the relative attractiveness of passive liquidity?

## 6. Local-midnight state transition

Daily-high and daily-low contracts have a resolver-specific local-day boundary. For markets already trading before the target local day begins, the first target-date observation immediately constrains the day's eventual extreme.

Research question: are prices around local midnight slow to incorporate the first target-date resolver observation, particularly in warm-night cities where the opening temperature can rule out lower high-temperature buckets?

This must be tested with exact resolver timezone, daylight-saving treatment and source date semantics.

## 7. Cross-market propagation

Weather forecast errors are correlated across nearby cities, adjacent dates and contracts affected by the same model cycle.

Research question: after controlling for the direct forecast update, does an early price move in a liquid related Weather market contain incremental information for a slower related market?

Candidate relationships include same-city adjacent dates, nearby cities under the same air mass, and multiple cities responding to one model cycle. This is probabilistic relative-value research, not a deterministic identity.

## 8. Spatial one-report-ahead nowcasting

Existing T+0 work measures value after a resolver observation appears. A harder but potentially earlier signal is predicting the resolver station's next report using nearby/upstream stations, radar/cloud evolution, wind shifts and local boundary propagation.

Research question: can a small spatial model materially improve the probability that the next resolver observation crosses the current extreme before that observation is published?

The minimum viable study should use only timestamped nearby observations and a few physically meaningful propagation features before adding complex models.

## 9. Monthly precipitation publication pipeline

NWS CF6 products for Central Park provide preliminary daily precipitation and running monthly totals. Current CF6 pages expose a `WTR` daily precipitation column and monthly total.

Example source:
- https://forecast.weather.gov/product.php?issuedby=NYC&product=CF6

Research question: can the final monthly bracket be estimated more accurately by combining the latest official cumulative total with rain that has occurred but has not yet entered the climate summary and with the remaining-month forecast distribution?

This separates accumulated official state, pending current-event precipitation and future uncertainty.

## 10. Tornado publication-basis research

Current Polymarket monthly tornado markets resolve from the first relevant NCEI U.S. Tornadoes time-series count published after a scheduled release time, even if that first value is labelled preliminary; later revisions do not change settlement.

Example:
- https://polymarket.com/event/how-many-tornadoes-in-the-us-in-august-2026-20260727150226367

NCEI publishes explicit monthly U.S. Tornadoes release dates/times.

Source:
- https://www.ncei.noaa.gov/access/monitoring/tornadoes/climatology

Research question: how predictable is that first scheduled NCEI count from point-in-time preliminary reports, survey outcomes and historical preliminary-to-published conversion patterns?

This is a resolver-publication basis problem rather than simply a severe-weather forecast problem.

## 11. Tropical cyclone advisory-state research

NHC's Tropical Weather Outlook is issued on a six-hour schedule with special updates possible between scheduled products. NHC also exposes real-time ATCF storm-history data used for warning generation and objective aids.

Sources:
- https://www.nhc.noaa.gov/aboutgtwo.php
- https://ftp.nhc.noaa.gov/atcf/docs/NRL_doc_ATCFdatabase.html

Polymarket hurricane-related rules can depend specifically on an initial NHC advisory and on the period after market creation. For example, current first-hurricane-name rules state that an initial qualifying NHC advisory may determine the event even if later reanalysis revises intensity downward.

Example:
- https://polymarket.com/event/what-will-be-the-name-of-the-first-hurricane-in-the-atlantic-for-the-2026-hurricane-season-20260723184627863

Research question: where does official NHC advisory/ATCF state become knowable before the corresponding Polymarket contract fully reflects the rule-defined state?

## Current research priority

The highest-value new measurements appear to be:

1. AIFS first-seen timing versus IFS and market response;
2. market-opening probability surfaces versus first market prices;
3. station-native aviation/LAMP incremental value;
4. spatial one-report-ahead resolver nowcast;
5. resolver-publication reconstruction for precipitation and tornado counts;
6. NHC advisory-state timing and rule mapping;
7. cross-market propagation and passive-liquidity subsidy as secondary overlays.

These directions are intentionally complementary to the repository's existing strongest work rather than duplicates of the already-developed T+0 observation and T+1 model-revision theses.