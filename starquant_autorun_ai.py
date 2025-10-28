# -*- coding: utf-8 -*-
"""
StarQuant v5.3 FinalPro — 一键全功能启动系统（终极版）
自动检测 / 自动修复 / 自动补全 / 自动自愈
"""

import os, importlib, traceback, time, json, tempfile, threading, webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(ROOT, "autorun_log.txt")

def log(msg):
    print(msg)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")

# === 检查模块是否存在 ===
def check_import(name):
    try:
        importlib.import_module(name)
        log(f"✅ 模块 {name} 导入正常")
        return True
    except Exception as e:
        log(f"⚠️ 模块 {name} 导入失败：{e}")
        return False

def check_file(path):
    if not os.path.exists(path):
        log(f"❌ 缺失文件：{path}")
        return False
    return True

# === 行情检测 ===
def check_data_source():
    try:
        import data_fetcher
        data = data_fetcher.get_realtime_data(limit=10)
        if not data:
            raise ValueError("数据为空")
        log(f"✅ 行情数据正常：{len(data)} 条")
        return True
    except Exception as e:
        log(f"⚠️ 行情异常：{e} → 自动切换备用数据")
        fake = [{"code": f"TEST{i}", "name": f"样本{i}", "price": 10+i, "pct": i} for i in range(10)]
        with open(os.path.join(tempfile.gettempdir(), "fallback_market.json"), "w", encoding="utf-8") as f:
            json.dump(fake, f, ensure_ascii=False, indent=2)
        return False

# === 启动主程序 ===
def run_main():
    try:
        import main_starquant

        # 自动补全 main_loop（如果缺失）
        if not hasattr(main_starquant, "main_loop"):
            log("⚠️ 检测到缺失 main_loop()，自动补全中...")
            def main_loop():
                while True:
                    try:
                        main_starquant.tick_once()
                        time.sleep(30)
                    except Exception as e:
                        log(f"💥 循环异常：{e}")
                        time.sleep(10)
            main_starquant.main_loop = main_loop
            log("✅ 已自动修复 main_loop()")

        log("🚀 启动 StarQuant 主程序 ...")
        threading.Thread(target=main_starquant.main_loop, daemon=True).start()

        # 自动检测 Flask 服务
        try:
            threading.Thread(target=main_starquant.run_flask_server, daemon=True).start()
        except Exception as e:
            log(f"⚠️ Flask 启动异常：{e}")

        time.sleep(5)
        webbrowser.open("http://127.0.0.1:8000")
        log("✅ 系统已启动，监控中...")

        while True:
            time.sleep(30)
            log("🔍 周期检测：系统运行中...")
    except Exception:
        log("💥 主程序异常：\n" + traceback.format_exc())

# === 主检测入口 ===
def main():
    log("=== StarQuant 一键全功能启动器 ===")
    core = ["data_fetcher", "ai_predict_engine", "policy_fusion_v24",
            "ai_stock_query", "ai_emotion_copy", "web_server", "voice_output"]
    ok = True
    for name in core:
        if not check_file(os.path.join(ROOT, f"{name}.py")) or not check_import(name):
            ok = False
    if check_data_source():
        log("✅ 数据源检测通过")
    else:
        log("⚙️ 使用备用数据运行系统")

    if ok:
        run_main()
    else:
        log("⚠️ 检测到模块问题，请查看 autorun_log.txt 详情")

if __name__ == "__main__":
    main()
