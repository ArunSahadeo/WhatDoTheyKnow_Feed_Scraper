import feedparser

def fetch_rss_entries(url):
    feed = feedparser.parse(url)
    print(f"The feed data: {feed.feeddata}")
    print(f"The feed entries: {feed.entries}")
    print(f"The feed version: {feed.version}")
    print(f"The feed namespaces: {feed.namespaces}")
    return feed.entries
