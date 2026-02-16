# Tasks: 基金/指数走势分析工具

## 1. 基础结构搭建

- [x] 1.1 创建 `analysis/indices_dashboard` 目录结构
    - 创建 `analysis/indices_dashboard/logs/`
    - 创建 `analysis/indices_dashboard/output/`
- [x] 1.2 创建配置文件 `analysis/indices_dashboard/config.csv`
    - 添加表头：`code,name,enabled,notes`
    - 添加示例数据：上证指数, 创业板指, 中证有色

## 2. 核心模块实现

- [x] 2.1 实现 `utils.py` - 数据获取模块
    - 封装 `akshare` 调用
    - 实现最大重试次数装饰器 (`@retry`)
    - 实现异常捕获与日志记录
- [x] 2.2 实现 `utils.py` - 绘图模块
    - 封装 `mplfinance` 调用
    - 配置中文字体 (`SimHei`)
    - 实现图片保存逻辑 (无弹窗)
- [x] 2.3 实现 `main.py` - 主流程控制
    - 读取 CSV 配置并过滤 `enabled=True`
    - 遍历指数列表，串行调用数据获取与绘图
    - 输出简要执行统计报告

## 3. 验证与文档

- [x] 3.1 运行测试
    - 执行 `python analysis/indices_dashboard/main.py`
    - 验证 `logs/` 下生成日志文件
    - 验证 `output/<date>/` 下生成图片文件
- [x] 3.2 错误处理测试
    - 在 CSV 中添加无效代码，验证脚本不崩溃并记录错误
