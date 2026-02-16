
import logging
import os
import time
from functools import wraps
import pandas as pd
import akshare as ak
import mplfinance as mpf
import matplotlib.pyplot as plt

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 配置中文字体
# 尝试常见的可以显示中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def retry(max_retries=3, delay=2):
    """
    重试装饰器
    :param max_retries: 最大重试次数
    :param delay: 每次重试间隔（秒）
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    logger.warning(f"Error executing {func.__name__}: {e}. Retrying {retries}/{max_retries}...")
                    time.sleep(delay)
            logger.error(f"Failed to execute {func.__name__} after {max_retries} attempts.")
            return None
        return wrapper
    return decorator

@retry(max_retries=3, delay=2)
def fetch_data(symbol: str, start_date: str = None, end_date: str = None):
    """
    获取指定指数的日线数据，并根据日期过滤
    :param symbol: 指数代码，如 sh000001
    :param start_date: 开始日期 'YYYY-MM-DD'
    :param end_date: 结束日期 'YYYY-MM-DD'
    :return: DataFrame or None (Index: Date, Columns: Open, High, Low, Close, Volume)
    """
    logger.info(f"Fetching data for {symbol}...")
    try:
        # 尝试使用 stock_zh_index_daily_em 获取数据
        df = ak.stock_zh_index_daily_em(symbol=symbol)
        if df is None or df.empty:
            logger.warning(f"Data is empty for {symbol}")
            return None
            
        # 数据预处理：统一列名
        rename_dict = {}
        for col in df.columns:
            if 'date' in col.lower() or '日期' in col: rename_dict[col] = 'Date'
            elif 'open' in col.lower() or '开盘' in col: rename_dict[col] = 'Open'
            elif 'close' in col.lower() or '收盘' in col: rename_dict[col] = 'Close'
            elif 'high' in col.lower() or '最高' in col: rename_dict[col] = 'High'
            elif 'low' in col.lower() or '最低' in col: rename_dict[col] = 'Low'
            elif 'volume' in col.lower() or '成交' in col: rename_dict[col] = 'Volume'
        
        df.rename(columns=rename_dict, inplace=True)
        
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            
        # 按照日期过滤
        if start_date:
            df = df[df.index >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df.index <= pd.to_datetime(end_date)]
            
        if df.empty:
            logger.warning(f"Data is empty for {symbol} after filtering ({start_date} - {end_date})")
            return None

        # 补全 Volume
        if 'Volume' not in df.columns:
            df['Volume'] = 0
            
        return df
    except Exception as e:
        logger.error(f"API Error fetching {symbol}: {e}")
        raise e

def calculate_bias(df: pd.DataFrame, periods=[10, 20, 60]):
    """
    计算乖离率
    :param df: DataFrame with 'Close' column
    :param periods: list of periods for BIAS calculation
    :return: DataFrame with new BIAS columns
    """
    for p in periods:
        ma = df['Close'].rolling(window=p).mean()
        # 避免除以 0
        df[f'BIAS_{p}'] = (df['Close'] - ma) / ma * 100
    return df

def plot_kline(symbol: str, name: str, df: pd.DataFrame, output_dir: str):
    """
    绘制并保存 K 线图
    """
    if df is None or df.empty:
        return

    try:
        # 检查必要列
        required = ['Open', 'High', 'Low', 'Close']
        if not all(col in df.columns for col in required):
            logger.error(f"Missing columns for {symbol}. Available: {df.columns}")
            return

        # 使用全部数据（已经在 fetch_data 中经过过滤）
        plot_df = df.copy()

        # 计算 BIAS
        plot_df = calculate_bias(plot_df)

        # 准备 style
        s = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.family': ['SimHei', 'Microsoft YaHei']})

        # 添加 BIAS 子图
        # 注意: Volume 占用 panel 1, 所以 BIAS 用 panel 2
        ap = [
            mpf.make_addplot(plot_df['BIAS_10'], panel=2, color='fuchsia', secondary_y=False, width=1),
            mpf.make_addplot(plot_df['BIAS_20'], panel=2, color='orange', secondary_y=False, width=1),
            mpf.make_addplot(plot_df['BIAS_60'], panel=2, color='green', secondary_y=False, width=1),
        ]

        # 文件路径
        filename = f"{name}_{symbol}.png".replace("/", "_") # 防止名字里有非法字符
        filepath = os.path.join(output_dir, filename)

        # 绘图并保存
        mpf.plot(
            plot_df,
            type='candle',
            mav=(20, 60, 120),
            volume=True,
            addplot=ap,
            title=f"{name} ({symbol})",
            style=s,
            ylabel='价格',
            ylabel_lower='成交量',
            panel_ratios=(2, 1, 1), # 主图:成交量:BIAS 高度比例
            savefig=dict(fname=filepath, dpi=100, pad_inches=0.25),
            warn_too_much_data=10000
        )
        logger.info(f"Saved plot to {filepath}")
    
    except Exception as e:
        logger.error(f"Error plotting {symbol}: {e}")
