## ADDED Requirements

### Requirement: Multiple Moving Averages
The system MUST support configuring multiple MA periods.

#### Scenario: Config
- **WHEN** `strategy.ma_list` is set to `[20, 60, 120]`
- **THEN** lines for MA20, MA60, MA120 should be calculated and plotted.

### Requirement: BIAS Subplot
The system MUST support an optional BIAS subplot.

#### Scenario: Display
- **WHEN** `plot.show_bias` is `true`
- **THEN** a separate subplot should render BIAS lines (e.g., BIAS-20, BIAS-60).
