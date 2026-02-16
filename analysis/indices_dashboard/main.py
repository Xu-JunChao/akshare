import logging
import yaml
import os
import sys

# 导入模块
try:
    from analysis.indices_dashboard import data, strategy, plotter
except ImportError:
    # 如果作为脚本直接运行，尝试添加路径
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from analysis.indices_dashboard import data, strategy, plotter

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'config.yaml')
    
    if not os.path.exists(config_path):
        logger.error(f"配置文件未找到: {config_path}")
        return

    logger.info("加载配置...")
    config = load_config(config_path)
    
    indices = []
    csv_path = os.path.join(base_dir, 'config.csv')
    if os.path.exists(csv_path):
        import csv
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                code = row.get('code', '').strip()
                if not code:
                    continue
                
                # Check enabled status (default True if missing)
                enabled_str = row.get('enabled', 'true').lower()
                if enabled_str not in ['true', '1', 'yes', 'on']:
                    continue
                    
                # Handle optional name
                name = row.get('name', '').strip()
                if not name:
                    name = code
                
                indices.append({'code': code, 'name': name})
    else:
        logger.warning(f"指数配置文件未找到: {csv_path}")

    global_settings = config.get('settings', {})
    strategy_settings = config.get('strategy', {})
    backtest_settings = config.get('backtest', {})
    plot_settings = config.get('plot', {})
    
    start_date = global_settings.get('start_date', '2024-01-01')
    output_dir = os.path.join(base_dir, global_settings.get('output_dir', 'output'))
    enable_backtest = global_settings.get('enable_backtest', False)
    
    for idx in indices:
        code = idx['code']
        name = idx['name']
        
        logger.info(f"--- 处理 {name} ({code}) ---")
        
        # 1. 获取数据
        df = data.fetch_and_process_data(
            symbol=code, 
            name=name, 
            start_date=start_date,
            ma_window=strategy_settings.get('ma_window', 20),
            strict_inflection=strategy_settings.get('strict_inflection', True),
            slope_confirmation_days=strategy_settings.get('slope_confirmation_days', 2),
            show_signal_logs=strategy_settings.get('show_signal_logs', True)
        )
        
        if df is None:
            continue
            
        # 2. 策略处理 (统一入口)
        # 无论是否回测，都经过 process_strategy 处理数据格式
        hist_df, trades = strategy.process_strategy(
            df, backtest_settings, name=name, enable_backtest=enable_backtest
        )
        
        # 3. 绘图
        plotter.generate_report(
            hist_df, name, code, plot_settings, output_dir, enable_backtest=enable_backtest
        )
        
    logger.info("所有任务完成。")

if __name__ == "__main__":
    main()
