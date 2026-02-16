## Goals

1.  **Professional Visualization**: Replace line chart with Candlestick chart.
2.  **Indicators**: Display MA20, MA60, MA120. Display BIAS20/60 in a separate subplot.
3.  **Layout**: Dynamic layout supporting 3 rows (Main, BIAS, Capital) or 2 rows (Main, BIAS) based on config.

## Decisions

### 1. Unified Interface
`process_strategy` must now return a DataFrame with `Open, High, Low, Close, MAxx, BIASxx`.
Previously it only returned `price` (Close) and one `ma`.
**Change**: `process_strategy` should return `history_df` containing ALL columns from `data.py`'s result, plus `action` and `total`.

### 2. Layout Logic in `plotter.py`
We need a robust row allocation strategy.
Let `total_rows` = 1 (Main).
If `show_bias`: `total_rows` += 1.
If `enable_backtest`: `total_rows` += 1.

**Row Assignment:**
- **Main (Row 1)**: Candlestick + MAs + Buy/Sell Markers.
- **BIAS (Row 2 or 3)**: Independent subplot.
- **Capital (Row 2 or 3)**: Independent subplot.

Let's fix the order:
- Row 1: Main (Always)
- Row 2: BIAS (Optional)
- Row 3: Capital (Optional)

If BIAS is hidden, Capital moves to Row 2.

### 3. Config
```yaml
strategy:
  ma_list: [20, 60, 120]
plot:
  show_bias: true
```

## Risks
- **Data Volume**: Rendering 3 subplots with thousands of candles might be heavy for SVG. We will stick to SVG but user can switch to WebGL if needed (future scope).
