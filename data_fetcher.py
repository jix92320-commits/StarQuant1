# -*- coding: utf-8 -*-
"""
StarQuant v5.3 FinalPro - 实盘行情模块（稳定版）
"""
import akshare as ak
import pandas as pd
import datetime

def get_realtime_data(limit=300):
    """获取真实A股行情，自动过滤 ST / BJ / 退市"""
    try:
        df = ak.stock_zh_a_spot_em()
        df = df.convert_dtypes()
        df = df.rename(columns={
            "代码": "code", "名称": "name", "最新价": "price",
            "涨跌幅": "pct", "成交量": "volume", "成交额": "amount"
        })
        df = df[~df["name"].str.contains("ST|退|BJ", na=False)]
        df = df[df["price"].astype(float) > 0]
        df["pct"] = pd.to_numeric(df["pct"], errors="coerce")
        data = df.head(limit).to_dict("records")

        for row in data:
            for k, v in list(row.items()):
                if isinstance(v, str):
                    row[k] = v.encode("utf-8", "ignore").decode("utf-8")
        return data
    except Exception as e:
        print("❌ 行情错误：", e)
        return []

def get_time_status():
    now = datetime.datetime.now()
    hour = now.hour
    if 9 <= hour < 15:
        status = "交易中"
    elif hour >= 15:
        status = "收盘"
    else:
        status = "未开盘"
    return {"status": status, "phase": status, "now": now.strftime("%H:%M:%S")}

def normalize_keys(data_list):
    norm = []
    for i in data_list:
        new = {str(k).lower(): v for k, v in i.items()}
        norm.append(new)
    return norm
