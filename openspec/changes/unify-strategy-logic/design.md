## Context

Currently, the `main.py` orchestrator branches based on `enable_backtest`. This creates two different data structures (`hist_df` vs `df` with renamed columns) passed to the plotter, increasing complexity.

## Goals

1.  **Single Data Path**: `data.py` -> `strategy.py` -> `plotter.py`.
2.  **Standardized Output**: `strategy.py` always returns a `report_df` with standard columns: `date, total, price, ma, signal, action, holdings, cash`.
3.  **Config Driven**: The `plotter` decides whether to show the "Capital Curve" based on whether `total` changes over time, or explicitly via config, rather than receiving different data shapes.

## Decisions

### 1. `strategy.py` Refactor
- Rename `run_backtest_simulation` -> `process_strategy(df, config, name, enable_backtest=True)`.
- If `enable_backtest` is False:
    - Still iterate or vector-calculate to produce the same columns.
    - `total` = initial_capital (flat line).
    - `action` = None.
    - `holdings` = 0.
- Return `(report_df, trades_list)`.

### 2. `main.py` Refactor
- Remove `if enable_backtest:` block.
- Always call `strategy.process_strategy`.
- Always call `plotter.generate_report`.

### 3. `plotter.py` Refactor
- Check if `enable_backtest` is false (passed in config).
- If false, hide the "Capital Curve" subplot or just show it as flat (user preference could be to hide it).
- **Decision**: If `enable_backtest` is False, we can either:
    A) Hide the bottom subplot entirely (1 row).
    B) Show it flat (2 rows).
    -> Let's go with **A** (Hide/Single Row) if `enable_backtest` is False, to save space.

## Risks
- Performance: Iterating through rows in `strategy.py` even when not backtesting might be slightly slower than vector ops, but for <10000 rows it's negligible (ms level). The code simplicity win is worth it.
