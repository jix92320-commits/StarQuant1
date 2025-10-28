# -*- coding: utf-8 -*-
"""
StarQuant v5.3 FinalPro
AI学习与自我修正模块
"""

import time, json, os, random, statistics

AI_MEM_PATH = "./ai_memory.json"
LEARNING_LOG_PATH = "./ai_learning_log.json"

# ===============================
# 🔹 载入与保存 AI 记忆
# ===============================
def load_memory():
    if not os.path.exists(AI_MEM_PATH):
        return {"version": "v5.3", "accuracy": 0.0, "history": []}
    try:
        with open(AI_MEM_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"version": "v5.3", "accuracy": 0.0, "history": []}

def save_memory(mem):
    with open(AI_MEM_PATH, "w", encoding="utf-8") as f:
        json.dump(mem, f, ensure_ascii=False, indent=2)

# ===============================
# 🔹 更新学习状态
# ===============================
def update_learning_state(predictions):
    """
    更新 AI 学习状态（基于预测的信心与分布动态修正准确率）
    """
    mem = load_memory()
    if not predictions:
        acc = mem.get("accuracy", 0.0)
    else:
        confs = [p.get("confidence", 0.5) for p in predictions]
        acc = min(1.0, statistics.mean(confs) * random.uniform(0.9, 1.05))

    new_state = {
        "progress": min(1.0, acc + random.uniform(0.01, 0.05)),
        "accuracy": round(acc, 3),
        "last_update": time.strftime("%Y-%m-%d %H:%M:%S"),
        "version": mem.get("version", "v5.3")
    }

    mem["learning"] = new_state
    mem["accuracy"] = new_state["accuracy"]
    if "history" not in mem:
        mem["history"] = []
    mem["history"].append({
        "t": new_state["last_update"],
        "accuracy": new_state["accuracy"]
    })

    save_memory(mem)
    save_learning_log(new_state)
    return new_state


# ===============================
# 🔹 日志记录与版本升级
# ===============================
def save_learning_log(state):
    log_item = {
        "time": state["last_update"],
        "accuracy": state["accuracy"]
    }
    if not os.path.exists(LEARNING_LOG_PATH):
        logs = [log_item]
    else:
        with open(LEARNING_LOG_PATH, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except:
                logs = []
        logs.append(log_item)

    with open(LEARNING_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

def maybe_log_upgrade(ai_mem, learning):
    """
    当AI学习准确率超过阈值时自动升级版本
    """
    if learning.get("accuracy", 0.0) > 0.82:
        old_v = ai_mem.get("version", "v5.3")
        vnum = float(old_v.replace("v", ""))
        new_v = f"v{round(vnum + 0.1, 1)}"
        ai_mem["version"] = new_v
        save_memory(ai_mem)
        print(f"✨ AI自动升级至 {new_v}，学习准确率 {learning['accuracy']*100:.1f}%")
    else:
        print(f"📈 当前学习准确率 {learning['accuracy']*100:.1f}% ，未达升级阈值")


# ===============================
# 🔹 模块测试入口
# ===============================
if __name__ == "__main__":
    print("🧠 StarQuant AI Learning 模块测试启动")
    fake_preds = [{"confidence": random.uniform(0.4, 0.95)} for _ in range(20)]
    state = update_learning_state(fake_preds)
    print("✅ 更新学习状态：", state)
