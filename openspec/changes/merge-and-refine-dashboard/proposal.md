## Why

The current implementation has split logic between `main.py` (plotting) and `backtest.py` (backtesting), leading to code duplication and disjointed workflows.
Additionally, the user finds the HTML charts blurry and wants to consolidate configuration management.

## What Changes

We will merge the codebase into a unified `main.py`, supported by `data.py` (logic), `plotter.py` (visualization), and `config.yaml` (configuration).
We will remove PNG generation in favor of high-quality, interactive HTML reports with SVG-based rendering for clarity.

## Capabilities

### New Capabilities
- `unified-workflow`: Single entry point for fetching data, backtesting (optional), and generating reports.
- `yaml-configuration`: Centralized configuration for indices, strategies, and plotting.
- `clear-html-charts`: SVG-based Plotly charts for high-definition rendering.

## Impact

- [NEW] `analysis/indices_dashboard/config.yaml`: New configuration file.
- [NEW] `analysis/indices_dashboard/plotter.py`: New plotting module.
- [MODIFY] `analysis/indices_dashboard/main.py`: Refactored main entry point.
- [DELETE] `analysis/indices_dashboard/backtest.py`: Logic merged into main/plotter.
- [DELETE] `analysis/indices_dashboard/config.csv`: Replaced by YAML.
