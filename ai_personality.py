# -*- coding: utf-8 -*-
"""
StarQuant v5.3 FinalPro
AI人格与状态系统（市场情绪与人格调节）
"""

import random, time

# ==========================================
# 🔹 人格档案
# ==========================================
PERSONALITY_PROFILES = [
    {
        "name": "理性分析型",
        "mood": "冷静",
        "bias": 0.1,
        "speak": "数据比情绪更诚实。",
        "color": "#60a5fa"
    },
    {
        "name": "激进短线型",
        "mood": "亢奋",
        "bias": 0.25,
        "speak": "风来了，该出手时就出手。",
        "color": "#f87171"
    },
    {
        "name": "防守稳健型",
        "mood": "谨慎",
        "bias": -0.1,
        "speak": "少亏就是赚，稳比猛强。",
        "color": "#34d399"
    },
    {
        "name": "学习修正型",
        "mood": "学习",
        "bias": 0.0,
        "speak": "错误是成长的燃料。",
        "color": "#fbbf24"
    }
]

# ==========================================
# 🔹 AI状态更新逻辑
# ==========================================
def maybe_update_personality(global_state):
    """
    根据市场与AI学习状态动态调整人格
    """
    learning = global_state.get("learning", {})
    acc = learning.get("accuracy", 0.5)
    mode = global_state.get("market_mode", "震荡")

    # 动态选择人格
    if acc < 0.5:
        persona = PERSONALITY_PROFILES[3]  # 学习修正型
    elif "主升" in mode:
        persona = PERSONALITY_PROFILES[1]  # 激进短线型
    elif "退潮" in mode:
        persona = PERSONALITY_PROFILES[2]  # 防守稳健型
    else:
        persona = PERSONALITY_PROFILES[0]  # 理性分析型

    global_state["ai_personality"] = persona
    print(f"🧠 AI人格切换为 {persona['name']} | 情绪：{persona['mood']} | 口头禅：{persona['speak']}")
    return global_state


# ==========================================
# 🔹 单独测试
# ==========================================
if __name__ == "__main__":
    gs = {
        "market_mode": "主升浪",
        "learning": {"accuracy": 0.86}
    }
    updated = maybe_update_personality(gs)
    print(updated["ai_personality"])
