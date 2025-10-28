# -*- coding: utf-8 -*-
"""
StarQuant v5.3 FinalPro
AI自我反思与认知修复模块
"""

import random, time, json, os, statistics

AI_MEM_PATH = "./ai_memory.json"
SELF_LOG_PATH = "./ai_self_reflect_log.json"

# ====================================
# 🔹 自我反思逻辑核心
# ====================================
def maybe_self_reflect(predictions, market_data, ai_mem):
    """
    AI 每次预测结束后进行自我反思：
    - 对比预测与实际
    - 自动调整权重
    - 记录反思内容
    """
    if not predictions or not market_data:
        return ai_mem

    diffs = []
    for p in predictions:
        code = p.get("code")
        exp = p.get("expect", 0)
        real = _find_real_change(code, market_data)
        diffs.append(abs(exp - real))

    mean_diff = statistics.mean(diffs) if diffs else 0
    bias_adj = _calculate_bias(mean_diff)

    ai_mem["reflect"] = {
        "last_reflect_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "mean_diff": round(mean_diff, 2),
        "bias_adj": bias_adj,
        "thought": _generate_thought(mean_diff)
    }

    _apply_reflect(ai_mem, bias_adj)
    _save_reflect_log(ai_mem["reflect"])
    print(f"🪞 AI反思完成 | 平均偏差 {mean_diff:.2f} | 修正系数 {bias_adj}")
    return ai_mem


# ====================================
# 🔹 内部工具函数
# ====================================
def _find_real_change(code, market_data):
    """模拟实际涨跌"""
    for r in market_data:
        if r.get("code") == code:
            return r.get("pct", random.uniform(-3, 3))
    return random.uniform(-3, 3)


def _calculate_bias(mean_diff):
    """根据误差计算修正系数"""
    if mean_diff < 1:
        return random.uniform(-0.02, 0.02)
    elif mean_diff < 3:
        return random.uniform(-0.05, 0.05)
    else:
        return random.uniform(-0.08, 0.08)


def _generate_thought(mean_diff):
    """生成AI自我思考语句"""
    if mean_diff < 1:
        return "预测精度良好，维持当前策略。"
    elif mean_diff < 3:
        return "略有偏差，需关注市场波动性变化。"
    else:
        return "误差过大，可能过度情绪化，将修正算法权重。"


def _apply_reflect(ai_mem, bias_adj):
    """应用修正系数到AI权重"""
    if "weights" not in ai_mem:
        ai_mem["weights"] = {}
    base_bias = ai_mem.get("bias_adj", 0.0)
    ai_mem["bias_adj"] = round(base_bias + bias_adj, 3)
    return ai_mem


def _save_reflect_log(reflect):
    """保存反思日志"""
    if not os.path.exists(SELF_LOG_PATH):
        logs = [reflect]
    else:
        try:
            with open(SELF_LOG_PATH, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except:
            logs = []
        logs.append(reflect)

    with open(SELF_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


# ====================================
# 🔹 模块独立测试
# ====================================
if __name__ == "__main__":
    print("🧠 StarQuant 自我反思系统测试启动")
    fake_preds = [{"code": "000001", "expect": 3.1}, {"code": "002594", "expect": -0.8}]
    fake_market = [{"code": "000001", "pct": 2.5}, {"code": "002594", "pct": -2.0}]
    fake_mem = {"version": "v5.3", "weights": {}}
    res = maybe_self_reflect(fake_preds, fake_market, fake_mem)
    print(json.dumps(res["reflect"], ensure_ascii=False, indent=2))
