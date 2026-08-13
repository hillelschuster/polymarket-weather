# ENSO RONI publication-basis research

Snapshot: **2026-08-13**

## Research verdict

The new 2026–27 “Super El Niño” market is another clean publication-basis contract: it resolves on NOAA CPC's first published Relative Oceanic Niño Index (RONI) values for a defined set of overlapping seasons, with a threshold at **+2.0°C**.

This creates two separate research layers:

1. **seasonal ENSO strength forecasting** — estimate the probability that at least one target 3-month season reaches +2.0°C;
2. **first-publication reconstruction** — estimate the RONI value CPC will initially publish from monthly/weekly SST information before that exact seasonal value appears on the RONI page.

The second layer is especially attractive because CPC explicitly warns that recent RONI values may later change, while the Polymarket contract is tied to the first published qualifying value rather than an eventually revised historical index.

Official sources:

- https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/roni/
- https://www.cpc.ncep.noaa.gov/data/indices/index.shtml
- https://polymarket.com/event/will-there-be-a-super-el-nino-this-winter-202627-20260721221614682

---

## 1. Exact RONI definition

NOAA CPC currently defines RONI using:

- a 3-month running mean of ERSST.v5 SST anomalies in Niño 3.4;
- subtraction of the average tropical-mean SST anomaly over 20°N–20°S;
- an adjustment so the variance matches the original Niño 3.4 index;
- a 1991–2020 base period for the current table.

This is not identical to the traditional ONI or to raw Niño 3.4 SST anomaly.

Therefore a correct reconstruction must target **RONI**, not substitute:

- weekly Niño 3.4;
- monthly Niño 3.4;
- ONI;
- model-predicted Niño 3.4;

without applying the documented relative/tropical-mean transformation and variance adjustment.

---

## 2. First-published value matters

CPC's RONI page says it is updated by the **5th of each month** and warns that recent RONI values can change for up to two months because of the high-frequency filter applied to ERSSTv5.

That makes point-in-time labels essential.

For research store:

- first publication of each target season;
- every later revision;
- value eventually appearing in the historical table;
- Polymarket rule treatment of the first qualifying value.

A backtest using only today's revised historical RONI table can mislabel what the market actually would have known at the contractual publication time.

---

## 3. Current contract structure

The current Polymarket contract resolves Yes if RONI is +2.0°C or higher for **any** of:

- ASO 2026;
- SON 2026;
- OND 2026;
- NDJ 2026–27;
- DJF 2026–27.

Thus if `R_s` is RONI for season `s`, the event is:

`E = max_s R_s >= 2.0`

The seasons overlap heavily, so their probabilities are highly dependent. Do not sum independent seasonal exceedance probabilities.

The correct object is a joint trajectory distribution over monthly relative Niño-3.4 values and their CPC transformation.

---

## 4. Three-month arithmetic creates strong partial-season constraints

For a target season such as OND:

`RONI_OND = transform(relative_ERSST_Oct, relative_ERSST_Nov, relative_ERSST_Dec)`

Once one or two component months are largely observed, the remaining monthly anomaly needed to cross +2.0 becomes increasingly constrained.

Research can express this as:

`required_remaining_relative_SST = threshold implied by observed component months + transformation`

The exact variance adjustment should be reproduced from CPC methodology rather than approximated silently.

This is analogous to monthly precipitation/annual temperature accumulation: observed components progressively reduce remaining uncertainty.

---

## 5. Weekly and monthly precursor information

CPC's index page publishes several useful point-in-time SST series, including:

- weekly OISSTv2.1 Niño indices;
- monthly OISSTv2.1;
- monthly ERSSTv5 Niño 3.4;
- monthly relative ERSSTv5 Niño 3.4;
- seasonal relative ERSSTv5 3-month averages.

Official source:

- https://www.cpc.ncep.noaa.gov/data/indices/index.shtml

The likely hierarchy is:

1. weekly relative/current SST information provides an early within-month state;
2. monthly ERSSTv5 relative Niño 3.4 sharpens the completed-month estimate;
3. CPC seasonal RONI publication provides contractual index truth.

The useful research object is the historical mapping from stages 1–2 into stage 3.

---

## 6. CPC itself publishes strength probabilities

NOAA CPC currently publishes official ENSO strength probabilities by overlapping season, including an `Index >= 2.0°C` category.

In the July 2026 strength outlook, CPC assigned very large probabilities to ≥2.0°C in several target seasons, including approximately:

- ASO: 48%;
- SON: 71%;
- OND: 81%;
- NDJ: 75%;
- DJF: 54%.

Official source:

- https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/roni/strengths/

These are valuable public priors but do **not** directly equal the probability that the contract resolves Yes, because:

- seasons are highly dependent;
- the contract asks whether **any** listed season crosses the threshold;
- the strength outlook may itself be updated before the corresponding RONI publication;
- exact first-publication semantics matter.

Still, CPC's own probability distribution is a strong baseline that a custom model must improve upon, not ignore.

---

## 7. Forecast model hierarchy

A minimal strength model should begin with public ENSO information already known to be predictive:

- current weekly relative Niño-3.4 state;
- monthly relative ERSSTv5;
- subsurface heat content;
- equatorial thermocline/Kelvin-wave state;
- low-level westerly wind anomalies;
- NMME/CFSv2 strength distribution;
- CPC official strength probabilities.

The objective is not to outbuild climate-center models from scratch.

Instead test whether a simple ensemble/calibration model can improve the contract-specific target:

`P(max target-season first-published RONI >= 2.0)`

particularly as component months become observed.

---

## 8. First-publication reconstruction may be easier than long-horizon strength prediction

Early in the event lifecycle, the main uncertainty is meteorological/oceanographic.

Late in the lifecycle, after most component months have occurred, the problem changes:

`future ENSO uncertainty -> index/publication basis uncertainty`

At that stage, reproducing CPC's first-published RONI may matter more than another seasonal climate forecast.

This is the same strategic pattern as GISTEMP:

- forecast the physical state while uncertainty is large;
- switch toward dataset/index reconstruction as the publication approaches.

---

## 9. Revision-basis study

For every RONI season since the modern methodology is reconstructable, store vintages:

- first published value;
- +1 month revision;
- +2 month revision;
- latest historical value.

Then estimate:

- first-to-final bias;
- revision standard deviation;
- frequency of threshold crossing reversal near +2.0;
- whether revision error depends on ENSO strength or trend.

For Polymarket, the economically relevant label is the first publication specified by the rule, so later revision behavior is useful mainly for estimating first-publication uncertainty—not for changing the settlement label afterward.

---

## 10. Connection to existing GISTEMP/annual-temperature research

ENSO state also affects global temperature distributions with a lag.

Therefore a RONI trajectory model can serve two purposes:

1. value ENSO-specific contracts;
2. improve priors for GISTEMP monthly and annual-rank markets.

This is a real cross-market information connection, but the resolver functions differ and must remain separate.

The same latent ENSO trajectory can feed both models without forcing identical probabilities or timelines.

---

## 11. Current capacity and priority

The current Super El Niño contract is new and small relative to flagship Weather markets, with indexed volume around **$1.8k** in the latest page inspected.

That makes it lower immediate dollar priority than daily temperature, Arctic sea ice, Mt. Washington wind or major climate-rank markets.

However, the research has high reuse value because:

- CPC publishes the exact target index and official strength probabilities;
- the event has a clean +2.0 threshold;
- overlapping seasons create an interesting joint-distribution problem;
- late-stage first-publication reconstruction is tractable;
- ENSO trajectory informs other climate contracts.

Priority: **medium strategic / high reuse**.

The smallest useful research result is:

> reconstruct historical first-published RONI vintages and test whether monthly/weekly relative ERSST information predicts the first seasonal value more tightly than the public market probability already implies.