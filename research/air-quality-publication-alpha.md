# Air-quality publication and cumulative-state research

Snapshot: **2026-08-13**

## Research verdict

PM2.5 Air Quality Index markets are a genuinely distinct Weather family with three attractive properties:

1. the contractual daily AQI is based on a full-day PM2.5 quantity, while AirNow's public current AQI uses a different NowCast algorithm;
2. finalized Historical Air Quality values can appear after much of the underlying hourly monitor data already exists;
3. some Polymarket AQI markets use multiple nested “below 100 by date” deadlines, creating exact logical consistency constraints across outcomes.

This suggests a research program around **resolver reconstruction + cumulative 24-hour state + temporal contract consistency**, not generic smoke headlines.

---

## 1. Existing Polymarket capacity is already material

Resolved July 2026 examples:

- NYC “PM2.5 AQI below 100 by...?” event: roughly **$42.6k** total volume in an indexed snapshot;
- Chicago analogous event: roughly **$22k** by resolution;
- a World Cup Final stadium AQI event: roughly **$6.4k**.

Official Polymarket examples:

- https://polymarket.com/event/nyc-air-quality-index-below-100-byptptpt-20260717052808748
- https://polymarket.com/event/chicago-air-quality-index-below-100-byptptpt-20260717130414628
- https://polymarket.com/event/highest-air-quality-index-at-the-stadium-during-the-world-cup-final-20260717141117378

The NYC/Chicago rules specify the finalized AirNow **Historical Air Quality** reporting-area row and the **Daily AQI for PM2.5** column.

This means the settlement object is not simply the live dial visible on AirNow during the day.

---

## 2. Current AQI and final daily AQI are different information objects

AirNow/EPA documentation distinguishes:

### Daily AQI

For particle pollution, the daily AQI corresponds to a **24-hour** time frame.

Official AirNow source:

- https://www.airnow.gov/aqi/aqi-basics/using-air-quality-index/

EPA's current AQI technical documentation likewise defines PM2.5 daily AQI from the 24-hour pollutant concentration framework.

Official EPA source:

- https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P101AP0Q.TXT

### NowCast AQI

AirNow's “current AQI” uses a NowCast algorithm combining multiple recent hourly observations and adapting the averaging weight when air quality changes quickly.

That makes NowCast useful as a real-time signal but not the contractual final daily PM2.5 AQI in the NYC/Chicago examples.

This difference is exactly the kind of resolver-basis problem that has produced useful Weather research elsewhere in the repo.

---

## 3. Threshold concentration can be reconstructed directly

EPA's current AQI breakpoint table shows for PM2.5:

- AQI 51–100 corresponds to 24-hour concentration **9.1–35.4 µg/m³**;
- AQI 101–150 begins at **35.5 µg/m³**.

Official EPA breakpoint source:

- https://aqs.epa.gov/aqsweb/documents/codetables/aqi_breakpoints.html

Therefore a contract asking whether daily PM2.5 AQI is **below 100** can be studied at the underlying 24-hour concentration level rather than repeatedly converting an unstable current NowCast.

The exact reporting-area aggregation semantics still need to be reconstructed empirically; do not assume one monitor or one simple regional average without verification.

---

## 4. Partial-day state has useful arithmetic

Suppose a local calendar day has `h` valid hourly PM2.5 concentration observations with cumulative concentration sum:

`S_h = sum_{j=1..h} c_j`

Ignoring missing-data/reporting-area complications for the moment, the eventual 24-hour average is:

`C_24 = (S_h + R_h) / 24`

where `R_h` is the sum of remaining hourly concentrations.

This gives a simple threshold formulation:

`R_h < 24*K - S_h`

for a final average below concentration threshold `K`.

As the day progresses, the remaining amount compatible with the threshold becomes increasingly constrained.

This is structurally similar to monthly precipitation:

- past concentration-hours are already realized;
- future concentration-hours are uncertain;
- the final publication arrives later.

Unlike precipitation, high future PM2.5 can offset earlier clean hours and vice versa, so the state is an accumulating average rather than a monotone sum. But the remaining threshold budget is still explicit.

---

## 5. Finalized reporting-area basis must be learned

The Polymarket rules name a reporting area such as “New York City Region” or “Chicago,” not necessarily one monitor.

AirNow provides reporting-area current/historical data and monitor-level data, while EPA's AQS ecosystem provides regulatory historical data.

Research should determine historically:

- which PM2.5 monitors contribute to the finalized AirNow reporting-area daily value;
- whether the reporting-area daily AQI is the maximum monitor AQI, another aggregation, or changes with monitor availability;
- treatment of missing hours;
- timestamp/date convention;
- preliminary versus finalized changes;
- how often AirNow historical values differ from values reconstructed from real-time feeds.

Do not encode an assumed aggregation rule until this is measured against finalized historical pages.

---

## 6. Wildfire-smoke transition is a meteorological forecast problem layered on top

For smoke episodes, the remaining concentration distribution depends strongly on:

- transport wind direction/speed;
- boundary-layer mixing depth;
- frontal passage;
- precipitation/wet removal;
- fire emissions and plume injection;
- regional smoke arrival/departure timing.

The useful model target is narrow:

`P(remaining hourly concentrations keep/fall below the daily threshold | current accumulated state, meteorological/smoke state)`

rather than a generic AQI forecast.

AirNow itself notes that state/local forecasters use weather models, satellite imagery, monitoring data and pollution-transport models for AQI forecasts.

Official source:

- https://www.airnow.gov/aqi/aqi-basics/using-air-quality-index/

The first research baseline should use official forecasts/current monitor trajectories before adding a custom smoke model.

---

## 7. Nested “below 100 by date” contracts create exact probability ordering

The July NYC and Chicago event families asked whether the reporting area had a PM2.5 daily AQI below 100 between the starting date and progressively later deadlines.

Define:

`E_D = at least one qualifying daily AQI < 100 by deadline D`.

For `D1 < D2`:

`E_D1 => E_D2`

so fair probabilities must satisfy:

`P(E_D1) <= P(E_D2)`.

This is an exact logical relationship, subject only to identical rule/source semantics across the contracts.

The research opportunity is to measure:

- whether market probabilities respect this ordering at executable prices;
- whether one deadline updates faster than later/earlier deadlines after new daily information;
- whether the whole deadline curve is coherent with a common hazard model for the first clean day.

A common model is cleaner than forecasting each deadline independently.

---

## 8. First-clean-day hazard model

Let `T` be the first day in the contract window with finalized PM2.5 AQI below 100.

Then:

`P(E_D) = P(T <= D)`.

The incremental daily hazard is:

`h_d = P(T=d | T>=d)`.

This naturally connects the nested Polymarket deadlines.

Inputs to `h_d` can include:

- current day's partial PM2.5 state;
- official next-day AQI forecast;
- smoke transport/meteorology;
- persistence of the current episode;
- monitor/reporting-area basis uncertainty.

The hazard formulation turns four superficially separate contracts into one probability distribution over the first qualifying day.

---

## 9. Point-in-time evidence plan

For each historical AQI event/day store:

- reporting area;
- local date;
- final AirNow Historical Air Quality PM2.5 daily AQI;
- hourly monitor concentrations available point-in-time;
- AirNow current/NowCast values;
- official AQI forecast vintages;
- first-seen timestamps;
- Polymarket prices for every deadline;
- final outcome.

At each hour estimate:

- current accumulated/partial-day concentration state;
- probability the current day finishes below 100;
- probability each later deadline has seen a qualifying day;
- model-vs-market residual.

Primary metrics:

- calibration of current-day threshold probability;
- improvement from hourly concentration state over current NowCast alone;
- finalized reporting-area basis error;
- coherence of nested market probabilities;
- market response to finalized daily publication.

---

## 10. Short-duration AQI extrema are a separate subfamily

The World Cup stadium market resolved on the highest PM2.5 current AQI during a game window, using an AirNow current figure / named monitor fallback.

That target is fundamentally different from final daily AQI:

- it uses current/NowCast information;
- it is a short-window running maximum;
- hourly publication cadence and monitor selection dominate.

Do not combine these records with daily finalized-AQI research merely because both are labelled “AQI.”

---

## 11. Economic ranking

Current evidence grade:

- **resolver distinction between current and daily AQI:** strong/official;
- **nested deadline relationship:** exact from contract logic;
- **historical market capacity:** meaningful, roughly $20k–$40k in the first examples;
- **forecast/publication edge:** not yet measured.

Priority: **medium-high and unusually attractive for diversification**.

Reasons:

- the required math is compact;
- many participants may confuse NowCast with final daily AQI;
- wildfire smoke creates large discrete distribution shifts;
- nested deadlines create a reusable common hazard surface;
- official hourly data and historical labels exist;
- the mechanism is largely independent of daily-temperature forecast errors.

The smallest decisive study is:

> Reconstruct the July 2026 NYC and Chicago events hour by hour from point-in-time PM2.5 monitor data and compare a common first-clean-day hazard curve with the four Polymarket deadline probabilities.