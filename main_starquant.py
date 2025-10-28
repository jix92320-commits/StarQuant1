# -*- coding: utf-8 -*-
# --- 统一控制台编码，防止中文打印把主循环打断 ---
import sys, io
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="ignore")
    sys.stderr.reconfigure(encoding="utf-8", errors="ignore")
except Exception:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="ignore")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="ignore")

"""
StarQuant v5.3 FinalPro
主控核心 - 全模块整合执行器（完整修复版）
"""
import time, threading, webbrowser
from data_fetcher import get_realtime_data, get_time_status, normalize_keys
from policy_fusion_v25 import get_policy_news
from ai_stock_query import apply_watchlist_actions, get_watchlist_snapshot, get_board_suggestions
from ai_predict_engine import run_ai_predict, load_ai_memory, save_ai_memory
from ai_learning import update_learning_state
from ai_personality import maybe_update_personality
from ai_self_reflect import maybe_self_reflect
from ai_emotion_copy import generate_emotional_copy
from web_server import run_flask_server, set_global_state
from voice_output import speak_text

# ========== 全局状态 ==========
GLOBAL_STATE = {
    "market_status": {"status": "初始化", "phase": "INIT", "now": ""},
    "market_data": [],
    "predictions": [],
    "board_suggestions": [],
    "news_data": [],
    "copy_text": "",
    "learning": {"accuracy": 0.0, "progress": 0.0, "version": "v5.3"},
    "market_mode": "未知",
    "update_time": "--:--:--"
}

AI_MEM = load_ai_memory()
_TICK_LOCK = threading.Lock()

# ========== 主循环函数 ==========
def tick_once():
    global GLOBAL_STATE
    with _TICK_LOCK:
        try:
            print("\n🧠 [AI] 正在更新行情、预测与新闻...")

            # 1️⃣ 市场状态
            GLOBAL_STATE["market_status"] = get_time_status()

            # 2️⃣ 行情
            try:
                data = get_realtime_data(limit=100)
                data = normalize_keys(data)
                GLOBAL_STATE["market_data"] = data
                print(f"✅ 行情刷新完成 {len(data)} 条")
            except Exception as e:
                print("❌ 行情错误:", e)

            # 3️⃣ 新闻
            try:
                news = get_policy_news(limit=30)
                GLOBAL_STATE["news_data"] = news
                print(f"✅ 新闻更新 {len(news)} 条")
            except Exception as e:
                print("❌ 新闻错误:", e)

            # 4️⃣ AI预测
            try:
                preds = run_ai_predict(GLOBAL_STATE["market_data"], GLOBAL_STATE["news_data"], AI_MEM)
                GLOBAL_STATE["predictions"] = preds
                print(f"✅ AI预测完成 {len(preds)} 条")
            except Exception as e:
                print("❌ 预测错误:", e)

            # 5️⃣ 打板推荐
            try:
                boards = get_board_suggestions(GLOBAL_STATE["predictions"], topk=10)
                GLOBAL_STATE["board_suggestions"] = boards
            except Exception as e:
                print("❌ 打板错误:", e)

            # 6️⃣ AI文案
            try:
                text = generate_emotional_copy(GLOBAL_STATE["predictions"], GLOBAL_STATE["news_data"], GLOBAL_STATE)
                GLOBAL_STATE["copy_text"] = text
                if text:
                    speak_text(text[:150])
            except Exception as e:
                print("❌ 文案错误:", e)

            # 7️⃣ 学习状态
            try:
                learn = update_learning_state(GLOBAL_STATE["predictions"])
                GLOBAL_STATE["learning"] = learn
            except Exception as e:
                print("❌ 学习状态错误:", e)

            # 8️⃣ 保存记忆
            save_ai_memory(AI_MEM)

            # 9️⃣ 更新时间
            GLOBAL_STATE["update_time"] = time.strftime("%Y-%m-%d %H:%M:%S")

            # 🔟 同步状态
            set_global_state(GLOBAL_STATE)
            print("🟢 GLOBAL_STATE 同步完成。")

        except Exception as e:
            print(f"💥 tick_once 异常: {e}")


# ========== 启动入口 ==========
def run_main_loop():
    while True:
        tick_once()
        time.sleep(30)


if __name__ == "__main__":
    print("🚀 启动 StarQuant v5.3 FinalPro（稳定版）")
    set_global_state(GLOBAL_STATE)

    threading.Thread(target=run_main_loop, daemon=True).start()
    threading.Thread(target=run_flask_server, daemon=True).start()

    try:
        webbrowser.open("http://127.0.0.1:8000")
    except:
        pass

    while True:
        time.sleep(60)
