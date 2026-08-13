# Weather market-opening probability discovery — deep dive

Snapshot: **2026-08-13**

## Verdict

Market opening is one of the cheapest recurring Weather inefficiencies to test because the information may already exist **before the contract exists**.

The strongest formulation is not “new markets have bad displayed probabilities.” Displayed prices can be stale last trades when spreads exceed 10 cents and therefore are not executable.

The economically serious hypothesis is:

> Maintain a resolver-calibrated fair probability surface before recurring Weather markets list. When the new ladder appears, test whether executable bids/asks converge slowly toward information that was already public, and whether passive fills earn positive fill-conditioned markout after fees/rebates.

This requires almost no additional meteorology beyond the existing fair-value engine.

Official Polymarket mechanics:

- displayed price is midpoint when spread is <= $0.10, otherwise last trade is displayed;
- buying executes against the ask and selling against the bid;
- Weather taker fee is `0.05*p*(1-p)` per share;
- makers pay zero platform trading fee and Weather receives a 25% share of the eligible taker-fee pool through the maker-rebate program.

Sources:

- https://docs.polymarket.com/concepts/prices-orderbook
- https://docs.polymarket.com/trading/fees
- https://docs.polymarket.com/market-makers/maker-rebates

---

## 1. Pre-list fair value is the key asset

For an expected city/date event, maintain before listing:

`q_pre(i) = P(final resolver outcome = bucket i | information available now)`.

The vector must satisfy:

`q_pre(i) >= 0`

and

`sum_i q_pre(i) = 1`.

For daily temperature this already comes from:

- exact resolver station;
- calibrated model/ensemble daily maximum;
- station-specific residual distribution;
- latest observations;
- latest forecast revisions.

The event listing should therefore be viewed as a **market-data event**, not the start of weather research.

---

## 2. Why opening can be structurally inefficient

New ladders have no established internal reference price.

Possible causes of temporary executable mispricing:

- first quotes use generic city forecasts rather than resolver-station calibration;
- individual buckets are seeded independently instead of as one coherent distribution;
- early spreads are wide because few makers are present;
- the latest forecast cycle existed before listing but early quotes reflect an older weather state;
- modal probability moves while tails remain stale;
- a replacement/new strike ladder appears after the forecast regime has already changed.

The mechanism is **cold-start price discovery of old public information**.

This is distinct from forecast-release latency, where new information arrives after the market already exists.

---

## 3. Opening screenshots can be highly misleading

Polymarket documents that if the spread is wider than $0.10, the site displays the **last traded price** instead of midpoint.

Therefore a ladder can visually sum to 150%, 200% or more without offering any simultaneous executable arbitrage.

The required state is always:

- best bid;
- best ask;
- depth;
- last trade;
- spread;
- timestamp.

For exact mutually exclusive outcomes, displayed-probability incoherence is only a **screening signal for weak price discovery**.

It becomes economic evidence only after using actual executable books.

---

## 4. Taker economics

For YES bucket `i` with fair probability `q_i` and executable ask `a_i`:

`fee_i = 0.05 * a_i * (1-a_i)`

`cost_i = a_i + fee_i`

`EV_taker_i = q_i - cost_i`.

For depth `x`, replace single-price cost with the depth-weighted average across asks and apply fees per fill price.

A taker opportunity exists only if the fair-value discrepancy survives actual spread/depth/fees.

At opening, wide spreads mean visually large disagreement can still have **negative** taker EV.

---

## 5. Maker economics are more interesting

Suppose a passive YES bid at price `p` is filled.

The unconditional spread is irrelevant. The right object is:

`EV_maker(p,h) = P(fill) * [E(q(t+h) - p | fill) + rebate_per_share - inventory_cost]`.

The central statistic is:

`fill_conditioned_markout_h = E(q(t+h) - p | fill)`.

Why condition on fill?

Because fills are not random. If informed traders only hit the quote when our fair probability is about to fall, a large posted spread can still lose money.

At opening, favorable maker economics require some combination of:

- wide spread;
- weak competitor depth;
- sufficiently accurate pre-list q;
- fills driven by uninformed/cold-start flow rather than fresh information;
- rebate that improves already-positive economics rather than rescuing toxic quotes.

This is the strongest reason to collect production-fidelity opening L2/fill data.

---

## 6. A natural opening convergence model

Let normalized executable market probability estimate at time `t` be `m_i(t)`.

Define opening residual:

`e_i(t) = m_i(t) - q_pre(i)`.

If there is no new weather information after listing, a simple convergence model is:

`e_i(t) = e_i(0) * exp(-lambda_i t) + noise`.

Half-life:

`t_half_i = ln(2)/lambda_i`.

Estimate half-life by:

- city;
- bucket rank;
- spread;
- event volume class;
- opening hour;
- forecast age;
- number/size of early makers.

The profit opportunity depends not only on initial error but on whether `t_half` is long relative to order placement/fill time.

---

## 7. Separate old-information convergence from new weather

This is crucial.

Suppose the market opens at `t0` and moves over the next hour. A new ECMWF/model run arriving at `t0+20m` could explain the move.

To call the first 20 minutes an opening inefficiency, freeze the fair surface at listing:

`q_pre = q(t0-)`.

Then construct a second time-varying fair surface `q_live(t)` using post-list information.

Decompose market price movement into:

`market_move = convergence_to_q_pre + response_to_new_information + residual`.

A practical regression is:

`Delta m_i = beta1*(q_pre_i - m_i) + beta2*Delta q_live_i + epsilon`.

Positive `beta1` after controlling for `Delta q_live` supports genuine old-information price discovery.

---

## 8. Existing Weather listings make this measurable every day

Prior repo research found established London daily-high markets opening roughly two days before the target date and later reaching six-figure event volume.

That gives a recurring experiment:

1. create q for expected future date before the event is listed;
2. timestamp the actual market creation;
3. capture the first complete ladder state;
4. continue L2 for the first hours;
5. distinguish convergence from new forecast releases.

A few weeks can produce dozens of city/date opening events without waiting for settlement to evaluate short-horizon markout.

---

## 9. Snow demonstrates why pre-list state matters

The January 24–26 NYC snowfall ladder was created January 21 at 2:12 PM ET.

NWS discussion earlier that day had already increased snow probabilities and described improving model agreement.

Therefore a serious snow model could have formed a probability distribution **before the Polymarket ladder existed**.

A separate February snow ladder indexed at very low early volume showed extreme displayed probability incoherence and very wide asks, then rapidly concentrated probability into the upper tail.

The correct interpretation is:

- initial price discovery was visibly immature;
- no immediate taker-arbitrage conclusion follows from displayed probabilities;
- a precomputed fair distribution would have been valuable for evaluating the first actual bids/asks.

This makes snowfall an especially attractive market-opening case study because the weather state can change enough that newly selected strikes themselves reveal the organizer's regime assumptions.

---

## 10. Ladder coherence gives extra diagnostics

For exact mutually exclusive buckets, fair probabilities sum to one.

Normalize an executable/reference market vector only for diagnosis:

`m_norm_i = m_i / sum_j m_j`.

Then compare cumulative distributions:

`CDF_q(k) = sum_{i<=k} q_i`

`CDF_m(k) = sum_{i<=k} m_norm_i`.

A systematic horizontal shift between CDFs is more interpretable than independent bucket errors:

- market hotter than model;
- market colder than model;
- market too dispersed;
- market too concentrated.

For temperature/snow ladders this can reveal one simple miscalibration rather than seven unrelated bets.

---

## 11. Temporal complete-set interaction

Existing repo research identified a binary mechanism where complementary YES/NO inventory acquired at different times can later be merged to $1 if combined basis is below $1.

Opening periods with wide spreads and volatile probability discovery may create more opportunities for complementary inventory to be acquired on different sides over time.

This should be measured separately from directional forecast edge:

`pair_locked_value = 1 - cost_yes_lot - cost_no_lot`.

Do not mix this mechanical source of PnL with weather calibration when evaluating the opening strategy.

---

## 12. Smallest decisive dataset

For each of 30–100 opening events:

- expected event/city/date;
- `q_pre` vector with version timestamp;
- market creation timestamp;
- token IDs and explicit outcome labels;
- first L2 state;
- all L2 changes for first 2h;
- first trades/fills;
- new weather information timestamps;
- updated `q_live`;
- 5s/30s/5m/30m markout;
- eventual resolver result.

Primary statistics:

1. median absolute executable opening error;
2. convergence half-life after controlling for new weather;
3. maker fill probability by quote distance;
4. fill-conditioned markout;
5. taker edge actually available at depth;
6. rebate contribution separated from valuation PnL.

## Bottom line

Market opening is attractive because it requires almost no new forecasting machinery. The research question is simply whether a mature resolver probability estimate can arrive **before** a newly created Polymarket ladder has completed price discovery.

If yes, it is a highly recurring complement to forecast-release and observation-latency alpha. If not, the test is cheap and can be rejected quickly.
