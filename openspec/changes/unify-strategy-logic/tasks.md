# Tasks: Unify Strategy Logic

## 1. Refactor Strategy
- [x] 1.1 Modify `analysis/indices_dashboard/strategy.py`:
    - Rename `run_backtest_simulation` to `process_strategy`.
    - Accept `enable_backtest` flag.
    - Return standardized DataFrame even if backtest is disabled.

## 2. Refactor Plotter
- [x] 2.1 Modify `analysis/indices_dashboard/plotter.py`:
    - Accept `enable_backtest` flag.
    - Dynamically switch between 1-row (Trend only) and 2-row (Trend + Capital) layouts.

## 3. Refactor Main
- [x] 3.1 Modify `analysis/indices_dashboard/main.py`:
    - Remove branching logic.
    - Update calls to new method signatures.

## 4. Verification
- [x] 4.1 Run with `enable_backtest: true` -> Check 2-row chart.
- [x] 4.2 Run with `enable_backtest: false` -> Check 1-row chart.
