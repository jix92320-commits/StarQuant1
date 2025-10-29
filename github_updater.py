# -*- coding: utf-8 -*-
"""
GitHub 自动检测与拉取更新（安全版）
- 手动触发：python -m github_updater --once
- 循环检测：python -m github_updater --loop --interval 3600
"""
import os, sys, json, subprocess, time
from urllib.request import Request, urlopen

REPO_OWNER = "jix92320-commits"
REPO_NAME  = "StarQuant1"
BRANCH     = "main"
API_URL    = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits/{BRANCH}"
STATE_FILE = "latest_commit.txt"

def _run(cmd: list) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    if p.returncode != 0:
        raise RuntimeError(f"cmd failed: {' '.join(cmd)}\n{p.stderr}")
    return p.stdout.strip()

def _get_remote_head_sha() -> str:
    req = Request(API_URL, headers={"User-Agent":"StarQuant-Updater"})
    with urlopen(req, timeout=15) as r:
        data = json.loads(r.read().decode("utf-8"))
    return data.get("sha") or data["commit"]["tree"]["sha"]

def _get_local_head_sha() -> str:
    try:
        return _run(["git", "rev-parse", "HEAD"])
    except Exception:
        return ""

def _read_state() -> str:
    if os.path.exists(STATE_FILE):
        try:
            return open(STATE_FILE, "r", encoding="utf-8").read().strip()
        except Exception:
            return ""
    return ""

def _write_state(sha: str):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(sha or "")

def check_and_update() -> dict:
    """返回: {'updated': bool, 'old': local, 'new': remote, 'changed_files': [...]}"""
    remote = _get_remote_head_sha()
    local  = _get_local_head_sha()
    saved  = _read_state()

    if remote in (local, saved):
        return {"updated": False, "old": local, "new": remote, "changed_files": []}

    # 先 fetch 再 diff 看看改了哪些
    _run(["git", "fetch", "origin", BRANCH])
    changed = _run(["git", "diff", "--name-only", f"{local}..origin/{BRANCH}"]).splitlines()

    # 可选：排除不希望自动覆盖的文件（示例）
    EXCLUDE = {"venv/", "__pycache__/"}
    changed = [p for p in changed if not any(p.startswith(x) for x in EXCLUDE)]

    # 拉取
    _run(["git", "pull", "origin", BRANCH])
    _write_state(remote)

    return {"updated": True, "old": local, "new": remote, "changed_files": changed}

def main():
    once = "--once" in sys.argv
    loop = "--loop" in sys.argv
    interval = 3600
    if "--interval" in sys.argv:
        try:
            idx = sys.argv.index("--interval")
            interval = int(sys.argv[idx+1])
        except Exception:
            pass

    if once:
        info = check_and_update()
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return

    if loop:
        while True:
            try:
                info = check_and_update()
                ts = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{ts}] updated={info['updated']} {info['old']} -> {info['new']}")
                if info["updated"]:
                    print("changed files:", info["changed_files"])
            except Exception as e:
                print("[updater] error:", e)
            time.sleep(interval)

if __name__ == "__main__":
    main()
