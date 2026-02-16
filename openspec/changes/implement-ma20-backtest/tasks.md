# Tasks: Implement MA20 Backtest (Chinese)

## 1. 基础环境准备
- [x] 1.1 更新 `requirements.txt` 添加 `plotly`
- [x] 1.2 创建 `analysis/indices_dashboard/backtest.py` 基础框架

## 2. 策略逻辑实现
- [x] 2.1 实现 MA20 计算与严格拐头判定 (`Slope > 0`)
- [x] 2.2 实现交易模拟引擎
    - 初始资金设置
    - T+0 / T+1 逻辑（假设以收盘价成交）
    - 7天内赎回费 1.5% 逻辑
    - **Log 输出**: 使用中文日志

## 3. 可视化实现 (Plotly)
- [x] 3.1 绘制基础 K 线与 MA20 (中文标题/坐标轴)
- [x] 3.2 绘制买卖点标记 (Arrows)
- [x] 3.3 绘制资金曲线 (Capital Curve)
- [x] 3.4 组合图表并导出为 HTML

## 4. 验证
- [ ] 4.1 运行回测脚本
    - 验证生成 `backtest_report.html`
    - 验证中文显示正常
    - 验证手续费计算正确
