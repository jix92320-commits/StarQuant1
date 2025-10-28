# -*- coding: utf-8 -*-
"""
StarQuant v5.3 FinalPro - 政策/新闻融合模块 v25
自动多源抓取 + 智能降噪 + 防阻塞机制
"""
import feedparser, time

NEWS_SOURCES = [
    "https://www.chinanews.com.cn/rss/scroll-news.xml",
    "https://rsshub.app/cailianpress/index",
    "https://rsshub.app/xueqiu/today",
    "https://36kr.com/feed",
]

def _try_fetch(url, limit=30):
    try:
        d = feedparser.parse(url)
        lst = []
        for e in d.entries[:limit]:
            title = e.get("title", "").strip()
            if not title: continue
            lst.append({"title": title, "link": e.get("link", ""), "source": url.split("/")[2]})
        return lst
    except Exception:
        return []

def get_policy_news(limit=30):
    all_news = []
    for url in NEWS_SOURCES:
        items = _try_fetch(url, limit)
        if items:
            print(f"✅ 新闻源成功: {url}")
            all_news.extend(items)
        else:
            print(f"⚠️ 超时: {url}")
        time.sleep(0.3)
    if not all_news:
        return [{"title": "暂无政策新闻，请稍后刷新"}]
    return all_news[:limit]


# ---------------- 主函数 ----------------
def get_policy_news(limit=30):
    """
    自动轮询有效新闻源，优先国内源
    """
    all_news = []
    for url in NEWS_SOURCES:
        items = _try_fetch(url, limit)
        if items:
            print(f"✅ 已加载新闻源：{url}")
            all_news.extend(items)
        else:
            print(f"⚠️ 跳过失效源：{url}")
        time.sleep(0.3)

    # 去重 + 截取
    titles = set()
    unique_news = []
    for n in all_news:
        if n["title"] not in titles:
            titles.add(n["title"])
            unique_news.append(n)

    if not unique_news:
        unique_news = [{"title": "暂无政策新闻（所有源均超时）"}]

    return unique_news[:limit]
