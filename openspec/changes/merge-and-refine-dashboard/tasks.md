# Tasks: Merge and Refine Dashboard

## 1. 结构与配置
- [x] 1.1 创建 `analysis/indices_dashboard/config.yaml`
- [x] 1.2 创建 `analysis/indices_dashboard/data.py` (数据层)
- [x] 1.3 创建 `analysis/indices_dashboard/strategy.py` (回测层)
- [x] 1.4 创建 `analysis/indices_dashboard/plotter.py` (展示层)
- [x] 1.5 重构 `analysis/indices_dashboard/main.py` (入口)

## 2. 逻辑迁移与优化
- [x] 2.1 迁移 fetch_data 和 MA20 计算逻辑到 `data.py`
    - 增加双重验证日志 (Price vs MA)
- [x] 2.2 迁移 BacktestStrategy 到 `strategy.py`
    - 适配 config.yaml 参数
- [x] 2.3 迁移绘图逻辑到 `plotter.py`
    - 强制使用 SVG 渲染
    - 优化 Layout (去除杂乱元素)

## 3. 清理
- [x] 3.1 删除 `backtest.py`
- [x] 3.2 删除 `utils.py` (功能合并入 data/plotter)
- [x] 3.3 删除 `config.csv`

## 4. 验证
- [ ] 4.1 运行新版 `main.py`
- [ ] 4.2 检查 HTML 输出清晰度 (SVG)
- [ ] 4.3 检查日志验证信息
