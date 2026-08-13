# Weather market opening — hypothesis finalization

Snapshot: **2026-08-13**

## Verdict

Market opening is the cheapest recurring hypothesis to finalize because the required fair-value model can exist before the market is created.

The final research question is:

> When a recurring Weather ladder is first listed, does its first executable market state take measurable time to incorporate weather information that was already public before listing?

This must be answered using the first order-book state, not UI probabilities or later historical midpoints.

---

## 1. Pre-list fair value is the benchmark

For expected city/date ladder `d`, construct before listing:

`q_pre,d = (q_1, ..., q_n)`

with:

`sum_i q_i = 1`.

Only information available before the eventual market creation timestamp may enter `q_pre`:

- model vintages already public;
- station calibration;
- resolver rules;
- observations already available;
- AIFS/other early guidance if its first-seen time is valid.

Freeze that vector and its input vintages before observing the opening market.

The research then compares the opening book with a genuinely ex-ante probability surface.

---

## 2. Market creation discovery has a documentation ambiguity

Polymarket's market WebSocket currently documents a `new_market` event when custom features are enabled. However, the same subscription examples require one or more known token IDs.

Official source:

- https://docs.polymarket.com/market-data/websocket/market-channel

Therefore the documentation does **not** by itself prove that `new_market` acts as a global market-discovery broadcast on an otherwise unscoped connection.

This should be tested experimentally rather than assumed.

For robust research discovery, Polymarket also exposes stable keyset market/event pagination with creation timestamps and market metadata:

- https://docs.polymarket.com/api-reference/markets/list-markets-keyset-pagination
- https://docs.polymarket.com/api-reference/events/list-events-keyset-pagination

A narrow Weather/category/date discovery process is sufficient for this hypothesis because the expected market family/date is known in advance. There is no need for broad universe polling.

---

## 3. Historical screening versus prospective proof

Historical data can provide:

- creation timestamp;
- first trade timestamp;
- early price history;
- subsequent convergence path;
- final resolver outcome.

But historical price history cannot recreate the exact first resting bids/asks or quote queue.

Therefore use historical opening studies only to identify whether large early moves are common.

Prospective evidence requires capturing:

- first known token IDs;
- first complete relevant book state;
- first trade;
- subsequent bid/ask/depth changes;
- any new weather/model information after listing.

---

## 4. Do not mistake Polymarket display behavior for probability incoherence

Polymarket documents that the displayed probability is normally the bid/ask midpoint, but if the spread exceeds `$0.10`, the UI may display the last trade instead.

Official source:

- https://docs.polymarket.com/concepts/prices-orderbook

Thus a newly opened ladder can visually sum to far more or less than 100% without presenting an executable inconsistency.

All opening research should use actual bid/ask/depth.

---

## 5. Cold-start error decomposition

For bucket `i` at time `t` after creation:

`e_i(t) = p_market,i(t) - q_pre,i`.

But observed price changes after listing can arise from two sources:

`market move = convergence to old information + response to new post-list information`.

The research must timestamp every new forecast/observation release after listing and censor or explicitly model those intervals.

The cleanest openings are those where no major weather information arrives during the first convergence window.

A simple descriptive model is:

`e_i(t) ~= e_i(0) * exp(-lambda_i t)`

until new information arrives.

The relevant quantity is the distribution of error magnitude and convergence half-life by city/bucket/spread/liquidity.

---

## 6. Whole-ladder coherence

Because exactly one bucket wins, a calibrated fair-value vector should sum to one.

Opening books can be tested for several forms of incoherence:

### Individual valuation error

Compare each executable side to `q_pre,i`.

### Distribution-shape error

Compare implied modal bucket, width and tail mass against `q_pre`.

### Neighbor inconsistency

If adjacent buckets are misordered relative to a smooth resolver distribution, estimate whether the discrepancy survives actual spreads/depth.

### Complete-set economics

Keep structural YES/NO and NegRisk identities separate from forecast valuation. A distribution that looks incoherent at UI prices may not offer a fillable complete-set inconsistency.

---

## 7. Maker-specific research question

Opening periods may have fewer competing makers and wider spreads, but that does not imply profitable passive fills.

For every prospectively observed opening quote opportunity measure:

- whether the quote would have been filled;
- subsequent probability/market markout conditional on that fill;
- whether the fill occurred immediately before new information;
- realized/available maker incentives separately from valuation movement.

Current Polymarket documentation states Weather makers pay zero platform fee and can participate in the Weather maker rebate program.

Official sources:

- https://docs.polymarket.com/trading/fees
- https://docs.polymarket.com/market-makers/maker-rebates

Do not attribute rebate economics to forecast skill.

---

## 8. Decisive prospective sample

For each recurring daily-temperature listing:

### Before listing

- expected city/date;
- resolver mapping;
- frozen `q_pre` vector;
- input model/source vintages and first-seen times.

### At first discovery

- event/condition/token IDs;
- `createdAt`;
- first locally seen time;
- first available complete book;
- first trade.

### After discovery

Record book/price path at dense early intervals and every information update.

The research output per event is:

- initial executable discrepancy versus `q_pre`;
- convergence time;
- whether new weather information intervened;
- fill-conditioned markout for any passive candidate;
- later resolver result.

---

## 9. Falsification / downgrade criteria

Downgrade the opening thesis if:

1. first executable books are already close to `q_pre` within forecast-calibration error;
2. large apparent errors exist only in UI/last-trade displays rather than executable books;
3. convergence happens before reliable market discovery can observe it;
4. early moves are mostly caused by new post-list forecast updates, not discovery of old information;
5. passive fills are systematically adverse despite attractive initial spreads;
6. opening depth is too small to matter economically.

---

## 10. Final research deliverable

This hypothesis is finalized when the repository has a prospective sample of new Weather listings with frozen pre-list probability surfaces, first-book captures and information-timestamp attribution.

The decisive result is the joint distribution of:

`opening executable error x persistence x available depth x fill-conditioned markout`.

If those terms are repeatedly nontrivial, opening price discovery becomes a distinct recurring Weather mechanism rather than an anecdotal market-formation effect.