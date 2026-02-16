# Proposal: 基金/指数走势分析工具

## Context

<!-- Why are we doing this? Current state, problems, goals. -->
目前工程中只包含一个名为 `plot_indices.py` 的脚本，只能通过硬编码的方式分析特定的指数（如恒生科技、有色金属）。
用户需要一个更灵活、生产级的工具，支持通过配置文件批量管理关注的指数，并自动生成 K 线分析图。
要求不修改现有代码，而是通过新增模块来实现。

## What Changes

<!-- Describe what will change. Be specific about new capabilities, modifications, or removals. -->
我们将开发一个新的 Python 分析工具，置于 `analysis/indices_dashboard` 目录下。

核心功能包括：
1.  **配置化管理**：通过 `config.csv` 管理指数列表，支持“启用/禁用”开关。
2.  **批量分析**：自动读取配置，利用 `akshare` 获取数据并绘制 K 线图（包含均线）。
3.  **结果归档**：生成的图片按日期自动保存到 `output/` 目录，不弹出窗口。
4.  **健壮性**：即使个别指数获取失败，脚本也会记录错误日志并继续执行，支持网络请求重试。

## Capabilities

### New Capabilities
<!-- Capabilities being introduced. Replace <name> with kebab-case identifier (e.g., user-auth, data-export, api-rate-limiting). Each creates specs/<name>/spec.md -->
- `fund-analysis-dashboard`: 包含配置读取、数据抓取、绘图和流程控制的核心能力。

### Modified Capabilities
<!-- Existing capabilities whose REQUIREMENTS are changing (not just implementation).
     Only list here if spec-level behavior changes. Each needs a delta spec file.
     Use existing spec names from openspec/specs/. Leave empty if no requirement changes. -->

## Impact

<!-- Affected code, APIs, dependencies, systems -->
- **新增目录**: `analysis/indices_dashboard/`
- **新增文件**:
    - `analysis/indices_dashboard/main.py` (主程序)
    - `analysis/indices_dashboard/config.csv` (配置文件)
    - `analysis/indices_dashboard/requirements.txt` (可选，如果需要独立依赖)
- **不影响**: 根目录下的 `plot_indices.py` 和其他现有业务代码。
