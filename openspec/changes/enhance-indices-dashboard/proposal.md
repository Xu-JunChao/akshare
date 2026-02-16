## Why

The current indices dashboard is functional but lacks flexibility in date range configuration and depth in financial analysis indicators. The user specifically requested the ability to configure the analysis period globally and to include Bias Ratio (BIAS) indicators for better trend analysis. Additionally, the chart labels and coordinates need to be localized to Chinese for better usability.

## What Changes

We will enhance the `analysis/indices_dashboard` module by:
1.  **Global Configuration**: Implementing a global setting for the analysis date range, defaulting to the last 6 months (approx. 120 trading days).
2.  **New Indicator**: Adding a Bias Ratio (BIAS) subplot to the charts with 10, 20, and 60-day parameters.
3.  **Localization**: Translating chart coordinates and labels to Chinese.
4.  **Visual Improvements**: optimizing the chart layout to accommodate the new indicator.

## Capabilities

### New Capabilities
<!-- Capabilities being introduced. -->

### Modified Capabilities
<!-- Existing capabilities whose REQUIREMENTS are changing. -->
- `fund-analysis-dashboard`: Add requirements for global date range configuration, BIAS indicators, and Chinese localization.

## Impact

- `analysis/indices_dashboard/main.py`: Configuration loading.
- `analysis/indices_dashboard/utils.py`: Data fetching (date range) and Plotting logic (BIAS calculation, subplots, localization).
- `analysis/indices_dashboard/config.csv`: (Indirectly) Usage pattern changes.
