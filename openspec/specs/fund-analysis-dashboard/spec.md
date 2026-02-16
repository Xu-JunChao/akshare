## ADDED Requirements

### Requirement: 配置文件读取
系统应从指定路径（`analysis/indices_dashboard/config.csv`）读取指数配置信息。

#### Scenario: 正常读取配置
- **WHEN** 配置文件存在且格式正确（包含 code, name, enabled 列）
- **THEN** 系统应加载所有 `enabled=true` 的指数条目进入待处理列表

#### Scenario: 配置文件缺失或为空
- **WHEN** 配置文件不存在或为空
- **THEN** 系统应提示错误并安全退出，不进行任何下载操作

### Requirement: 批量数据抓取与绘图
系统应遍历待处理列表，利用 `akshare` 接口获取数据并生成 K 线图。

#### Scenario: 成功获取数据
- **WHEN** `akshare` 接口返回有效数据（包含 OHLCV）
- **THEN** 系统应绘制包含 MA20/MA60/MA120 的 K 线图，并保存为图片文件

#### Scenario: 数据获取失败
- **WHEN** 网络超时、接口报错或数据为空
- **THEN** 系统应捕获异常，记录错误日志（包括指数代码和错误信息），并继续处理下一个指数

### Requirement: 结果归档
生成的分析结果图片应按日期归档，避免文件混乱。

#### Scenario: 图片保存路径
- **WHEN** 绘图完成
- **THEN** 图片应保存至 `analysis/indices_dashboard/output/<YYYY-MM-DD>/` 目录下，文件名格式推荐为 `<name>_<code, optional>.png`
