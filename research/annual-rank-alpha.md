# Annual GISTEMP rank alpha — reuse monthly distributions at larger capacity

Snapshot: **2026-08-11**

Purpose: extend the monthly GISTEMP replica into Polymarket's annual hottest-year rank market **without creating a separate climate model**.

The current 2026 annual-rank event has about **$3.21M** in event volume and six mutually exclusive outcomes. One of the largest WEATHER-category specialists, `gopfan2`, holds roughly **91.7k YES shares** of second-hottest 2026 at an average entry around **29.3¢** in the indexed profile snapshot.

This is exactly the type of high-capacity contract that should consume the monthly climate distribution as an input.

---

# 1. Exact settlement rule

Polymarket event:

https://polymarket.com/event/where-will-2026-rank-among-the-hottest-years-on-record

The contract ranks 2026 against all other years in descending order of NASA GISTEMP global Land-Ocean Temperature Index.

Primary resolution source:

NASA's **Land-Ocean Temperature Index (C)** graph data, column `No_Smoothing`, row `2026`.

The rules state:

- hottest year = rank 1;
- second hottest = rank 2, etc.;
- ties resolve according to the place occupied by the year tied with;
- resolve immediately once the specified data becomes available;
- later revisions are ignored.

This is again a **first-release-vintage contract**.

---

# 2. NASA annual mean calculation is simple

NASA's published GISTEMP source documentation states:

> **Annual series are computed from their monthly counterparts. Each month is weighted equally.**

Official source:
https://data.giss.nasa.gov/gistemp/sources/gistemp.html

Therefore for the annual vintage used at resolution:

`A_2026 = (M_Jan + M_Feb + ... + M_Dec) / 12`.

No annual climate model is required.

---

# 3. Important vintage distinction

Do **not** calculate the annual contract from the monthly Polymarket settlement values alone.

Monthly Polymarket contracts freeze the **first monthly GISTEMP publication**.

The annual 2026 rank will be based on the annual GISTEMP value first published after the year ends. At that time NASA may have incorporated late reports and corrections that revised earlier 2026 monthly values.

So for month `m`:

`M_m^annual_vintage = M_m^first_release + revision_m`.

Then:

`A_2026^first_annual = mean(M_m^first_release + revision_m)`.

The revision term is usually small but cannot be ignored when annual rank gaps are only a few hundredths of a degree.

---

# 4. Monthly uncertainty shrinks by 12 in the annual mean

A monthly error of `δ` changes the annual average by:

`δ / 12`.

Examples:

- 0.01°C monthly error → **0.00083°C** annual error;
- 0.05°C monthly error → **0.00417°C** annual error;
- 0.10°C monthly error → **0.00833°C** annual error.

This is economically attractive.

Even if an individual monthly bracket remains uncertain by 0.05°C, its contribution to annual-rank uncertainty is only about four thousandths of a degree.

As more months become observed, annual-rank variance collapses rapidly.

---

# 5. Minimal annual distribution

At date `t`, split the year into:

- months already published;
- current month partial/near-complete;
- future months.

For already published months, use the **current estimate of what that month will look like at annual-release vintage**, not just first-release value.

For future months use a simple monthly anomaly distribution.

Then simulate/propagate:

`A_2026 = (Σ known/revised monthly values + Σ future monthly draws) / 12`.

Finally compare with competitor-year annual values at the anticipated resolution vintage.

The rank probabilities are:

`P(rank=1)`
`P(rank=2)`
`...`.

No separate classifier is needed.

---

# 6. Future-month model should remain simple

The annual market does not justify a large climate-model ensemble unless it materially changes rank probability.

For each remaining month use one of:

1. ERA5 / seasonal forecast anomaly distribution;
2. ECMWF seasonal global anomaly if available and demonstrably useful;
3. a historical ENSO/trend regression;
4. market-implied monthly GISTEMP distributions where active monthly contracts exist.

The last option is especially interesting because Polymarket itself may already encode specialist climate information.

A simple combined future-month distribution can be:

`q_month = λ * our_climate_estimate + (1-λ) * monthly_market_distribution`.

Again, fit `λ` only if it improves rank forecasting / PnL.

---

# 7. Cross-market consistency creates a free relative-value test

Monthly GISTEMP bracket markets and annual-rank markets share the same latent climate path.

Suppose the current annual-rank market implies:

- 55% rank 2;
- 40% rank 1;
- 5% all other ranks.

Meanwhile the next few monthly markets imply anomaly distributions that, when propagated through the annual mean, produce only:

- 25% rank 2;
- 70% rank 1;
- 5% others.

That inconsistency can be traded even without believing our weather model is superior.

The simplest structural calculation is:

`annual_rank_distribution_implied_by_monthly_markets`

versus

`direct_annual_rank_market_distribution`.

This is a climate version of full-ladder consistency.

---

# 8. The annual market should use updated historical comparator values

The contract compares 2026 with all previous GISTEMP years at resolution time.

NASA's historical series can itself be revised as late reports/corrections arrive.

Therefore store current comparator-year values and update them whenever NASA's GISTEMP files change.

The relevant thresholds are simply the top existing annual values:

`T_1 = hottest prior year`
`T_2 = second-hottest prior year`
`...`.

Then:

- rank 1 if `A_2026 > T_1`;
- rank 2 if `T_2 < A_2026 <= T_1` under the contract's tie convention;
- etc.

No historical climate simulation is required once those thresholds are read from NASA.

---

# 9. `gopfan2` demonstrates real dollar appetite

Indexed profile:

https://polymarket.com/profile/0xdd42ffb8aabe818f7538d93c175a9f9e2da9990d

Visible position:

- **Will 2026 be the second-hottest year on record? — YES**;
- average entry about **29.3¢**;
- approximately **91,697.5 shares**;
- raw cost around **$26.9k**;
- indexed mark around the mid-50¢ region;
- visible unrealized gain around **$22–25k** depending crawl.

The same account is the all-time WEATHER PnL leader in the current category snapshot.

This does not prove the annual position's final EV, but it demonstrates that specialist capital can be deployed at a scale far above a normal city-temperature bucket.

---

# 10. Annual rank can be updated after every monthly GISTEMP release

Each monthly publication creates a deterministic information event.

After month `m` is released:

1. replace its forecast distribution with the current GISTEMP estimate + revision distribution;
2. recompute annual mean distribution;
3. recompute rank probabilities;
4. compare with annual-rank prices;
5. trade only if the probability revision exceeds executable friction.

This creates 12 natural annual-market revaluation events per year, plus meaningful intra-month updates from ERA5T/ERSST/GHCN inputs.

---

# 11. Release-day direct-replica information improves annual rank too

The monthly replica from `gistemp-basis-alpha.md` has dual value.

If it predicts August GISTEMP before NASA releases it:

- trade the August bracket market;
- immediately propagate the same inferred August value into `A_2026`;
- trade annual rank if the direct rank market has not incorporated the implication.

One information acquisition can therefore generate **multiple correlated but distinct PnL opportunities**.

The correct allocation is by marginal expected dollars and shared outcome exposure, not by treating them as independent bets.

---

# 12. Monthly-to-annual sensitivity gives a fast screening rule

If the annual mean before month `m` is uncertain, a forecast revision `ΔM_m` changes the annual mean by:

`ΔA = ΔM_m / 12`.

So a +0.12°C revision in one month shifts the annual estimate only +0.01°C.

Before recalculating the whole rank distribution, a fast screen is:

`annual_shift ≈ monthly_revision / 12`.

If that cannot move meaningful probability across a historical rank threshold, skip the annual trade and focus on the monthly market.

This keeps annual execution sparse and high-value.

---

# 13. Potential source of underpricing: attention separation

Monthly GISTEMP traders and annual-rank traders may not be identical populations.

The annual event attracts broader climate/news narratives:

- El Niño headlines;
- scientist forecasts;
- record-year commentary.

The monthly contract is closer to a near-term data-release/basis problem.

If the monthly input pipeline is more precise than narrative annual traders, the cross-market propagation can create a persistent edge after monthly releases.

This is a hypothesis to test through price-response timing, not an assumption.

---

# 14. Minimal historical test

For each historical year where related monthly and annual-rank contracts exist:

1. reconstruct the monthly GISTEMP probability distributions through the year;
2. at each monthly release date calculate annual rank distribution using only information then available;
3. compare with direct annual market price;
4. measure 1d/1w markout and final settlement PnL.

For 2026, this can be recorded prospectively from now through January 2027 without any large historical archive.

---

# 15. Current strategy hierarchy

The climate engine should produce in this order:

### A. Monthly bracket fair value

Highest direct connection to the upstream GISTEMP replica.

### B. Annual rank fair value

Derived from the same monthly distributions.

### C. Hottest-month / record-month markets

Also derived from monthly distributions and historical monthly threshold values.

Only build a separate model if one of these contracts uses a fundamentally different resolver.

---

# Bottom line

Annual GISTEMP rank is a high-capacity **derived trade**, not a new forecasting problem.

NASA computes annual GISTEMP by equally weighting the 12 monthly values. A monthly replica/basis model can therefore produce annual-rank probabilities almost for free, with one added detail: model revisions between monthly first release and the annual-release vintage.

The current annual event has **~$3.21M volume**, and a leading WEATHER specialist has deployed tens of thousands of dollars into one rank outcome. That makes monthly→annual probability propagation one of the highest-value low-complexity extensions in the project.