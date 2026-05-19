"""Real financial news service for Glimmora MacroMind.

Fetches live financial news from free RSS feeds using feedparser.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from typing import Optional

import feedparser

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------
_news_cache: dict = {"articles": [], "ts": 0}
_CACHE_TTL = 300  # 5 minutes

# ---------------------------------------------------------------------------
# RSS Feed Sources
# ---------------------------------------------------------------------------
RSS_FEEDS: list[dict[str, str]] = [
    {
        "url": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB",
        "source": "Google Finance",
    },
    {
        "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114",
        "source": "CNBC",
    },
    {
        "url": "https://finance.yahoo.com/news/rssindex",
        "source": "Yahoo Finance",
    },
    {
        "url": "https://feeds.marketwatch.com/marketwatch/topstories/",
        "source": "MarketWatch",
    },
    {
        "url": "https://www.investing.com/rss/news.rss",
        "source": "Investing.com",
    },
]

# ---------------------------------------------------------------------------
# Category keywords
# ---------------------------------------------------------------------------
_CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "monetary_policy": ["fed", "rate", "central bank", "monetary", "interest rate", "fomc", "ecb", "boj"],
    "markets": ["stock", "market", "dow", "s&p", "nasdaq", "shares", "rally", "selloff", "wall street", "equity"],
    "commodities": ["oil", "gold", "commodity", "mining", "copper", "silver", "crude", "natural gas", "wheat"],
    "geopolitical": ["war", "sanction", "trade", "tariff", "geopolitical", "conflict", "diplomacy", "treaty", "embargo"],
    "crypto": ["bitcoin", "crypto", "blockchain", "ethereum", "token", "defi", "nft"],
}


def _categorize(title: str, summary: str) -> str:
    """Auto-categorize a news article based on keyword matching."""
    text = f"{title} {summary}".lower()
    for category, keywords in _CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return category
    return "corporate"


def _parse_published(entry: dict) -> str:
    """Extract and normalise the published date from a feed entry."""
    published_parsed = entry.get("published_parsed")
    if published_parsed:
        try:
            dt = datetime(*published_parsed[:6], tzinfo=timezone.utc)
            return dt.isoformat()
        except Exception:
            pass
    # Fallback: try the raw string
    raw = entry.get("published") or entry.get("updated") or ""
    if raw:
        return raw
    return datetime.now(timezone.utc).isoformat()


def _clean_summary(entry: dict) -> str:
    """Extract a clean plain-text summary from a feed entry."""
    summary = entry.get("summary") or entry.get("description") or ""
    # Strip HTML tags (simple approach)
    import re
    summary = re.sub(r"<[^>]+>", "", summary)
    summary = summary.strip()
    # Truncate to 300 chars
    if len(summary) > 300:
        summary = summary[:297] + "..."
    return summary


def _title_similarity(a: str, b: str) -> bool:
    """Return True if two titles are similar enough to be considered duplicates."""
    a_lower = a.lower().strip()
    b_lower = b.lower().strip()
    if a_lower == b_lower:
        return True
    # Check if one is a substring of the other (at least 60% overlap)
    shorter = a_lower if len(a_lower) <= len(b_lower) else b_lower
    longer = b_lower if len(a_lower) <= len(b_lower) else a_lower
    if len(shorter) > 10 and shorter in longer:
        return True
    # Word-level overlap
    words_a = set(a_lower.split())
    words_b = set(b_lower.split())
    if not words_a or not words_b:
        return False
    overlap = len(words_a & words_b) / max(len(words_a), len(words_b))
    return overlap > 0.7


def _fetch_all_feeds() -> list[dict]:
    """Fetch articles from all RSS feeds."""
    all_articles: list[dict] = []

    for feed_info in RSS_FEEDS:
        url = feed_info["url"]
        source = feed_info["source"]
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.get("title", "").strip()
                if not title:
                    continue
                summary = _clean_summary(entry)
                article = {
                    "title": title,
                    "summary": summary,
                    "source": source,
                    "url": entry.get("link", ""),
                    "published": _parse_published(entry),
                    "category": _categorize(title, summary),
                }
                all_articles.append(article)
        except Exception as e:
            logger.warning(f"Failed to fetch RSS feed from {source} ({url}): {e}")

    return all_articles


def _deduplicate(articles: list[dict]) -> list[dict]:
    """Remove duplicate articles based on title similarity."""
    unique: list[dict] = []
    for article in articles:
        is_dup = False
        for existing in unique:
            if _title_similarity(article["title"], existing["title"]):
                is_dup = True
                break
        if not is_dup:
            unique.append(article)
    return unique


def _sort_by_date(articles: list[dict]) -> list[dict]:
    """Sort articles by published date, newest first."""

    def _sort_key(article: dict) -> str:
        return article.get("published", "")

    return sorted(articles, key=_sort_key, reverse=True)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def fetch_financial_news(limit: int = 20) -> list[dict]:
    """Fetch latest financial news from multiple RSS feeds.

    Results are cached for 5 minutes to avoid hammering upstream feeds.
    """
    now = time.time()

    # Return cached data if still fresh
    if _news_cache["articles"] and now - _news_cache["ts"] < _CACHE_TTL:
        return _news_cache["articles"][:limit]

    # Fetch from all feeds
    all_articles = _fetch_all_feeds()

    # Deduplicate
    articles = _deduplicate(all_articles)

    # Sort newest first
    articles = _sort_by_date(articles)

    # Update cache
    _news_cache["articles"] = articles
    _news_cache["ts"] = now

    return articles[:limit]


def fetch_market_alerts() -> list[str]:
    """Generate market alerts from recent news headlines.

    Returns the top 5 most relevant headlines formatted as alert strings.
    """
    articles = fetch_financial_news(limit=50)

    # Prioritise non-corporate categories as they tend to be more market-moving
    priority_categories = ["monetary_policy", "geopolitical", "markets", "commodities", "crypto"]
    priority_articles = [a for a in articles if a["category"] in priority_categories]
    remaining = [a for a in articles if a["category"] not in priority_categories]

    # Take from priority first, then fill with remaining
    selected = (priority_articles + remaining)[:5]

    alerts: list[str] = []
    for article in selected:
        alerts.append(f"[{article['source']}] {article['title']}")

    return alerts


def search_news(query: str, limit: int = 10) -> list[dict]:
    """Search news articles for a specific topic.

    Filters by query keywords present in title or summary.
    """
    articles = fetch_financial_news(limit=50)
    query_lower = query.lower()
    query_words = query_lower.split()

    matched: list[dict] = []
    for article in articles:
        text = f"{article['title']} {article['summary']}".lower()
        # Match if any query word appears in text
        if any(word in text for word in query_words):
            matched.append(article)

    return matched[:limit]
