# Fastest path to live Weather PnL — PolyRust integration audit

Snapshot: **2026-08-13**

## Verdict

Do **not** wait for a full Rust implementation before trading the Weather edge.

The fastest economically correct path is:

1. **`polymarket-weather` remains the alpha/truth repository** — resolver mapping, weather-source timing, calibration, probability surfaces, historical reconstruction, specialist reverse engineering and profitability evidence.
2. **`polymarket-bot` becomes the first live Weather execution bridge** — it already has authenticated Polymarket V2 signing, FOK execution, batch submission, unwind logic and a live public market WebSocket order-book implementation.
3. **`Polyrustbot` remains the destination hot engine** — once faster weather feeds reduce the information window enough that local tail latency, maker cancel/replace races, queue position and multi-market coordination materially affect realized PnL.

This is not a language preference. It follows the measured latency budget.

The live NYC Aug 12 experiment measured:

- NOAA station-TXT source delay from nominal observation time: about **211 seconds** to our collector's first-seen clock;
- after that actual source-first-seen timestamp, several economically relevant CLOB sides remained stale/old for roughly **20–27 seconds**;
- an observed complementary 86–87°F NO fill at **47¢** marked **55.5¢** roughly 18 seconds later.

A ground-up Rust build cannot recover the 211 seconds currently lost upstream. A small TypeScript hot path can comfortably test whether the 20–27 second residual window converts into realized money while the faster weather source work proceeds.

## What already exists

### `polymarket-weather`

Strengths:

- resolver/station mapping;
- T+0 running-extreme and next-threshold logic;
- T+1 model-vintage research;
- live source-first-seen versus CLOB-reprice evidence;
- full-ladder/NegRisk economics;
- maker/taker routing math;
- specialist-maker/taker transaction evidence;
- exact fee-aware profitability research.

Missing for production:

- authenticated order placement;
- resident authenticated user/order state;
- maker quote lifecycle;
- cancel/replace path;
- order heartbeat/dead-man;
- one continuously running live event loop.

Do not turn this repository into a second exchange engine. Export the alpha invariants and live weather state needed by the execution process.

### `polymarket-bot`

Already implemented:

- `@polymarket/clob-client-v2` authenticated client;
- signer + credentials + funder/signature configuration;
- exact FOK buy execution;
- batch FOK submission;
- incomplete-basket unwind/reconciliation concepts;
- fee/tick/NegRisk-aware execution metadata;
- live market WebSocket;
- incremental in-memory per-token order books;
- active live-trading configuration path.

Money-relevant defects for Weather latency trading:

1. current `executeFokBuy()` re-fetches the book and fee model over REST immediately before signing;
2. the real-time calendar live path queries database risk and writes a durable row before submission;
3. current order-book representation reconstructs/sorts arrays for depth queries;
4. inspected execution code is FOK-centric and lacks the required Weather maker GTC/post-only quote lifecycle;
5. no authenticated user WebSocket was found in the current repo audit;
6. no exchange open-order heartbeat/dead-man loop was found; the existing `PING` is only the market-WebSocket keepalive.

For the first Weather live lane, fix only 1, 2, 4, 5 and 6. Number 3 can wait unless profiling shows it consumes meaningful parts of the measured edge window.

### `Polyrustbot`

Current state is **design only**.

The design is highly compatible with the Weather mechanism:

`external weather event -> resident state update -> affected ladder recompute -> capital reservation -> maker/taker intent -> sign -> warm CLOB submission`

Relevant planned primitives already match Weather exactly:

- external reference-feed adapters;
- source + local receive timestamps;
- resident market books;
- dependency routing;
- maker/taker strategy intents;
- global inventory/capital authority;
- post-only maker orders;
- cancel/replace;
- FOK/FAK;
- user stream;
- order heartbeat;
- async downstream persistence;
- precise latency instrumentation.

The only strategic change is **priority**: Weather now has stronger direct live lead/lag evidence than the original crypto-first design had when PolyRust was written.

## Does the Weather mechanism need Rust?

### No, for first live validation

Current measured opportunity window after our actual source arrival is on the order of tens of seconds in the strongest live case.

A small event-driven TypeScript process using:

- direct weather feed;
- resident Polymarket WebSocket books;
- resident fee/tick metadata;
- preinitialized signer/client;
- no hot-path database/REST calls;

should be capable of acting well inside that window.

The much larger current latency loss is weather dissemination, not JavaScript runtime.

### Yes, potentially, after the source is improved

Rust becomes economically important if measurement shows one or more of:

- one-minute/five-minute direct weather feeds reach us materially earlier and CLOB reaction compresses into sub-second/few-second windows;
- maker profitability depends on cancel/reprice races after every observation update;
- queue position from faster quote replacement affects fill-conditioned markout;
- the bot continuously makes both sides across many cities and bucket ladders;
- source bursts require updating many related YES/NO markets in one event;
- TypeScript p99/p99.9 event-to-wire latency or GC pauses cause measurable lost fills/adverse selection;
- global Weather + crypto + structural inventory needs one resident capital authority.

Only then does the Rust rewrite directly increase expected net income.

## Immediate live architecture

One **dedicated TypeScript process** is enough for the first lane.

### Slow/control plane

At startup and periodically:

- discover active Weather events;
- resolve station/source/rules;
- resolve explicit YES/NO token labels;
- load condition IDs, token IDs, tick sizes, minimum sizes, fee parameters and NegRisk metadata;
- choose events/cities with usable source feeds and liquidity.

This path may use Gamma/Data/REST. It must not sit between a weather update and an order.

### Hot state

Keep resident:

- active event metadata;
- both YES and NO books for every selected bucket;
- fee/tick/min-size/NegRisk metadata;
- current orders and positions;
- source valid time;
- source first-seen monotonic time;
- running resolver-aligned extreme;
- current probability vector `q` or compact hazard state;
- latest strategy generation/version.

### Hot event path

`weather message received`

`-> parse exact station state`

`-> update running max/min and threshold state`

`-> recompute affected bucket q values`

`-> cancel now-bad maker quotes`

`-> compare resident executable prices with q`

`-> choose maker/post-only or immediate FOK/FAK`

`-> sign using resident client`

`-> submit on warm connection`

`-> journal asynchronously`

No Gamma, Data API, fresh book REST fetch, database query or disk write belongs between source receive and submission.

## First live strategy lane

Do not begin with a full weather forecasting platform.

Start with **T+0 resolver observation repricing** because it has direct live evidence.

### State

For each active event:

- exact resolver station;
- running maximum/minimum;
- current bucket;
- next threshold distance;
- local time / remaining peak window;
- compact probability vector or next-threshold hazard;
- all YES/NO books.

### Execution router

1. **Hard elimination**
   - if an observation makes a bucket impossible, value it at ~0 subject to resolver/source semantics;
   - cross only if actual remaining executable price exceeds fees/spread enough to matter;
   - otherwise use the information to cancel maker bids and reallocate quotes.

2. **Probability redistribution**
   - when the observation changes survival/next-threshold probabilities without certainty, update the whole ladder;
   - prefer passive complementary liquidity when spread is wide and expected fill-conditioned markout is positive;
   - cross only where `q - all_in_ask` or `net_bid - q` is materially positive at actual depth.

3. **Quiet state**
   - quote passively around fair `q` only where expected spread/rebate exceeds fill-conditioned adverse selection.

The London/NYC live evidence argues for this state-dependent maker/taker router rather than a pure taker bot.

## Minimum TypeScript changes before real Weather orders

### A. Weather source adapter

Emit compact events with:

- station;
- report valid time;
- source first-seen monotonic timestamp;
- precise temperature/extreme fields;
- raw/source version when needed for audit.

First source priority remains faster US ASOS/MADIS distribution; NOAA station TXT is a baseline/verification feed.

### B. Weather universe + ladder map

Reuse Gamma/CLOB discovery off the hot path.

Store explicit token labels. Never infer YES/NO from primary/secondary token ordering.

### C. Both sides of the ladder on market WebSocket

Subscribe all selected YES and NO token IDs.

The live NYC case demonstrated that a favorable short view can express through complementary NO; YES-only state is insufficient.

### D. Resident executable economics

Add functions equivalent to:

- `quoteBuySharesExactResident()`;
- `quoteSellSharesExactResident()`;
- `executeFokFromResidentState()`;
- `executeFakFromResidentState()` when partial immediate size is profitable.

Do not call `getOrderBook()` or fee endpoints on the event-to-order path.

### E. Maker order lifecycle

Add only:

- GTC/GTD post-only placement;
- cancel one / batch cancel;
- replace desired quote;
- local order generation/version;
- immediate withdrawal when source state becomes stale or q changes materially.

### F. Authenticated user stream

Use it as normal fast truth for:

- placement;
- partial/full fills;
- cancellation;
- trade state changes.

REST becomes reconnect/reconciliation, not ordinary hot-path state.

### G. Exchange order heartbeat

For resting Weather maker orders, use the CLOB heartbeat/dead-man mechanism so a dead process does not leave stale quotes exposed.

### H. Latency/PnL record

For every signal/order/fill persist after the hot decision:

- source valid time;
- source first-seen;
- q before/after;
- book generation used;
- decision time;
- sign start/end;
- submission start/response;
- user-stream placement/fill/cancel;
- intended/realized maker/taker role;
- fee/rebate;
- 5s/30s/5m markout;
- final PnL.

This is the evidence needed to decide when Rust earns its cost.

## Rust migration trigger

Do not set a language-based milestone. Set an economic one.

Move the hot Weather lane into PolyRust when live evidence shows:

`expected dollars recovered by lower local latency / better cancel-fill behavior > cost of delayed strategy iteration and migration`

Practical measurable triggers include:

- TypeScript p99 source-event -> request-write is a meaningful fraction of observed stale-window duration;
- a material fraction of lost opportunities disappear between TypeScript decision and actual submission;
- maker adverse-selection loss is concentrated in TypeScript cancel latency;
- queue-position/fill probability improves materially with faster replace timing;
- simultaneous city/ladder load creates measurable stale-state decisions.

Until one of those is true, source quality and strategy calibration have higher expected value.

## Cross-repo ownership

### `polymarket-weather`

Own:

- research;
- resolver/source maps;
- calibration/model coefficients;
- historical evidence;
- point-in-time data tools;
- strategy economics.

Do not own production wallet/order state.

### `polymarket-bot`

Own **temporary first production Weather lane**:

- live weather-source adapter;
- market/user WebSockets;
- resident books;
- current orders/positions;
- maker/taker router;
- signing/submission;
- live latency and PnL evidence.

Do not duplicate broad weather research.

### `Polyrustbot`

Own eventual shared production money path:

- normalized hot feeds;
- resident exact books;
- global capital/inventory;
- maker/taker intents;
- signing/execution;
- order lifecycle;
- cross-strategy coordination.

Weather then becomes one strategy/reference adapter inside the same engine, not a separate wallet/process forever.

## Profit-ranked next actions

1. **Connect a faster US weather source and measure source-first-seen against the same CLOB timeline.** This attacks the current ~211-second upstream loss.
2. **Add a minimal Weather lane to the existing TypeScript execution bot with resident books and no hot-path REST/DB.** This gets real fill/markout evidence fastest.
3. **Implement post-only maker + cancel/replace + user stream + exchange heartbeat.** The strongest live observed fill economics were maker-like.
4. **Run the lane on one/few high-quality events, recording actual realized maker/taker PnL and latency.**
5. **Only then decide whether to port the hot lane to Rust.** The migration decision should be based on lost-dollar attribution, not aesthetics.

## Bottom line

The repositories are complementary rather than competing:

> **Weather has the alpha. The existing TypeScript bot has the fastest bridge to real orders. PolyRust is the eventual execution fabric when measured local latency becomes expensive enough to justify it.**

Going live fastest therefore means **reuse before rewrite**.