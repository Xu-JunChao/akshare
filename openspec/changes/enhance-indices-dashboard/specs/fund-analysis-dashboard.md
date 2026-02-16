## ADDED Requirements

### Requirement: Global Date Range Configuration
The system MUST allow configuring the analysis date range globally.

#### Scenario: Explicit Date Range
- **WHEN** the dashboard is run
- **THEN** it should use the globally configured `START_DATE` and `END_DATE` to filter data.
- **AND** if `END_DATE` is not provided, it should default to the current date.

### Requirement: BIAS Indicator Plotting
The system MUST include a Bias Ratio (BIAS) indicator in the generated charts.

#### Scenario: BIAS Subplot
- **WHEN** a chart is generated for an index
- **THEN** it should include a subplot displaying local BIAS lines for 10, 20, and 60 days.
- **AND** this subplot should be positioned below the volume chart.

### Requirement: Localized Chart Labels
The system MUST use Chinese labels for all chart coordinates and legends.

#### Scenario: Chinese Labels
- **WHEN** a chart is generated
- **THEN** the X-axis (Date), Y-axis (Price), Volume, and Indicator labels should be in Chinese.
- **AND** the chart title should use the Chinese name of the index.
