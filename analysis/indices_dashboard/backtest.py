import logging
import pandas as pd
import akshare as ak
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import datetime

# 配置日志 (中文)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BacktestStrategy:
    """
    MA20 严格拐头策略回测引擎
    """
    def __init__(self, symbol, name, start_date, end_date=None, initial_capital=100000.0):
        self.symbol = symbol
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        
        self.cash = initial_capital
        self.holdings = 0
        self.last_buy_date = None # 用于计算持有天数
        self.history = [] # 记录每日资产 {date, cash, holdings, total, price}
        self.trades = []  # 记录交易明细 {date, type, price, shares, commission, reason}
        self.df = None

    def fetch_data(self):
        """
        获取数据并计算 MA20
        """
        logger.info(f"正在获取 {self.name} ({self.symbol}) 的数据...")
        try:
            # 使用 akshare 获取指数数据
            df = ak.stock_zh_index_daily_em(symbol=self.symbol)
            if df is None or df.empty:
                logger.error(f"获取数据失败: {self.symbol}")
                return False
            
            # 数据清洗
            rename_dict = {}
            for col in df.columns:
                if 'date' in col.lower() or '日期' in col: rename_dict[col] = 'Date'
                elif 'open' in col.lower() or '开盘' in col: rename_dict[col] = 'Open'
                elif 'close' in col.lower() or '收盘' in col: rename_dict[col] = 'Close'
                elif 'high' in col.lower() or '最高' in col: rename_dict[col] = 'High'
                elif 'low' in col.lower() or '最低' in col: rename_dict[col] = 'Low'
                elif 'volume' in col.lower() or '成交' in col: rename_dict[col] = 'Volume'
            df.rename(columns=rename_dict, inplace=True)
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            df.sort_index(inplace=True)

            # 过滤日期 (需要多取前面 20 天计算 MA)
            filter_start = pd.to_datetime(self.start_date) - datetime.timedelta(days=60)
            df = df[df.index >= filter_start]
            if self.end_date:
                df = df[df.index <= pd.to_datetime(self.end_date)]

            # 计算 MA20
            df['MA20'] = df['Close'].rolling(window=20).mean()
            
            # 计算 Slope (今日MA20 - 昨日MA20)
            df['MA20_Slope'] = df['MA20'].diff()
            
            # 严格拐头判定
            # 拐头向上: Slope > 0 且 Yesterday_Slope <= 0
            # 拐头向下: Slope < 0 且 Yesterday_Slope >= 0
            df['Slope_Prev'] = df['MA20_Slope'].shift(1)
            
            # 标记信号 (1: Buy, -1: Sell, 0: Hold)
            df['Signal'] = 0
            
            # Buy Signal
            buy_cond = (df['MA20_Slope'] > 0) & (df['Slope_Prev'] <= 0)
            df.loc[buy_cond, 'Signal'] = 1
            
            # Sell Signal
            sell_cond = (df['MA20_Slope'] < 0) & (df['Slope_Prev'] >= 0)
            df.loc[sell_cond, 'Signal'] = -1
            
            # 真正回测开始的日期
            self.df = df[df.index >= pd.to_datetime(self.start_date)].copy()
            
            logger.info(f"数据处理完成，回测区间: {self.df.index[0].date()} 至 {self.df.index[-1].date()}")
            return True

        except Exception as e:
            logger.error(f"数据处理异常: {e}")
            return False

    def run_backtest(self):
        """
        执行回测循环
        """
        logger.info("开始执行回测...")
        
        # 初始化
        self.cash = self.initial_capital
        self.holdings = 0
        self.history = []
        self.trades = []
        
        for date, row in self.df.iterrows():
            price = row['Close']
            signal = row['Signal']
            ma20 = row['MA20']
            
            action = None
            
            # 交易逻辑
            if signal == 1 and self.cash > 0:
                # 满仓买入
                shares = int(self.cash / price) # 向下取整
                if shares > 0:
                    cost = shares * price
                    self.cash -= cost
                    self.holdings = shares
                    self.last_buy_date = date
                    action = 'Buy'
                    
                    self.trades.append({
                        'date': date,
                        'type': '买入',
                        'price': price,
                        'shares': shares,
                        'commission': 0,
                        'reason': '20日线拐头向上',
                        'balance': self.cash
                    })
                    logger.info(f"[{date.date()}] 买入 {self.name}, 价格: {price:.2f}, 股数: {shares}, 余额: {self.cash:.2f}")

            elif signal == -1 and self.holdings > 0:
                # 清仓卖出
                revenue = self.holdings * price
                
                # 计算手续费
                hold_days = (date - self.last_buy_date).days
                fee_rate = 0.015 if hold_days < 7 else 0.0
                commission = revenue * fee_rate
                
                final_cash = revenue - commission
                self.cash += final_cash
                
                action = 'Sell'
                
                self.trades.append({
                    'date': date,
                    'type': '卖出',
                    'price': price,
                    'shares': self.holdings,
                    'commission': commission,
                    'reason': f'20日线拐头向下 (持有{hold_days}天)',
                    'balance': self.cash
                })
                logger.info(f"[{date.date()}] 卖出 {self.name}, 价格: {price:.2f}, 手续费: {commission:.2f}, 余额: {self.cash:.2f}")
                self.holdings = 0

            # 每日结算
            total_assets = self.cash + (self.holdings * price)
            self.history.append({
                'date': date,
                'total': total_assets,
                'price': price,
                'ma20': ma20,
                'signal': signal,
                'action': action,
                'holdings': self.holdings,
                'cash': self.cash
            })

        final_assets = self.history[-1]['total']
        ret = (final_assets - self.initial_capital) / self.initial_capital * 100
        logger.info(f"回测结束。最终资产: {final_assets:.2f}, 收益率: {ret:.2f}%")
        return pd.DataFrame(self.history)
    
    def plot_results(self):
        """
        生成交互式 HTML 报告 (Plotly)
        """
        if not self.history:
            logger.warning("没有回测数据，无法绘图")
            return

        df_res = pd.DataFrame(self.history)
        df_res.set_index('date', inplace=True)
        
        # 补全 OHLC 数据用于画 K 线
        # self.df 包含原始 OHLC
        plot_df = self.df.loc[df_res.index]

        # 创建子图: Row 1 = K线 + MA + 买卖点; Row 2 = 资金曲线
        fig = make_subplots(
            rows=2, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.03, 
            subplot_titles=(f'{self.name} ({self.symbol}) 走势与交易信号', '账户总资产'),
            row_heights=[0.7, 0.3]
        )

        # 1. K线图
        fig.add_trace(go.Candlestick(
            x=plot_df.index,
            open=plot_df['Open'],
            high=plot_df['High'],
            low=plot_df['Low'],
            close=plot_df['Close'],
            name='K线'
        ), row=1, col=1)

        # 2. MA20
        fig.add_trace(go.Scatter(
            x=plot_df.index,
            y=plot_df['MA20'],
            mode='lines',
            line=dict(color='orange', width=1.5),
            name='MA20'
        ), row=1, col=1)

        # 3. 买卖信号 (Markers)
        # 提取买入点
        buy_data = df_res[df_res['action'] == 'Buy']
        sell_data = df_res[df_res['action'] == 'Sell']

        # 买入箭头 (红色向上)
        fig.add_trace(go.Scatter(
            x=buy_data.index,
            y=buy_data['price'] * 0.98, # 画在K线下方
            mode='markers',
            marker=dict(symbol='triangle-up', size=10, color='red'),
            name='买入',
            text=[f"买入<br>价格: {p:.2f}" for p in buy_data['price']],
            hoverinfo='text+x'
        ), row=1, col=1)

        # 卖出箭头 (绿色向下)
        fig.add_trace(go.Scatter(
            x=sell_data.index,
            y=sell_data['price'] * 1.02, # 画在K线上方
            mode='markers',
            marker=dict(symbol='triangle-down', size=10, color='green'),
            name='卖出',
            text=[f"卖出<br>价格: {p:.2f}" for p in sell_data['price']],
            hoverinfo='text+x'
        ), row=1, col=1)

        # 4. 资金曲线
        fig.add_trace(go.Scatter(
            x=df_res.index,
            y=df_res['total'],
            mode='lines',
            line=dict(color='cyan', width=2),
            name='总资产',
            fill='tozeroy' # 填充下方面积
        ), row=2, col=1)

        # 布局设置 (中文)
        fig.update_layout(
            title=f"MA20 严格拐头策略回测报告 - {self.name}",
            xaxis_rangeslider_visible=False, # 隐藏 Plotly 自带的滑动条
            height=800,
            template="plotly_dark", # 深色主题
            hovermode="x unified" # 统一显示 Hover 信息
        )
        
        # 坐标轴标签
        fig.update_yaxes(title_text="价格", row=1, col=1)
        fig.update_yaxes(title_text="资产 (元)", row=2, col=1)

        # 保存文件
        output_dir = os.path.join(os.path.dirname(__file__), 'output_backtest')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        filename = f"{self.name}_{self.symbol}_report.html"
        filepath = os.path.join(output_dir, filename)
        fig.write_html(filepath)
        logger.info(f"回测报告已生成: {filepath}")
        
if __name__ == "__main__":
    # 上证指数
    # backtest = BacktestStrategy(symbol="sh000001", name="上证指数", start_date="2024-01-01")
    
    # 创业板指
    backtest = BacktestStrategy(symbol="sz399006", name="创业板指", start_date="2024-01-01")

    if backtest.fetch_data():
        backtest.run_backtest()
        backtest.plot_results()
