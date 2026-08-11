# GISTEMP input vintages — the late-stage information clock

Snapshot: **2026-08-11**

Purpose: determine whether a direct GISTEMP replica can gain information **before NASA's scheduled first publication**, and what minimal data must be preserved to measure the edge correctly.

The key result is favorable:

> **NOAA GHCN-M v4 explicitly provides daily rapid-access updates, while NASA consumes the adjusted qcf product for GISTEMP. These daily vintages are not retained long-term. A live trader only needs to snapshot the ~44 MB qcf tarball when it changes and run NASA's public code.**

This is small enough to be operationally trivial and economically important enough to justify doing exactly.

---

# 1. NOAA confirms daily GHCN-M v4 updates

NCEI's official GHCN-M v4 metadata states:

> Daily updates to GHCN-M V4 are available for users that require rapid access to the most current data. However, they will not be retained long-term. Permanently retained files are archived once per month.

Official dataset metadata:
https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc%3AC00950

NCEI also describes many operational GHCNm stations as providing **short time delay updates useful for climate monitoring**.

Product page:
https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-monthly

This makes the land input a continuously changing information source, not a single release-day file.

---

# 2. NASA explicitly uses the adjusted qcf product

NASA's GISTEMP FAQ states that the analysis uses GHCN v4 adjusted monthly mean data and specifically notes:

- **qcf is used**;
- qcu is not the production input.

NASA source/FAQ:
https://data.giss.nasa.gov/gistemp/faq/
https://data.giss.nasa.gov/gistemp/sources/gistemp.html

Thus the file to snapshot is:

`ghcnm.tavg.latest.qcf.tar.gz`

not a raw/unadjusted GHCN bundle.

---

# 3. File size is negligible relative to the edge

Current NCEI directory lists the qcf archive around **44 MB**.

Directory:
https://www.ncei.noaa.gov/pub/data/ghcn/v4/

Even storing every distinct qcf version for a two-week post-month window would be trivial by modern standards.

The useful record for each snapshot is only:

`download_time_utc`
`server_last_modified`
`sha256`
`file_path`
`target_month_station_count`
`gistemp_replica_output`.

No database infrastructure is required.

---

# 4. July 2026 live timing already shows a plausible lead

For the July 2026 GISTEMP publication cycle:

## Ocean

NCEI ERSST-v5 directory listed:

`ersst.v5.202607.nc`

at **2026-08-03 10:42 UTC**.

## Land

During the research pass, the current adjusted qcf bundle was observed with a release-day timestamp around **2026-08-11 03:42 UTC**.

## NASA

NASA's official July GISTEMP schedule:

**2026-08-11 15:00 UTC**.

So the exact input family used by NASA had a potential release-day lead measured in hours, while the ocean field was available days earlier.

The remaining question is content, not timing:

> **At which qcf vintage did running the NASA code first produce the same bracket NASA eventually published?**

That is a clean empirical variable.

---

# 5. The correct live experiment for August 2026

NASA's scheduled August GISTEMP release is:

**2026-09-10 15:00 UTC**.

Starting September 1:

1. poll only NCEI file metadata/hash;
2. when ERSST August file appears, save it;
3. whenever qcf hash changes, save the new qcf archive;
4. run unchanged NASA GISTEMP v4 source against that exact input vintage;
5. record the August LOTI result and Polymarket bracket;
6. record the full Polymarket ladder at the same timestamp.

For each qcf version define:

`replica_value_t`
`replica_bracket_t`
`market_probability_same_bracket_t`.

After NASA publication, calculate the first time:

`t_correct = earliest snapshot where replica_bracket == NASA_first_bracket`.

Then the economic lead is:

`lead = NASA_release_time - t_correct`.

This single number is highly informative.

---

# 6. More important than exact-value error: bracket stability

Polymarket pays brackets, not squared-error scores.

Suppose replica outputs over successive qcf versions are:

`1.184, 1.187, 1.191, 1.188°C`.

All lie in/around the same 1.15–1.19 bracket, except boundary sensitivity at 1.190 depending exact contract edges.

The trading question is:

`P(final first-publication value remains inside current bracket)`.

So measure:

- replica value drift between qcf versions;
- maximum remaining historical release-day drift at the same lead time;
- distance to nearest Polymarket bracket boundary.

A replica 0.02°C from the nearest boundary is economically different from one 0.001°C from it even if point-error expectations are identical.

---

# 7. Minimal uncertainty model by time before release

From live/historical dry runs estimate:

`delta_h = NASA_first_value - replica_value_h_hours_before_release`.

For lead-time bins such as:

- D+3;
- D+5;
- D+7;
- 24h;
- 12h;
- 6h;
- 2h;

retain the empirical `delta` distribution.

Then for current replica `g`:

`G_first ~ g + delta_h`.

Integrate that tiny residual distribution over the actual Polymarket bins.

No climate ML is required.

---

# 8. Historical difficulty is not a live-strategy difficulty

NOAA says daily GHCN-M rapid-access updates are **not retained long-term**.

That means exact historical release-day qcf vintages may be difficult to reconstruct for 2024–2026.

Do not confuse that with an inability to trade the edge going forward.

For research:

- use monthly permanent snapshots, resolved Polymarket brackets and ERA5T/ERSST basis models historically;
- collect exact qcf vintages prospectively from now onward;
- after several months, directly estimate the replica lead/residual distribution.

The live measurement problem becomes easier every month simply by saving the files.

---

# 9. Earlier D+3/D+5 stage does not need qcf perfection

Before the land input is mature:

## D+3

ERSST-v5 provides most of the ocean information.

## D+5

ERA5T gives a full-month independent reanalysis.

A simple basis model can produce an earlier, wider GISTEMP distribution.

The trading pipeline naturally has two stages:

### Stage A — basis trade

Days before NASA:

`P(GISTEMP bracket | ERA5T + ERSST + partial land)`.

Potentially larger price discrepancy, larger model uncertainty.

### Stage B — direct replica

Hours before NASA:

`P(GISTEMP bracket | current exact NASA upstream files)`.

Smaller uncertainty, potentially narrower remaining price gap but much higher confidence/capacity.

Measure dollar EV at each stage. There is no reason to choose one philosophically.

---

# 10. Input-file publication itself is a tradable event clock

For monthly climate markets, important event timestamps are not news headlines.

They are:

- new ERSST monthly file;
- ERA5T full-month completion;
- qcf hash/version change;
- NASA scheduled publication.

For each event calculate immediate ladder repricing at:

- pre-event;
- +5m;
- +30m;
- +2h;
- +6h.

If qcf updates occur hours before market repricing, the direct-replica edge can be exploited with ordinary polling and simple taker/maker routing.

---

# 11. NASA's own production behavior supports the approach

NASA states its monthly graphs/tables are updated around the 10th using the **current** NOAA GHCN v4 and ERSST v5 files, including the previous month plus late/corrected earlier reports.

NASA GISTEMP:
https://data.giss.nasa.gov/gistemp/

NCEI's daily qcf access exists specifically for rapid current-data use.

The direct-replica hypothesis is therefore not attempting to predict a hidden proprietary process. It is trying to execute the same public algorithm earlier against public inputs.

---

# 12. Smallest production requirement implied by research

When implementation eventually starts, climate input capture can literally be:

- one HTTP HEAD/metadata check;
- hash on change;
- save tarball;
- run NASA source;
- append one row to a CSV/SQLite table.

No service architecture, climate database or broad pipeline is justified by the current problem.

The sophistication belongs in **knowing which input vintage matters**, not in software structure.

---

# Bottom line

NOAA confirms the exact land dataset NASA uses has **daily rapid-access vintages**, and those vintages disappear unless we save them.

That creates a very concrete high-capacity experiment for the August 2026 Polymarket contract:

> **Snapshot each changed qcf file, combine it with the already-available ERSST, run NASA's public GISTEMP code, and measure the first timestamp at which the paid bracket becomes stable relative to market price.**

If that stability occurs hours before NASA at materially sub-$1 prices, the climate strategy becomes one of the simplest and largest-dollar edges in the project.