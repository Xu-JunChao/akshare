import logging
import pandas as pd

logger = logging.getLogger(__name__)

def process_strategy(df, config, name="Asset", enable_backtest=True):
    """
    处理策略逻辑 (统一入口)
    :param df: 包含 Signal, Close, Date 的 DataFrame
    :param config: backtest 配置部分
    :param enable_backtest: 是否开启资金回测
    :return: DataFrame (history), Report Dict
    """
    initial_capital = config.get('initial_capital', 100000)
    commission_rate_short = config.get('commission_rate_short', 0.015)
    short_term_days = config.get('short_term_days', 7)
    
    logger.info(f"[{name}] 开始处理策略 (回测={'开启' if enable_backtest else '关闭'})...")
    
    cash = initial_capital
    holdings = 0
    last_buy_date = None
    
    history = []
    trades = []
    
    # 获取 MA 列名 (假设 df 只有一列 MA)
    ma_col = [c for c in df.columns if c.startswith('MA')]
    ma_val_key = ma_col[0] if ma_col else 'MA'

    for date, row in df.iterrows():
        price = row['Close']
        signal = row['Signal']
        ma_val = row.get(ma_val_key, 0)
        
        action = None
        
        # 仅当开启回测时才进行交易逻辑
        if enable_backtest:
            # 1. Buy Logic
            if signal == 1 and cash > 0:
                shares = int(cash / price)
                if shares > 0:
                    cost = shares * price
                    cash -= cost
                    holdings = shares
                    last_buy_date = date
                    action = 'Buy'
                    
                    trades.append({
                        'date': date, 'type': '买入', 'price': price, 
                        'shares': shares, 'commission': 0, 'balance': cash
                    })

            # 2. Sell Logic
            elif signal == -1 and holdings > 0:
                revenue = holdings * price
                
                # Commission
                if last_buy_date:
                    hold_days = (date - last_buy_date).days
                else:
                    hold_days = 999 
                
                fee = 0.0
                if hold_days < short_term_days:
                    fee = revenue * commission_rate_short
                
                final_revenue = revenue - fee
                cash += final_revenue
                
                action = 'Sell'
                trades.append({
                    'date': date, 'type': '卖出', 'price': price, 
                    'shares': holdings, 'commission': fee, 'balance': cash
                })
                
                holdings = 0
        
        # 3. Standardized Record
        # 如果不开回测，total 就是 initial_capital，holdings=0
        total_assets = cash + (holdings * price)
        
        record = {
            'date': date,
            'total': total_assets,
            'price': price, # Close
            'action': action, # Only populated if backtest enabled
            'signal': signal,
            
            # Pass through OHLC
            'Open': row.get('Open', price),
            'High': row.get('High', price),
            'Low': row.get('Low', price),
            'Close': price
        }
        
        # Pass through all MA and BIAS columns
        for col in df.columns:
            if col.startswith('MA') or col.startswith('BIAS'):
                record[col] = row.get(col, 0)
                
        history.append(record)
        
    final_assets = history[-1]['total']
    ret = (final_assets - initial_capital) / initial_capital * 100
    
    if enable_backtest:
        logger.info(f"[{name}] 回测结束: 最终资产 {final_assets:.2f}, 收益率 {ret:.2f}%")
    else:
        logger.info(f"[{name}] 策略处理完成 (无回测)")
    
    return pd.DataFrame(history), trades
