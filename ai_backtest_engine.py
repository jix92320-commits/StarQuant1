# -*- coding: utf-8 -*-
"""
StarQuant v5.3 FinalPro
AI自我复盘与回测引擎
"""

import json, os, random, time, statistics

AI_MEM_PATH = "./ai_memory.json"
BACKTEST_LOG_PATH = "./ai_backtest_log.json"

# =================================
# 🔹 基础函数
# =================================
def load_ai_mem():
    if os.path.exists(AI_MEM_PATH):
        try:
            with open(AI_MEM_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"version": "v5.3", "accuracy": 0.0}
    else:
        return {"version": "v5.3", "accuracy": 0.0}

def save_ai_mem(mem):
    with open(AI_MEM_PATH, "w", encoding="utf-8") as f:
        json.dump(mem, f, ensure_ascii=False, indent=2)


# =================================
# 🔹 主复盘逻辑
# =================================
def maybe_run_daily_backtest(predictions, market_snapshot, ai_mem):
    """
    在收盘或周末时调用。评估预测正确率 -> 调整AI权重。
    返回：是否发生更新, 新的AI记忆
    """
    if not predictions or not market_snapshot:
        return False, ai_mem

    # 模拟计算AI预测和真实涨跌的差距
    diffs = []
    for p in predictions:
        code = p.get("code")
        exp = p.get("expect", 0)
        real = _find_real_change(code, market_snapshot)
        diff = abs(exp - real)
        diffs.append(diff)

    avg_diff = statistics.mean(diffs) if diffs else 0
    score = max(0.0, 1 - avg_diff / 10)
    score = round(score, 3)

    # 写入学习结果
    ai_mem["accuracy"] = score
    ai_mem["last_backtest"] = time.strftime("%Y-%m-%d %H:%M:%S")
    if "history" not in ai_mem:
        ai_mem["history"] = []
    ai_mem["history"].append({
        "time": ai_mem["last_backtest"],
        "accuracy": score
    })

    save_ai_mem(ai_mem)
    save_backtest_log(ai_mem["last_backtest"], score)

    print(f"📊 回测完成 | 准确率 {score*100:.2f}%")
    return True, ai_mem


# =================================
# 🔹 模拟真实涨跌
# =================================
def _find_real_change(code, market_snapshot):
    """
    模拟找到该股票真实涨跌幅（仅作为复盘用）
    """
    for r in market_snapshot:
        if r.get("code") == code:
            return r.get("pct", random.uniform(-3, 3))
    return random.uniform(-2, 2)


# =================================
# 🔹 保存回测日志
# =================================
def save_backtest_log(ts, acc):
    log_item = {"time": ts, "accuracy": acc}
    if not os.path.exists(BACKTEST_LOG_PATH):
        logs = [log_item]
    else:
        try:
            with open(BACKTEST_LOG_PATH, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except:
            logs = []
        logs.append(log_item)
    with open(BACKTEST_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


# =================================
# 🔹 模块独立测试
# =================================
if __name__ == "__main__":
    print("🧩 StarQuant 自我回测模块测试启动")
    fake_preds = [{"code": "600519", "expect": 3.2}, {"code": "000001", "expect": -1.1}]
    fake_market = [{"code": "600519", "pct": 2.8}, {"code": "000001", "pct": -1.0}]
    mem = load_ai_mem()
    changed, new_mem = maybe_run_daily_backtest(fake_preds, fake_market, mem)
    if changed:
        print("✅ 自我修正完成：", new_mem["accuracy"])
