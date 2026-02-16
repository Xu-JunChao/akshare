# Tasks: Enhance Dashboard Visuals

## 1. Upgrade Data Layer
- [x] 1.1 Modify `config.yaml` to include `ma_list` and `show_bias`.
- [x] 1.2 Modify `data.py` to calculate multiple MAs (loop `ma_list`).
- [x] 1.3 Modify `strategy.py` to pass through all data columns (including Open, High, Low, BIAS, etc.).

## 2. Upgrade Plotter
- [x] 2.1 Modify `plotter.py` to support multi-line MAs loops.
- [x] 2.2 Modify `plotter.py` to use `go.Candlestick` for price.
- [x] 2.3 Modify `plotter.py` layout logic to support optional BIAS row.
    - Logic: Row 1 (Main), Row 2 (BIAS if show), Row 3 (Capital if backtest).

## 3. Verification
- [x] 3.1 Run verification script to check 3-row layout (Candle + BIAS + Capital).
- [x] 3.2 Check visual quality.
