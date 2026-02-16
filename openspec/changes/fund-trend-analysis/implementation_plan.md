# Implementation Plan - Fund Trend Analysis Dashboard

Goal: Implement a configurable, production-grade tool for batch analyzing fund/index trends, generating K-line plots with moving averages.

## User Review Required

> [!IMPORTANT]
> This implementation introduces a new directory `analysis/indices_dashboard` and does not modify any existing root-level scripts.

## Proposed Changes

### analysis/indices_dashboard

#### [NEW] [analysis/indices_dashboard/config.csv](file:///c:/code/akshare/analysis/indices_dashboard/config.csv)
- Create initial configuration file with columns: `code`, `name`, `enabled`, `notes`.
- specific initial content: `sh000001` (上证指数), `sz399006` (创业板指), `csi930708` (中证有色).

#### [NEW] [analysis/indices_dashboard/utils.py](file:///c:/code/akshare/analysis/indices_dashboard/utils.py)
- Implement `fetch_data(symbol)`: Encapsulate `akshare` calls with retry logic.
- Implement `plot_kline(symbol, name, data, output_dir)`: Generate and save K-line plots using `mplfinance`.

#### [NEW] [analysis/indices_dashboard/main.py](file:///c:/code/akshare/analysis/indices_dashboard/main.py)
- Main entry point.
- Read `config.csv`.
- Iterate through enabled indices.
- Call `fetch_data` and `plot_kline`.
- Handle errors and logging.

## Verification Plan

### Automated Tests
- Run the main script: `python analysis/indices_dashboard/main.py`
- Check if `analysis/indices_dashboard/logs/` contains log files.
- Check if `analysis/indices_dashboard/output/<today>/` contains generated `.png` images.

### Manual Verification
- Verify generated images contain K-lines and MA lines.
- Verify that disabled entries in `config.csv` are skipped.
- Test error handling by adding an invalid code to `config.csv` and ensuring the script continues.
