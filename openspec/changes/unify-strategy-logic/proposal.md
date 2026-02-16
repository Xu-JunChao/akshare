## Why

Currently, `main.py` has a branch: `if enable_backtest: ... else: ...`. This duplication makes the code harder to maintain and test. Use cases like "just viewing the chart" and "running a backtest" should share the same data pipeline.

## What Changes

We will refactor `strategy.py` to always accept data and return a standardized report structure, regardless of whether backtesting is enabled.
If backtesting is disabled, the returned data will simply have empty or zeroed trading actions/assets.
`plotter.py` will be updated to handle this unified data structure, smartly hiding the capital curve if the data indicates no trading occurred.

## Capabilities

### New Capabilities
- `unified-pipeline`: One code path for both backtest and view-only modes.
- `simplified-main`: `main.py` becomes a linear orchestrator without business logic branching.

## Impact

- [MODIFY] `analysis/indices_dashboard/strategy.py`: Rename `run_backtest_simulation` to `process_strategy` and handle no-backtest mode.
- [MODIFY] `analysis/indices_dashboard/main.py`: Remove if/else branch.
- [MODIFY] `analysis/indices_dashboard/plotter.py`: Adapt to unified input.
