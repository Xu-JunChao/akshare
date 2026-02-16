## Context

The current indices dashboard is hardcoded to a 500-day window and lacks advanced indicators like BIAS. Users need more flexibility and better visualization tools. We will introduce a global configuration mechanism and enhance the plotting logic.

## Goals / Non-Goals

**Goals:**
- Implement a centralized configuration for date ranges (default 6 months).
- Add BIAS (10, 20, 60) subplot to K-line charts.
- Localize all chart text to Chinese.
- Ensure the plot layout is clean and readable with the new subplot.

**Non-Goals:**
- Interactive charts (we will stick to static static images).
- Real-time data updates (daily batch process is sufficient).
- Web interface (CLI tool is sufficient).

## Decisions

### Configuration Strategy
- **Decision:** Use `START_DATE` and `END_DATE` constants in `main.py` or `utils.py`.
- **Rationale:** User explicitly requested date range configuration.
- **Implementation:** 
  - `START_DATE = '2023-01-01'` (Example)
  - `END_DATE = '2023-06-30'` (Example)
  - If `END_DATE` is None/Empty, default to today.

### Plotting Library
- **Decision:** Stick with `mplfinance`.
- **Rationale:** Powerful enough for K-lines + Volume + Indicators. Supports subplots via `make_addplot`.

### BIAS Implementation
- **Formula:** `(Close - MA) / MA * 100`.
- **Periods:** 6, 12, 24 are standard, but user requested 10, 20, 60. We will use User's request.
- **Visualization:** Line chart in a separate panel below Volume.

## Risks / Trade-offs

- **Chart crowding:** Adding a 3rd panel might make the chart too tall or compress the K-line. We may need to adjust the figure key or aspect ratio.
- **Font issues:** Chinese characters might not render on all systems. We will use the existing font fallback logic in `utils.py`.
