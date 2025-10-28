# -*- coding: utf-8 -*-
import random, datetime

def _safe_decode(x):
    if isinstance(x, bytes):
        for enc in ("utf-8", "gbk", "latin1"):
            try:
                return x.decode(enc, errors="ignore")
            except Exception:
                continue
        return ""
    return x if isinstance(x, str) else str(x)

def generate_emotional_copy(preds, news, state):
    try:
        preds = [{k: _safe_decode(v) if isinstance(v, bytes) else v for k, v in (p or {}).items()} for p in (preds or [])]
        news  = [{k: _safe_decode(v) if isinstance(v, bytes) else v for k, v in (n or {}).items()} for n in (news  or [])]
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if not preds:
            return f"⏱ {now} | AI 正在观察市场，等待更多信号……"

        focus = random.sample(preds, min(3, len(preds)))
        lines = [f"📊 AI市况简报 {now}"]
        for p in focus:
            code = p.get("code","--"); name = p.get("name","--")
            sig  = p.get("signal","观望"); conf = float(p.get("confidence",0))
            t1   = p.get("t1") or p.get("T1") or "--"
            t3   = p.get("t3") or p.get("T3") or "--"
            lines.append(f"{code} {name} → {sig}｜置信 {conf:.2f}｜T+1:{t1}｜T+3:{t3}")

        if news:
            title = _safe_decode(news[0].get("title",""))
            lines.append(f"📰 资讯：{title}")

        lines.append(f"💡 建议：{random.choice(['稳健为主','轻仓试探','耐心等待','逢低布局'])}")
        return "\n".join(lines)
    except Exception as e:
        print("⚠️ 文案异常（已忽略）：", e)
        return "AI文案生成暂不可用。"
