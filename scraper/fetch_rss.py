import feedparser

def fetch_rss_entries(url):
    feed = feedparser.parse(url)
    return feed.entries
