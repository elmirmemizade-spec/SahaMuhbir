import feedparser
from datetime import datetime, timedelta, timezone
from config import RSS_FEEDS


def fetch_all_feeds(hours=24):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    all_entries = []

    for source_name, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                published = _parse_date(entry)
                if published and published >= cutoff:
                    all_entries.append({
                        "source": source_name,
                        "title": entry.get("title", ""),
                        "summary": entry.get("summary", entry.get("description", "")),
                        "link": entry.get("link", ""),
                        "published": published.isoformat(),
                    })
        except Exception as e:
            print(f"[WARN] {source_name} alinamadi: {e}")

    all_entries.sort(key=lambda x: x["published"], reverse=True)
    return all_entries


def _parse_date(entry):
    for key in ("published_parsed", "updated_parsed"):
        parsed = entry.get(key)
        if parsed:
            try:
                from time import mktime
                return datetime.fromtimestamp(mktime(parsed), tz=timezone.utc)
            except Exception:
                continue
    return None
