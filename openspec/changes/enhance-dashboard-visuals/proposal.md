## Why

The current charts are too simple (only Close price line and one MA). Users need professional technical analysis tools: Candlestick (K-line), multiple Moving Averages (20, 60, 120), and BIAS indicators in a separate subplot.

## What Changes

We will upgrade `data.py` to calculate multiple MAs and preserve OHLC data.
We will upgrade `plotter.py` to render a 2-3 row layout:
- Row 1: Candlestick + MA20/60/120 + Signals
- Row 2: BIAS (6/12/24 or user config)
- Row 3: Capital Curve (if backtest enabled)

## Capabilities

### New Capabilities
- `multi-ma`: Configurable multiple moving averages.
- `candlestick-chart`: Professional K-line visualization.
- `bias-subplot`: Independent subplot for BIAS indicators.

## Impact

- [MODIFY] `analysis/indices_dashboard/config.yaml`: Add `ma_list` and `show_bias`.
- [MODIFY] `analysis/indices_dashboard/data.py`: Calculate multiple MAs.
- [MODIFY] `analysis/indices_dashboard/strategy.py`: Pass through OHLC and new metrics.
- [MODIFY] `analysis/indices_dashboard/plotter.py`: Implement complex subplot layout.
