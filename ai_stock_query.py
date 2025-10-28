# -*- coding: utf-8 -*-
"""
StarQuant v5.3 FinalPro — 打板扫描 & 自选接口 稳定版
"""
import random

HOT_ZONES = ["宁波", "杭州", "拉萨", "上海", "深圳", "成都", "北京"]
LEADERS = ["新能源", "半导体", "医药", "光伏", "汽车", "AI算力", "中字头", "券商"]

def get_board_suggestions(market_data, topk=10):
    if not market_data:
        return []
    ranked = []
    for row in market_data:
        pct = row.get("pct", 0)
        amt = row.get("amount", 0)
        sc = pct * 0.6 + (amt / 1e8) * 0.4
        sc = max(-10, min(sc, 10))
        liq = min(max(row.get("turnover", 0) * 0.7 + amt / 1e9 * 0.3, 0), 10)
        total = round((sc * 0.5 + liq * 0.5) + random.uniform(-1, 1), 2)
        ranked.append({
            "code": row.get("code"),
            "name": row.get("name"),
            "price": row.get("price"),
            "pct": pct,
            "score": total,
            "zone": random.choice(HOT_ZONES),
            "theme": random.choice(LEADERS),
            "signal": "🔥 强势打板" if total > 7.5 else "⚡ 潜力活跃" if total > 5 else "观察中"
        })
    return sorted(ranked, key=lambda x: x["score"], reverse=True)[:topk]

def apply_watchlist_actions(watchlist, action, payload):
    """支持前端 add / del 操作"""
    if action == "add" and payload not in watchlist:
        watchlist.append(payload)
    elif action == "del":
        watchlist = [x for x in watchlist if x != payload]
    return watchlist

def get_watchlist_snapshot(market_data, predictions):
    pred_map = {p["code"]: p for p in predictions}
    snap = []
    for r in market_data:
        code = r.get("code")
        if code in pred_map:
            p = pred_map[code]
            snap.append({
                "code": code, "name": r.get("name"),
                "price": r.get("price"), "pct": r.get("pct"),
                "T1": p.get("T1", "--"), "T3": p.get("T3", "--"),
                "confidence": p.get("confidence", 0.0),
                "signal": p.get("signal", "--")
            })
    return snap
