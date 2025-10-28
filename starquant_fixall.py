# -*- coding: utf-8 -*-
"""
StarQuant v5.3 FinalPro - 一键系统修复与自动升级工具
作者：GPT 修复版
"""

import os, importlib, json, re, tempfile, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(ROOT, "_backup")
os.makedirs(BACKUP_DIR, exist_ok=True)

def backup_file(path):
    if os.path.exists(path):
        shutil.copy2(path, os.path.join(BACKUP_DIR, os.path.basename(path)))

def safe_read(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        try:
            with open(path, "r", encoding="gbk") as f:
                return f.read()
        except Exception as e:
            print("⚠️ 读取失败", path, e)
            return ""

def safe_write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def patch_function_signature(file_path, pattern, replacement):
    text = safe_read(file_path)
    if pattern in text:
        text = text.replace(pattern, replacement)
        safe_write(file_path, text)
        print(f"✅ 修复函数签名: {os.path.basename(file_path)}")
    return text

def ensure_search_api(file_path):
    text = safe_read(file_path)
    if "/api/search" not in text:
        print(f"⚙️ 注入 /api/search 接口: {os.path.basename(file_path)}")
        add_code = """
@_app.route("/api/search")
def api_search():
    q = (request.args.get("q", "") or "").lower()
    s = _STATE or {}
    data = s.get("market_data", [])
    return jsonify([r for r in data if q in str(r.get("name","")).lower() or q in str(r.get("code",""))][:20])
"""
        safe_write(file_path, text.strip() + "\n" + add_code)
    return text

def fix_voice_path(file_path):
    text = safe_read(file_path)
    if "C:\\\\StarQuant\\\\voice_ai.mp3" in text:
        new = "os.path.join(tempfile.gettempdir(), 'voice_ai.mp3')"
        text = re.sub(r"\"C:\\\\StarQuant\\\\voice_ai\.mp3\"", new, text)
        safe_write(file_path, text)
        print(f"✅ 修复语音路径: {os.path.basename(file_path)}")

def update_ai_memory():
    mem_path = os.path.join(ROOT, "ai_memory.json")
    default = {"version": "v5.3+AutoFix", "history": [], "weights": {}}
    try:
        if not os.path.exists(mem_path):
            with open(mem_path, "w", encoding="utf-8") as f:
                json.dump(default, f, ensure_ascii=False, indent=2)
        else:
            with open(mem_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["version"] = "v5.3+AutoFix"
            with open(mem_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        print("✅ AI记忆文件已升级版本。")
    except Exception as e:
        print("⚠️ 无法更新AI记忆:", e)

def main():
    print("🚀 StarQuant 一键修复启动中...")
    targets = [
        "ai_predict_engine.py",
        "policy_fusion_v24.py",
        "ai_stock_query.py",
        "web_server.py",
        "voice_output.py",
    ]

    for t in targets:
        path = os.path.join(ROOT, t)
        if not os.path.exists(path):
            print(f"❌ 缺失文件: {t}")
            continue
        backup_file(path)
        txt = safe_read(path)

        # 修AI预测参数数量
        if "def run_ai_predict(" in txt and "ai_mem" not in txt:
            patch_function_signature(path, "def run_ai_predict(", "def run_ai_predict(market_data, news_data=None, ai_mem=None):")

        # 修policy新闻limit参数
        if "def get_policy_news(" in txt and "limit" not in txt:
            patch_function_signature(path, "def get_policy_news(", "def get_policy_news(limit=20):")

        # 修语音路径
        if "voice_ai.mp3" in txt:
            fix_voice_path(path)

        # 确保web_server有搜索接口
        if "web_server" in t:
            ensure_search_api(path)

    update_ai_memory()
    print("\n✅ 修复任务完成。现在可运行:  python main_starquant.py")
    print("系统已备份原文件至 _backup 文件夹。")

if __name__ == "__main__":
    main()
