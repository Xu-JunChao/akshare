## ADDED Requirements

### Requirement: Centralized YAML Configuration
The system MUST read all operational parameters from a single `config.yaml` file.

#### Scenario: Startup
- **WHEN** `analysis/indices_dashboard/main.py` is executed
- **THEN** it should attempt to read `analysis/indices_dashboard/config.yaml`.
- **IF** the file is missing, it should raise a clear error message.

#### Scenario: Configuration Structure
The `config.yaml` MUST support the following sections:
- `indices`: List of indices to process (code, name).
- `settings`: Global settings (start_date, output_format, enable_backtest).
- `strategy`: Trading strategy parameters (ma_window, strict_inflection).
- `plot`: Plotting preferences (theme, use_svg).

### Requirement: SVG Plot Rendering
To address blurriness issues, the plotting module MUST support SVG rendering.

#### Scenario: Generate Plot
- **WHEN** a plot is generated
- **IF** `plot.use_svg` is true in `config.yaml`
- **THEN** the Plotly figure should be rendered using `render_mode='svg'` or configured to ensure vector graphics output in HTML.
