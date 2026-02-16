## Why

User wants to objectively verify a "Strict MA20 Inflection" trading strategy.
The system needs a backtesting capability that outputs high-definition, interactive reports in Chinese to assist decision making.

## What Changes

We will introduce a new backtesting module `analysis/indices_dashboard/backtest.py` that:
1.  **Implements Strategy**: Buys when MA20 slope turns positive (strictly `MA20[t] > MA20[t-1]`), sells when it turns negative.
2.  **Simulates Trading**: Tracks cash and holdings, accounting for a 1.5% commission if held for less than 7 days.
3.  **Generates Report**: Outputs a `backtest_report.html` using `plotly` with **Chinese language support**.

## Capabilities

### New Capabilities
- `backtesting-engine`: A lightweight framework for simulating trades based on technical indicators.
- `ma20-strategy`: Specific implementation of the strict MA20 inflection strategy.
- `interactive-reporting-zh`: Generation of interactive HTML reports in Chinese.

## Impact

- [NEW] `analysis/indices_dashboard/backtest.py`: Core logic.
- [MODIFY] `requirements.txt`: Add `plotly`.
