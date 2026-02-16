import logging
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

logger = logging.getLogger(__name__)

def generate_report(df_history, name, symbol, config, output_dir, enable_backtest=True):
    """
    生成 HTML 报告
    :param df_history: 包含 date, price, ma, action, total 的 DataFrame
    :param config: plot 配置部分
    :param enable_backtest: 是否根据回测结果绘制资金曲线
    """
    theme = config.get('theme', 'plotly_dark')
    use_svg = config.get('use_svg', True)
    height = config.get('height', 1000)
    
    # 获取可视化配置
    strategy_cfg = config.get('strategy', {})
    ma_list = strategy_cfg.get('ma_list', [20, 60, 120])
    
    show_bias = config.get('show_bias', True)
    
    # 准备数据
    if 'date' in df_history.columns:
        df_history.set_index('date', inplace=True)
    
    # 动态计算布局
    # Row 1: Main (Candle + MAs)
    # Row 2: BIAS (Optional)
    # Row 3: Capital (Optional, if backtest)
    
    rows = 1
    row_heights = [0.6] # Initial weight for main chart
    subplot_titles = [f'{name} ({symbol}) 走势']
    
    bias_row = None
    capital_row = None
    
    if show_bias:
        rows += 1
        bias_row = rows
        row_heights.append(0.2)
        subplot_titles.append('乖离率 (BIAS)')
        
    if enable_backtest:
        rows += 1
        capital_row = rows
        row_heights.append(0.2)
        subplot_titles.append('账户净值')
        
    # Normalize row heights
    total_h = sum(row_heights)
    row_heights = [h/total_h for h in row_heights]
    
    fig = make_subplots(
        rows=rows, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=subplot_titles,
        row_heights=row_heights
    )

    # 1. Main Chart (Row 1)
    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df_history.index,
        open=df_history['Open'],
        high=df_history['High'],
        low=df_history['Low'],
        close=df_history['Close'],
        name='K线',
        increasing_line_color='red', decreasing_line_color='green'
    ), row=1, col=1)
    
    # MAs
    colors = ['orange', 'cyan', 'magenta', 'yellow', 'blue']
    for i, w in enumerate(sorted(ma_list)):
        col_name = f'MA{w}'
        if col_name in df_history.columns:
            color = colors[i % len(colors)]
            fig.add_trace(go.Scatter(
                x=df_history.index, y=df_history[col_name],
                mode='lines', name=col_name,
                line=dict(color=color, width=1)
            ), row=1, col=1)
            
    # Markers (Buy/Sell)
    if enable_backtest:
        buy_pts = df_history[df_history['action'] == 'Buy']
        sell_pts = df_history[df_history['action'] == 'Sell']
        
        if not buy_pts.empty:
            fig.add_trace(go.Scatter(
                x=buy_pts.index, y=buy_pts['Low']*0.98,
                mode='markers', name='买入',
                # Buy: Yellow, Triangle Up
                marker=dict(symbol='triangle-up', size=15, color='yellow', line=dict(width=2, color='white'))
            ), row=1, col=1)
        
        if not sell_pts.empty:
            fig.add_trace(go.Scatter(
                x=sell_pts.index, y=sell_pts['High']*1.02,
                mode='markers', name='卖出',
                # Sell: Magenta, Triangle Down
                marker=dict(symbol='triangle-down', size=15, color='magenta', line=dict(width=2, color='white'))
            ), row=1, col=1)

    # 2. BIAS Chart (Optional Row)
    if show_bias and bias_row:
        # 绘制所有 BIAS 列
        bias_cols = [c for c in df_history.columns if c.startswith('BIAS')]
        for i, col in enumerate(bias_cols):
            color = colors[i % len(colors)]
            fig.add_trace(go.Scatter(
                x=df_history.index, y=df_history[col],
                mode='lines', name=col,
                line=dict(color=color, width=1)
            ), row=bias_row, col=1)
        
        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=bias_row, col=1)

    # 3. Capital Chart (Optional Row)
    if enable_backtest and capital_row:
        fig.add_trace(go.Scatter(
            x=df_history.index, y=df_history['total'],
            mode='lines', name='资产',
            line=dict(color='cyan', width=2),
            fill='tozeroy'
        ), row=capital_row, col=1)
    
    # Layout
    fig.update_layout(
        template=theme,
        height=height,
        title=f"{name} {'策略回测' if enable_backtest else '走势分析'}报告",
        hovermode="x unified",
        xaxis_rangeslider_visible=False
    )
    
    # SVG 配置
    if use_svg:
        # 强制 SVG 渲染通常是在显示端。对于 write_html，它主要依赖 Plotly JS。
        # 如果要“清晰”，关键是不要用 Scattergl (Webgl)。我们用的是 Scatter (SVG)，所以默认就是清晰的。
        pass

    # Save
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    filename = f"{name}_{symbol}_report.html"
    filepath = os.path.join(output_dir, filename)
    fig.write_html(filepath)
    logger.info(f"[{name}] 报告生成: {filepath}")
