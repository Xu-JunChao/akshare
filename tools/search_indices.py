import akshare as ak
import pandas as pd
import argparse

def search_indices(keyword=None):
    """
    搜索所有相关指数代码
    """
    print("正在获取所有可用指数列表...")
    try:
        # 尝试多种获取方式
        methods = [
            ("index_stock_info (所有指数)", lambda: ak.index_stock_info()),
            # ("中证系列 (spot_em)", lambda: ak.stock_zh_index_spot_em(symbol="中证系列")), # Fails
        ]
        
        dfs = []
        for desc, func in methods:
            try:
                print(f"尝试获取: {desc} ...")
                d = func()
                if d is not None and not d.empty:
                    dfs.append(d)
            except Exception as ex:
                print(f"  获取失败 ({desc}): {ex}")
        
        if dfs:
            df = pd.concat(dfs, ignore_index=True)
            # rename specific columns if needed (index_stock_info uses different cols)
            # index_stock_info cols: index_code, display_name, publish_date, ...
            df.rename(columns={'index_code': '代码', 'display_name': '名称', 'publish_date': '发布日期'}, inplace=True)
            # 去重
            if '代码' in df.columns:
                df.drop_duplicates(subset=['代码'], inplace=True)
        else:
            return pd.DataFrame()
            
        # 字段映射
        cols = df.columns
        # 常见列名: '代码', '名称', '最新价' 等
        
        # 筛选想要的列
        target_cols = ['代码', '名称']
        if '最新价' in cols: target_cols.append('最新价')
        if '涨跌幅' in cols: target_cols.append('涨跌幅')
        
        result = df[target_cols]
        
        if keyword:
            print(f"筛选关键词: {keyword}")
            filtered = result[result['名称'].str.contains(keyword, na=False)]
        else:
            filtered = result
            
        return filtered
        
    except Exception as e:
        print(f"获取指数列表失败: {e}")
        return pd.DataFrame()

def main():
    parser = argparse.ArgumentParser(description="搜索指数代码")
    parser.add_argument("keyword", nargs='?', default="中证", help="搜索关键词 (默认: 中证)")
    args = parser.parse_args()
    
    df = search_indices(args.keyword)
    

if __name__ == "__main__":
    main()
