# Milan case study — repeated wallet revaluation after ECMWF 18Z

Snapshot: **2026-08-11**

Purpose: isolate the strongest currently recovered behavioral fingerprint from the supplied wallet.

Wallet:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

The important observation is not merely that this wallet trades Milan. Two independent Milan actions on different dates occur in the same narrow overnight information window and point in opposite directions:

1. **June 25:** materially reduces 33°C YES after fresh overnight forecast information; that bucket later loses.
2. **June 29:** buys June 30 35°C YES at 01:55 UTC after the same forecast-cycle window; that bucket later loses if held, showing this is probabilistic revaluation rather than hindsight-perfect trading.

This is consistent with a systematic forecast-vintage update process.

---

# 1. ECMWF 18Z availability window

ECMWF's official dissemination schedule for the control forecast / formerly HRES states that the 18 UTC run publishes atmospheric fields progressively:

- steps 0–90 hourly: **23:45 → 00:12 UTC**;
- steps 93–144: **00:12 → 00:27 UTC**.

The next 00 UTC run does not begin atmospheric-field dissemination until about **05:45 UTC**.

Official ECMWF schedule:
https://www.ecmwf.int/en/forecasts/datasets/set-i

Therefore roughly **00:12–05:45 UTC** is a clean window in which a trader can act on the completed relevant early-horizon 18Z run while no 00Z successor is yet available.

For a T+0/T+1 Milan maximum, the relevant target hours are inside the 0–90h hourly tranche.

---

# 2. June 25 — supplied wallet exits 33°C

Struct preserved a live market snapshot for:

**“Will the highest temperature in Milan be 33°C on June 25?”**

Market page:
https://explorer.struct.to/markets/highest-temperature-in-milan-on-june-25-2026-33c

Struct snapshot timestamp:

- **June 25, 2026, 03:36 UTC**.

The supplied wallet's trade row was shown as approximately **“2h” old**:

- expression: 33°C YES;
- price: about **10.9¢**;
- shares: **-193.78**;
- value: about **$21.1**.

The negative share change means the wallet was selling/reducing the 33°C position.

Because Struct's UI age is rounded/coarse, the exact fill timestamp is not recovered from this page. The useful bound is approximately the **01–02 UTC region**, i.e. after the ECMWF 18Z early-step fields had completed around 00:12 UTC and long before the 00Z run became available.

## Outcome

The June 25 Milan event eventually resolved:

- **35°C = YES**;
- 33°C = NO.

So reducing 33°C was directionally correct relative to settlement.

## Specialist disagreement

In the same Struct live snapshot, other weather specialists/traders were still making small 33°C YES purchases around 11–12¢, including:

- `opopv.`;
- `Poligarch`;
- other accounts.

The supplied wallet's reduction was much larger than several of those individual contrary buys.

This is why simple wallet vote-count consensus is inferior to tracking:

`direction × normalized size × skill × freshness × entry-vs-exit state`.

---

# 3. June 29 — supplied wallet buys June 30 35°C

Recovered exact Polygon transaction:

`0xb8499e6f5331322f90a4d2245d3485085a838f67c8903eb9d1120be52c4f67b6`

Market:

**Milan June 30 — 35°C YES**.

Exact fill timestamp:

- **2026-06-29 01:55:11 UTC**;
- **03:55 Europe/Rome**.

Execution:

- 102.116 YES shares;
- $30.00 base consideration;
- raw price ≈ **29.38¢**;
- fee ≈ **$1.0593**;
- effective all-in price ≈ **30.42¢**.

## Information timing

The relevant June 28 ECMWF 18Z early-step fields completed dissemination around **00:12 UTC**.

The wallet bought at **01:55 UTC**, roughly **1h43m after** that completion.

The next 00Z run was not yet available.

## Outcome

Milan June 30 resolved:

- **34°C = YES**;
- 35°C = NO.

So the purchase would lose if held unchanged to settlement.

This is economically useful evidence because it shows the behavior is not a hidden deterministic resolver trick. It is a real probability view that can be wrong.

The remaining missing link is whether the wallet later reduced/exited after subsequent model revisions shifted mass toward 34°C.

---

# 4. Why the repeated timing matters

Two independent Milan actions now share the same structure:

| Date/action | Approx trade time UTC | Time after 18Z early fields complete | Direction |
|---|---:|---:|---|
| Jun 25 33°C | ~01–02 UTC, coarse Struct age | ~1–2h | **SELL / reduce** |
| Jun 29 35°C for Jun30 | 01:55:11 exact | 1h43m | **BUY** |

The directions differ. That weakens a trivial explanation such as:

> “the wallet automatically buys Milan every night around 2 UTC.”

A more plausible working hypothesis is:

> **After a fresh model cycle becomes available, the wallet recomputes a Milan probability distribution and trades the change in fair value.**

This is exactly the behavior a simple profitable system should test.

---

# 5. Why ECMWF 18Z is currently the leading clock hypothesis

At ~01–02 UTC:

- ECMWF 18Z relevant hourly fields are complete;
- ECMWF 00Z fields are not yet available;
- ItaliaMeteo ICON-2I itself has 00/12 UTC base cycles, but no public evidence recovered here shows that the 00Z ICON-2I run is already available by 01–02 UTC;
- ICON-2I uses ECMWF boundary conditions and runs operationally twice daily.

Therefore ECMWF 18Z is the strongest identified fresh global information event aligned with both recovered actions.

This remains a hypothesis, not a claim that the wallet literally consumes ECMWF directly. It could consume an aggregator or another product reflecting the same cycle.

The profitable test is source-agnostic:

`Does a new 18Z-derived probability surface predict the wallet's direction and subsequent market markout?`

---

# 6. Exact minimal event-study design

For every Milan daily-high event in the supplied wallet history:

## Forecast snapshots

Reconstruct:

- ECMWF 12Z;
- ECMWF 18Z;
- next ECMWF 00Z;
- ICON-2I latest legitimately available run;
- market probability surface immediately before/after.

For each run calculate the resolver-aligned daily maximum probability vector:

`q_old`

`q_new`.

Forecast revision:

`Δq_i = q_new_i - q_old_i`.

## Wallet action

For each fill around 00:12–05:45 UTC:

- BUY / SELL;
- bucket;
- raw price;
- dollars;
- normalized size relative to wallet baseline tier;
- minutes since 18Z completion.

## Market response

Measure token markout:

- +5m;
- +30m;
- +2h;
- until next model cycle;
- settlement.

---

# 7. The direct hypothesis to test

For wallet trade direction `s_i ∈ {+1,-1}`:

`alignment = s_i * Δq_i`.

If the wallet is reacting to forecast revisions, `alignment` should be positive more often/more strongly than chance.

Then test whether the wallet is **early**:

`markout_τ = s_i * (p_{t+τ} - p_t)`.

The high-value result is:

- positive `alignment` with the newest run;
- positive 30m/2h markout;
- strongest effect in 00:12–03:00 UTC fills.

That would directly establish a replicable source/timing edge.

---

# 8. Expand only after Milan

Do not build a giant global release-calendar model before this simple case is measured.

If Milan confirms the 18Z-revision mechanism, replicate the same study on European cities the supplied wallet trades:

- Paris;
- Madrid;
- Amsterdam;
- Munich;
- Warsaw;
- possibly Istanbul depending source coverage.

The forecast model can remain city-specific while the timing logic is shared.

---

# 9. Potential production implication if confirmed

A very simple live loop could wake around the relevant release, rather than continuously compute expensive forecasts:

1. load previous fair ladder;
2. fetch completed new 18Z-derived forecast inputs;
3. recompute `q_i`;
4. calculate `Δq_i` and current executable EV;
5. cross immediately when the revision creates large decaying edge;
6. otherwise quote passively if the edge is stable.

The recovered wallet's apparent 1–2 hour reaction window would imply this is **not necessarily a millisecond latency strategy**.

If market event studies show useful edge persists tens of minutes or more, implementation can stay extremely simple.

---

# Bottom line

The best recovered wallet-timing evidence now points to one concrete mechanism:

> **Milan probability revaluation after the ECMWF 18Z overnight forecast cycle.**

One recovered action sells a bucket that later loses; another opens a different next-day bucket at the same post-release clock and later loses if held. The combination is exactly what a probabilistic revision strategy should look like: update the distribution, trade whichever side the new information favors, accept that individual forecasts can still be wrong.

The highest-value next data task is not more broad weather research. It is to recover additional European wallet fills around **00:12–03:00 UTC** and test whether direction matches the new-vs-old forecast probability revision.