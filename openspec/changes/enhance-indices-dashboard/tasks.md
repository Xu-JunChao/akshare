# Tasks: 增强基金/指数走势分析工具

## 1. 全局配置实现

- [x] 1.1 在 `analysis/indices_dashboard/main.py` 或 `utils.py` 中定义常量
    - `START_DATE = 'YYYY-MM-DD'`
    - `END_DATE = 'YYYY-MM-DD'` (可为 None，默认为今天)
    - 确保数据获取逻辑使用此日期范围过滤

## 2. 乖离率 (BIAS) 指标实现

- [x] 2.1 修改 `analysis/indices_dashboard/utils.py` 中的 `fetch_data` 或 `plot_kline`
    - 计算 BIAS 10, 20, 60
    - 公式: `(Close - MA) / MA * 100`
- [x] 2.2 修改 `plot_kline` 绘图逻辑
    - 使用 `mpf.make_addplot` 添加 BIAS 子图 (Panel 2)
    - 调整图表高度和布局以容纳新子图

## 3. 中文本地化与界面优化

- [x] 3.1 修改 `plot_kline` 中的标签
    - 确保 X 轴、Y 轴、Volume、BIAS 等标签为中文
    - `ylabel='价格'`, `ylabel_lower='成交量'` 等
- [x] 3.2 验证中文字体显示
    - 确保 `simhei` 或其他中文字体生效，避免乱码

## 4. 验证与清理

- [x] 4.1 运行脚本生成图表
    - 检查是否生成了包含 BIAS 的新图表
    - 检查日期范围是否正确 (约半年)
    - 检查中文显示是否正常
- [x] 4.2 清理代码
    - 移除硬编码的魔法数字
