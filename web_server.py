# -*- coding: utf-8 -*-
"""
StarQuant v5.3 FinalPro
Web服务模块 - 接口整合修复版（最终版）
"""

from flask import Flask, jsonify, request, send_from_directory
import threading, os
from data_fetcher import get_realtime_data
from policy_fusion_v25 import get_policy_news

app = Flask(__name__, static_folder="static", template_folder="templates")

# ===== 全局状态 =====
GLOBAL_STATE = {}
_LOCK = threading.Lock()

def set_global_state(state):
    global GLOBAL_STATE
    with _LOCK:
        GLOBAL_STATE = state.copy()

def get_global_state():
    with _LOCK:
        return GLOBAL_STATE.copy()


# ===== 页面入口 =====
@app.route("/")
def index():
    return send_from_directory("templates", "index_starquant.html")


# ===== 实时数据接口 =====
@app.route("/api/data")
def api_data():
    s = get_global_state()
    payload = {
        "market": s.get("market_data", []),
        "market_data": s.get("market_data", []),
        "predictions": s.get("predictions", []),
        "board": s.get("board_suggestions", []),
        "board_suggestions": s.get("board_suggestions", []),
        "news": s.get("news_data", []),
        "news_data": s.get("news_data", []),
        "copy_text": s.get("copy_text", ""),
        "learning": s.get("learning", {}),
        "status": s.get("market_status", {}),
        "update_time": s.get("update_time", "--"),
        "market_mode": s.get("market_mode", "未知"),
        "watchlist": s.get("watchlist", []),
    }
    return jsonify(payload)


# ===== 搜索接口（修复缩进） =====
@app.route("/api/search")
def api_search():
    q = (request.args.get("q", "") or "").strip()
    if not q:
        return jsonify({"results": []})

    kw = q.lower()
    data = get_realtime_data(limit=3000)  # 放大样本避免截断
    results = []
    for d in data:
        name = str(d.get("name", "")).lower()
        code = str(d.get("code", "")).lower()
        if kw in name or kw in code:
            results.append({
                "code": d.get("code"),
                "name": d.get("name"),
                "price": d.get("price"),
                "pct": d.get("pct"),
            })
    return jsonify({"results": results[:20]})


# ===== 添加自选股 =====
@app.route("/api/add", methods=["POST"])
def api_add():
    try:
        code = request.json.get("code")
        name = request.json.get("name")
        if not code:
            return jsonify({"error": "缺少代码"})
        with _LOCK:
            wl = GLOBAL_STATE.get("watchlist", [])
            if not any(i.get("code") == code for i in wl):
                wl.append({"code": code, "name": name})
                GLOBAL_STATE["watchlist"] = wl
        return jsonify({"ok": True, "watchlist": GLOBAL_STATE["watchlist"]})
    except Exception as e:
        return jsonify({"error": str(e)})


# ===== 删除自选股 =====
@app.route("/api/delete", methods=["POST"])
def api_delete():
    try:
        code = request.json.get("code")
        if not code:
            return jsonify({"error": "缺少代码"})
        with _LOCK:
            wl = GLOBAL_STATE.get("watchlist", [])
            wl = [i for i in wl if i.get("code") != code]
            GLOBAL_STATE["watchlist"] = wl
        return jsonify({"ok": True, "watchlist": wl})
    except Exception as e:
        return jsonify({"error": str(e)})


# ===== 新闻接口 =====
@app.route("/api/news")
def api_news():
    try:
        news = get_policy_news(limit=20)
        return jsonify({"news": news})
    except Exception as e:
        return jsonify({"error": str(e), "news": []})


# ===== 静态文件路径 =====
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, "static"), filename)


# ===== 启动Flask服务 =====
def run_flask_server():
    print("🌐 Flask WebServer 已启动 → http://127.0.0.1:8000")
    app.run(host="127.0.0.1", port=8000, debug=False, use_reloader=False)


if __name__ == "__main__":
    run_flask_server()
