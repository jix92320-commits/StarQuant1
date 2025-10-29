# -*- coding: utf-8 -*-
"""
StarQuant v5.3 FinalPro - 实盘行情模块（稳定版）
"""
import akshare as ak
import pandas as pd
import datetime

# data_fetcher.py
import os, json, time
from datetime import datetime
try:
    import akshare as ak
except:
    ak = None

CACHE = "fallback_market.json"

def _save_cache(rows):
    try:
        with open(CACHE, "w", encoding="utf-8") as f:
            json.dump({"ts": time.time(), "rows": rows}, f, ensure_ascii=False)
    except: pass

def _load_cache():
    if not os.path.exists(CACHE): return []
    try:
        with open(CACHE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("rows", [])
    except:
        return []

def get_realtime_data(limit=3000):
    rows = []
    # 1. 先读缓存（保证不为空）
    cache = _load_cache()
    if cache: rows = cache

    # 2. 再尝试拉取实时（失败不抛错）
    try:
        if ak and hasattr(ak, "stock_zh_a_spot_em"):
            df = ak.stock_zh_a_spot_em()
            if df is not None and len(df) > 0:
                df = df.rename(columns={"代码":"code","名称":"name","最新价":"price","涨跌幅":"pct"})
                df = df[~df["name"].astype(str).str.contains("ST|退|BJ", na=False)]
                rows = df[["code","name","price","pct"]].head(limit).to_dict("records")
                _save_cache(rows)  # 刷新缓存
    except Exception:
        # 网络出问题就安静回退到缓存
        pass

    return rows


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
