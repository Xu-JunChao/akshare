## Context

The user wants to backtest a "Strict MA20 Inflection" strategy and see results in a high-definition interactive HTML chart with Chinese labels.

## Goals / Non-Goals

**Goals:**
- Implement strict MA20 inflection: `MA20[i] > MA20[i-1]` (Slope > 0).
- Simulate transaction costs: 1.5% for holdings < 7 days.
- Generate interactive HTML chart (Plotly).
- **Localization**: All output (Logs, Charts, Reports) MUST be in Chinese.

**Non-Goals:**
- Complex portfolio management.
- Multi-asset correlation.

## Decisions

### Strategy Logic
- **Signal**: 
    - **Buy**: `MA20[today] > MA20[yesterday]` (Slope > 0) AND `MA20[yesterday] <= MA20[day_before]`.
    - **Sell**: `MA20[today] < MA20[yesterday]` (Slope < 0) AND `MA20[yesterday] >= MA20[day_before]`.
- **Execution**: Market Close price on signal day.

### Visualization
- **Library**: `plotly` (Interactive & High Definition).
- **Localization**: Chinese titles, axis labels, legends, and tooltips.
- **Components**:
    - **Candlestick Chart**: With MA20 overlay.
    - **Markers**: Buy (Red Triangle Up), Sell (Green Triangle Down).
    - **Capital Curve**: Net worth over time.

## Risks / Trade-offs

- **Overfitting**: Simple strategies often look good on specific partial data.
- **Execution Assumption**: We assume we can buy at Close price.
