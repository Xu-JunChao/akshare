## Context

The user wants a unified dashboard that handles data fetching, plotting, and backtesting in one cohesive workflow, configured by a single YAML file, with high-definition SVG/HTML output.

## Goals / Non-Goals

**Goals:**
- **Merge**: `main.py` + `backtest.py` -> `main.py` (Orchestrator).
- **Configure**: `config.csv` -> `config.yaml`.
- **Visualize**: SVG-based Plotly HTML charts (No PNG).
- **Verify**: Double verification logging (MA values and Price values).

**Non-Goals:**
- Complex GUI (CLI is fine).
- Real-time streaming data.

## Decisions

### 1. Architecture
- **`config.yaml`**: The single source of truth.
- **`main.py`**: The orchestrator.
    - Reads config.
    - Loops through indices.
    - Calls `data.py` to fetch/calculate.
    - Calls `strategy.py` to run backtest (if enabled).
    - Calls `plotter.py` to generate HTML.
- **`data.py`**: Replaces `utils.py` fetch/calc logic. Incorporates `calculate_bias` and `calculate_signals`.
- **`strategy.py`**: Encapsulates the `BacktestStrategy` logic (trading simulation).
- **`plotter.py`**: Encapsulates Plotly logic. Focus on SVG/High-Def.

### 2. Configuration Schema
```yaml
indices:
  - code: "sh000001"
    name: "上证指数"
settings:
  start_date: "2023-01-01"
  output_format: "html"
  enable_backtest: true
strategy:
  ma_window: 20
  strict_inflection: true
plot:
  theme: "plotly_dark"
  use_svg: true
```

### 3. Visualization
- **Library**: Plotly Graph Objects.
- **Render Mode**: `svg` (for clarity).
- **Layout**:
    - **Top**: Candlestick + MA20.
    - **Bottom**: Capital Curve (if backtest enabled).

## Risks / Trade-offs

- **Migration**: Old CSV config will be lost. User needs to migrate manually if they have many custom entries.
- **Performance**: SVG might be slower with very large datasets (e.g., tick data), but for daily index data, it's negligible.
