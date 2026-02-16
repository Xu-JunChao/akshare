# Design: 基金/指数走势分析工具

## Context

本项目旨在提供一个配置化、健壮的批量指数分析工具。目前只有单个脚本 `plot_indices.py`，无法满足生产级需求。本设计将引入新的目录结构和模块化代码。

## Goals / Non-Goals

**Goals:**
*   **零侵入性**：不修改根目录下现有的 `plot_indices.py`。
*   **配置化**：支持通过 CSV 文件管理指数列表和开关。
*   **健壮性**：支持失败重试、错误日志记录，确保批量任务不中断。
*   **自动化归档**：按日期保存结果图片。

**Non-Goals:**
*   不支持实时数据推送（仅每日离线分析）。
*   不支持复杂的交互式 GUI（仅生成静态图片）。

## Architecture

### Directory Structure

```text
c:\code\akshare\
├── analysis/                  # [新增] 专门存放分析工具
│   └── indices_dashboard/     # [新增] 指数看板工具包
│       ├── main.py            # [Entry] 主程序入口
│       ├── config.csv         # [Data] 配置文件
│       ├── utils.py           # [Lib] 通用工具（绘图、网络重试）
│       ├── logs/              # [Output] 运行日志
│       └── output/            # [Output] 结果图表
```

### Module Design

#### 1. Configuration (`config.py` / `main.py`)
- **功能**: 读取 `config.csv`。
- **逻辑**: 使用 `pandas` 读取 CSV，过滤 `enabled=True` 的行。
- **Schema**:
    - `code`: 指数代码 (如 `sh000001`)
    - `name`: 显示名称 (如 `上证指数`)
    - `enabled`: 开关 (`true`/`false`)
    - `notes`: 备注 (可选)

#### 2. Data Fetcher (`utils.py`)
- **功能**: 封装 `akshare` 接口调用。
- **逻辑**:
    - 增加 `@retry` 装饰器（最大重试 3 次，间隔 2 秒）。
    - 捕获所有异常，返回 `None` 并记录 error log，不抛出崩溃。

#### 3. Plotter (`utils.py`)
- **功能**: 生成 K 线图。
- **逻辑**:
    - 复用现有 `mpf.plot` 逻辑。
    - 增加 `savefig` 参数，禁用 `plt.show()`。
    - 字体强制通过 `mplfinance` 的 `style` 参数配置 `SimHei`。

#### 4. Workflow Controller (`main.py`)
- **流程**:
    1.  Setup: 创建 `logs/` 和 `output/<date>/` 目录。
    2.  Load: 读取配置。
    3.  Loop: 遍历指数列表。
    4.  Fetch & Plot: 调用工具函数。
    5.  Report: 打印简要统计（成功 N 个，失败 M 个）。

## Decisions

### 1. 为什么使用 CSV 而不是 YAML/JSON？
- **Rationale**: 方便非技术人员（或用户自己）使用 Excel 编辑，表格视图更直观地管理大量指数的开关状态。

### 2. 为什么独立 `analysis` 目录？
- **Rationale**: 保持工程根目录整洁，避免脚本散落。方便未来添加其他分析工具（e.g., `fund_correlation`）。

## Risks / Trade-offs

*   **Risk**: `akshare` 接口变动。
    *   **Mitigation**: 封装在 `utils.py` 中，接口变动时只需修改一处。
*   **Risk**: 中文字体乱码。
    *   **Mitigation**: 代码中硬编码检测系统字体或使用 `akshare` 推荐的字体配置。
