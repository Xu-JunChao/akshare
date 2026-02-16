import logging
import pandas as pd
import akshare as ak
import datetime

logger = logging.getLogger(__name__)

def fetch_and_process_data(symbol, name, start_date, ma_window=20, strict_inflection=True, ma_list=None, slope_confirmation_days=2, show_signal_logs=True):
    """
    获取数据并计算指标 (MA, Slope, Signal)
    """
    logger.info(f"正在获取 {name} ({symbol}) 的数据...")
    try:
        # 1. 获取数据
        df = ak.stock_zh_index_daily_em(symbol=symbol)
        if df is None or df.empty:
            logger.error(f"获取数据失败: {symbol}")
            return None
        
        # 2. 清洗数据
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

        # 3. 过滤日期 (保留足够多的历史数据用于计算 MA)
        # 即使 start_date 是 2024-01-01，我们也需要更早的数据来计算那一天的 MA20
        # 所以这里先不做强过滤，或者过滤一个较早的时间点
        # The original code had a filter_date calculation here.
        # The new code snippet does not include this, so I'll keep the original filter_date logic
        # but adjust it to consider the maximum MA window from ma_list.
        
        # Assuming 'config' is passed or available in the scope,
        # but since it's not in the function signature, I'll define a dummy for now
        # to make the provided snippet syntactically correct.
        # In a real scenario, 'config' should be passed as an argument or defined globally.
        # For this edit, I'll simulate it based on the function's existing parameters.
        
        # --- Start of new code insertion ---
        # Strategy parameters (simulated from function args for now, as 'config' is not passed)
        # If 'config' were passed, these lines would be:
        # strategy_cfg = config.get('strategy', {})
        # ma_window = strategy_cfg.get('ma_window', 20)
        # strict_inflection = strategy_cfg.get('strict_inflection', True)
        # ma_list = strategy_cfg.get('ma_list', [20, 60, 120])
        
        # For now, using function arguments and a default ma_list
        # If the user intends to pass a 'config' object, the function signature needs to be updated.
        # For this specific instruction, I'll use the existing ma_window and strict_inflection,
        # and define a default ma_list.
        
        # Original ma_window and strict_inflection are already function parameters.
        # Let's define ma_list based on the instruction's intent.
        # Assuming a default ma_list if not explicitly provided by a 'config' object.
        ma_list = [20, 60, 120] # Default list, can be extended by ma_window
        
        # Ensure main ma_window is in ma_list
        if ma_window not in ma_list:
            ma_list.append(ma_window)
        ma_list = sorted(list(set(ma_list)))

        # Adjust filter_date to account for the largest MA window
        max_ma_window = max(ma_list)
        filter_date = pd.to_datetime(start_date) - datetime.timedelta(days=max_ma_window * 3)
        
        # Reset index to make 'Date' a column for the following operations
        df.reset_index(inplace=True)
        # Ensure 'Date' is datetime
        if not pd.api.types.is_datetime64_any_dtype(df['Date']):
             df['Date'] = pd.to_datetime(df['Date'])
             
        # Filter using the Date column
        df = df[df['Date'] >= filter_date].copy()
        
        df.sort_values('Date', inplace=True) # Ensure sorted after reset

        # Calculate all configured MAs and BIAS
        for w in ma_list:
            ma_col = f'MA{w}'
            bias_col = f'BIAS{w}'
            df[ma_col] = df['Close'].rolling(window=w).mean()
            # BIAS = (Close - MA) / MA * 100
            df[bias_col] = (df['Close'] - df[ma_col]) / df[ma_col] * 100
            
        # Signal logic still uses the main ma_window
        main_ma_col = f'MA{ma_window}'
        
        # Calculate Slope (Today's MA - Yesterday's MA)
        df['MA_Slope'] = df[main_ma_col].diff()
        
        # Strict inflection point determination
        # Upward inflection: Slope > 0 AND Yesterday_Slope <= 0
        # Downward inflection: Slope < 0 AND Yesterday_Slope >= 0
        df['Slope_Prev'] = df['MA_Slope'].shift(1)
        
        # 辅助验证列：Price_Prev_N (用于验证今日价格 vs 20日前价格)
        df['Close_Prev_N'] = df['Close'].shift(ma_window)
        
        # Mark signals (1: Buy, -1: Sell, 0: Hold)
        df['Signal'] = 0
        
        # Buy Signal (Confirmed Upward Trend)
        # 策略调整：为了过滤微小波动，改为“确认拐头”策略
        # 条件：Slope > 0 持续 N 天
        # 使用 rolling(min) > 0 来判断连续 N 天 Slope > 0
        if slope_confirmation_days > 1:
            # 连续 N 天 Slope > 0
            buy_cond = df['MA_Slope'].rolling(window=slope_confirmation_days).min() > 0
        else:
            # 只要当天 Slope > 0
            buy_cond = df['MA_Slope'] > 0

        df.loc[buy_cond, 'Signal'] = 1
        
        # Sell Signal (Slope turns negative)
        # 卖出依然保持敏感：只要拐头向下就卖
        sell_cond = (df['MA_Slope'] < 0)
        df.loc[sell_cond, 'Signal'] = -1
        
        result_df = df[df['Date'] >= pd.to_datetime(start_date)].copy()
        result_df.set_index('Date', inplace=True)
        
        if show_signal_logs:
            # 8. 记录验证日志 (仅记录信号发生变化的拐点)
            # 为了避免刷屏 (例如连续100天 Slope<0 导致连续100个卖出信号)，只记录信号跳变点
            result_df['Signal_Prev'] = result_df['Signal'].shift(1).fillna(0)
            
            changes = result_df[result_df['Signal'] != result_df['Signal_Prev']]
            # 进一步过滤：只关心变成 1 (Buy Start) 或 -1 (Sell Start) 的点
            action_points = changes[changes['Signal'] != 0]
            
            if not action_points.empty:
                logger.info(f"[{name}] 信号拐点列表 ({len(action_points)} 次):")
                for date, row in action_points.iterrows():
                    sig = row['Signal']
                    sig_type = "触发买入" if sig == 1 else "触发卖出"
                    slope = row['MA_Slope']
                    
                    desc = f"Slope={slope:.4f}"
                    if sig == 1:
                         price_curr = row['Close']
                         price_prev_n = row['Close_Prev_N']
                         desc += f", Price({price_curr:.2f}) > Prev20({price_prev_n:.2f})"
                    
                    logger.info(f"  {date.date()}: {sig_type} ({desc})")

        logger.info(f"[{name}] 数据处理完成: {len(result_df)} 行")
        return result_df

    except Exception as e:
        logger.error(f"[{name}] 处理异常: {e}")
        return None
