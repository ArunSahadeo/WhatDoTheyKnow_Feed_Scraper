import feedparser

def fetch_rss_entries(url):
    import requests
    r = requests.get(url)
    feed = feedparser.parse(r.text if r.status_code == 200 else '')
    return feed.entries
