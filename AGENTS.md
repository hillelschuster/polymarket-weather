# AGENTS.md — Profitability First

## Objective

The project exists to find and exploit repeatable, executable edge in Polymarket weather markets. The success metric is realized net PnL and bankroll compounding, not architectural elegance.

## Working rules

1. **Evidence over stories.** Separate verified facts, source claims, inference, and hypotheses.
2. **Executable EV over forecast vanity.** Optimize probability estimates for net trading returns after price, spread, fees, fill probability, and settlement mechanics.
3. **Settlement first.** Model the exact station/source/rules the contract settles on, not generic city weather.
4. **Simple before fancy.** Use the smallest method that captures the edge. Do not add frameworks, services, abstractions, mocks, or process ceremony without a demonstrated profit reason.
5. **Preserve promising edges.** Weak evidence changes confidence and sizing; it does not justify deleting a hypothesis before it has been measured properly.
6. **Point-in-time data only.** Never evaluate a trading idea with information unavailable when the trade would have been placed.
7. **Market data matters.** Midpoint is not executable price. Track bid/ask, depth, maker/taker economics, and cross-bucket consistency.
8. **Weather is probabilistic.** A point forecast is not a tradable probability distribution.
9. **Wallets are data.** Profitable public weather traders are signals to reverse-engineer, not personalities to imitate blindly.
10. **Research before code.** During the current phase, document the thesis and identify the minimum data needed to decide which edge deserves implementation.

## Current phase

Research only. Do not build the bot yet.
