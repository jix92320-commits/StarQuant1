# -*- coding: utf-8 -*-
"""
StarQuant v5.3 FinalPro — AI预测引擎（最终稳版）
"""
import random, json, os, statistics, requests
from typing import List, Dict

AI_MEM_PATH = "C:\\StarQuant\\ai_memory.json"

def load_ai_memory() -> Dict:
    if not os.path.exists(AI_MEM_PATH):
        mem = {"version": "v5.3", "history": []}
        save_ai_memory(mem)
        return mem
    try:
        with open(AI_MEM_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"version": "v5.3", "history": []}

def save_ai_memory(mem: Dict):
    try:
        with open(AI_MEM_PATH, "w", encoding="utf-8") as f:
            json.dump(mem, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("⚠️ 保存AI记忆异常:", e)

def get_global_indicators() -> Dict:
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=SPX500USD", timeout=4).json()
        return {"SPX": float(r.get("price", 0))}
    except:
        return {"SPX": 0}

def run_ai_predict(market_data: List[Dict], news_data: List[Dict], ai_mem=None) -> List[Dict]:
    """AI预测主逻辑（真实行情 + 新闻热度 + 市场偏置）"""
    if not market_data:
        return []

    results = []
    avg_pct = statistics.mean([float(x.get("pct", 0)) for x in market_data if abs(float(x.get("pct", 0))) < 20]) or 0
    avg_amt = statistics.mean([float(x.get("amount", 0)) for x in market_data if float(x.get("amount", 0)) > 1e6]) or 1e6

    # 新闻情绪
    news_boost = 0
    if news_data:
        text = " ".join([n.get("title", "") for n in news_data])
        hot = sum(1 for w in ["利好","突破","创新","增长","订单","新高","上调"] if w in text)
        bad = sum(1 for w in ["下滑","亏损","负面","停牌","调查"] if w in text)
        news_boost = (hot - bad) * 0.2

    market_bias = avg_pct / 10 + news_boost

    for row in market_data[:80]:
        try:
            price = float(row.get("price", 0))
            pct = float(row.get("pct", 0))
            amt = float(row.get("amount", 0))
            if price <= 0 or abs(pct) > 20:
                continue

            # 算力逻辑
            strength = (pct / 2) + (amt / avg_amt) * 0.3 + market_bias
            expect = round(strength, 2)
            expect = max(-3, min(3, expect))
            conf = round(0.55 + abs(expect) / 10, 3)

            T1 = f"{round(price * (1 + expect / 200), 2)}~{round(price * (1 + expect / 120), 2)}"
            T3 = f"{round(price * (1 + expect / 100), 2)}~{round(price * (1 + expect / 70), 2)}"

            signal = (
                "强烈看多🚀" if expect > 1.5 else
                "看多" if expect > 0.3 else
                "观望" if -0.3 <= expect <= 0.3 else
                "谨慎" if expect > -1 else
                "看空⚠️"
            )

            results.append({
                "code": row.get("code"), "name": row.get("name"),
                "price": price, "T1": T1, "T3": T3,
                "expect": expect, "confidence": conf, "signal": signal
            })
        except Exception:
            continue

    print(f"✅ AI预测完成 {len(results)} 条（市场情绪: {round(market_bias,3)}）")
    return results
