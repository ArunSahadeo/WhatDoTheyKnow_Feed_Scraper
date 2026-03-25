import feedparser

def fetch_rss_entries(url):
    import requests
    r = requests.get(url)
    feed = feedparser.parse(r.text if r.status_code == 200 else '')

    if r.status_code != 200:
        import base64
        content = base64.b64encode(r.text.encode())
        print(f"The base64-encoded content from {url}: {content}")

    return feed.entries
