## ADDED Requirements

### Requirement: Interactive Backtest Reporting (Chinese)
The system MUST generate an interactive HTML report for strategy backtests, fully localized in Chinese.

#### Scenario: Generate Report
- **WHEN** the backtest script is executed
- **THEN** it should produce a `.html` file containing an interactive Plotly chart.
- **AND** all labels, titles, and hover text MUST be in Chinese.
- **AND** the chart should display Buy/Sell signals clearly.

### Requirement: MA20 Strict Inflection Strategy
The system MUST implement a trading strategy based on the strict inflection of the 20-day Moving Average.

#### Scenario: Buy Signal
- **WHEN** `MA20[t] > MA20[t-1]` (Strictly rising)
- **AND** `MA20[t-1] <= MA20[t-2]` (Previously flat or falling)
- **THEN** a Buy signal is generated.

#### Scenario: Sell Signal
- **WHEN** `MA20[t] < MA20[t-1]` (Strictly falling)
- **AND** `MA20[t-1] >= MA20[t-2]` (Previously flat or rising)
- **THEN** a Sell signal is generated.

### Requirement: Commission Calculation
The system MUST apply commission rules based on holding duration.

#### Scenario: Short-term Holding
- **WHEN** a position is sold within 7 calendar days of buying
- **THEN** a 1.5% commission fee is deducted.

#### Scenario: Long-term Holding
- **WHEN** a position is sold after holding for 7 or more calendar days
- **THEN** no commission fee is applied.
