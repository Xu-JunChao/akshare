import akshare as ak
import pandas as pd
import numpy as np

def run_backtest(df, bias_window=10, bias_threshold=None):
    """
    Run simplified backtest:
    Buy: MA20 Slope > 0 (2-day confirmed)
    Sell: 
        1. MA20 Slope < 0
        2. BIAS(N) > bias_threshold (if enabled)
    Returns: Total Return %
    """
    # 1. Compute Indicators
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['Slope'] = df['MA20'].diff()
    df['Slope_Prev'] = df['Slope'].shift(1)
    
    # BIAS Calculation (Close - MA_N) / MA_N * 100
    ma_n = df['Close'].rolling(window=bias_window).mean()
    df['BIAS'] = (df['Close'] - ma_n) / ma_n * 100
    
    # 2. Simulate Trading
    position = 0
    cash = 100000
    shares = 0
    initial_capital = 100000
    
    # Align signals with data.py logic (Confirmed Buy)
    # Buy: Slope > 0 and Prev > 0
    # Sell: Slope < 0 OR BIAS > Threshold
    
    for i in range(20, len(df)):
        price = df['Close'].iloc[i]
        slope = df['Slope'].iloc[i]
        slope_prev = df['Slope_Prev'].iloc[i]
        bias = df['BIAS'].iloc[i]
        date = df.index[i]
        
        # Buy Signal
        buy_signal = (slope > 0) and (slope_prev > 0)
        
        # Sell Signal
        sell_signal_slope = (slope < 0)
        sell_signal_bias = (bias_threshold is not None) and (bias > bias_threshold)
        sell_signal = sell_signal_slope or sell_signal_bias
        
        if position == 0:
            if buy_signal:
                # Buy
                shares = cash / price
                cash = 0
                position = 1
        elif position == 1:
            if sell_signal:
                # Sell
                cash = shares * price
                shares = 0
                position = 0
                
    final_value = cash + (shares * df['Close'].iloc[-1])
    return (final_value - initial_capital) / initial_capital * 100

def optimize_bias(symbol="sh000813", start_date="2020-01-01"):
    print(f"Fetching data for {symbol} ...")
    try:
        df = ak.stock_zh_index_daily_em(symbol=symbol)
        df['Date'] = pd.to_datetime(df['date'])
        df.set_index('Date', inplace=True)
        df = df[df.index >= start_date].copy()
        df.rename(columns={'close':'Close'}, inplace=True)
        df['Close'] = pd.to_numeric(df['Close'])
        
        print(f"Data range: {df.index[0].date()} to {df.index[-1].date()}")
        print("-" * 40)
        
        # Baseline (No BIAS Sell)
        base_ret = run_backtest(df.copy(), bias_threshold=None)
        print(f"基准收益 (仅Slope卖出): {base_ret:.2f}%")
        
        # Test Thresholds
        best_ret = -999
        best_th = None
        
        print("\n测试不同 BIAS 阈值 (基于 MA10):")
        print("阈值(%) | 收益率(%) | 提升(%)")
        print("-------|-----------|--------")
        
        for th in range(3, 21): # Test 3% to 20%
            ret = run_backtest(df.copy(), bias_window=10, bias_threshold=th)
            diff = ret - base_ret
            print(f"{th:6d} | {ret:9.2f} | {diff:+.2f}")
            
            if ret > best_ret:
                best_ret = ret
                best_th = th
                
        print("-" * 40)
        if best_ret > base_ret:
            print(f"✅ 最佳阈值: {best_th}% (收益率: {best_ret:.2f}%)")
            print(f"   相比基准提升: {best_ret - base_ret:.2f}%")
        else:
            print("❌ 增加 BIAS 卖出并未提升收益 (可能卖飞了牛市)")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    optimize_bias()
