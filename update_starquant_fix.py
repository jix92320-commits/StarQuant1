import os, shutil, json, requests

print("🚀 StarQuant 智能修复程序启动中...")

# === 1. 修复 voice_output 路径问题 ===
voice_file = "voice_output.py"
if os.path.exists(voice_file):
    with open(voice_file, "r", encoding="utf-8") as f:
        content = f.read()
    if "Temp" in content:
        content = content.replace("Temp", "StarQuant")
        with open(voice_file, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ 已修复 voice_output 路径问题。")

# === 2. 修复行情接口错误回退 ===
fetcher = "data_fetcher.py"
if os.path.exists(fetcher):
    with open(fetcher, "r", encoding="utf-8") as f:
        text = f.read()
    if "stock_zh_a_spot_em" in text:
        text = text.replace(
            "ak.stock_zh_a_spot_em()",
            "ak.stock_zh_a_spot_em() if hasattr(ak, 'stock_zh_a_spot_em') else None"
        )
        with open(fetcher, "w", encoding="utf-8") as f:
            f.write(text)
        print("✅ 已添加行情源容错逻辑。")

# === 3. 检查 policy_fusion_v24 ===
if not os.path.exists("policy_fusion_v24.py"):
    print("⚠️ 缺失 policy_fusion_v24.py，自动下载中...")
    url = "https://raw.githubusercontent.com/jix92320-commits/StarQuant1/main/policy_fusion_v24.py"
    r = requests.get(url)
    if r.status_code == 200:
        with open("policy_fusion_v24.py", "w", encoding="utf-8") as f:
            f.write(r.text)
        print("✅ 已恢复 policy_fusion_v24.py 文件。")

print("🌟 所有修复已完成，请运行：python main_starquant.py")
