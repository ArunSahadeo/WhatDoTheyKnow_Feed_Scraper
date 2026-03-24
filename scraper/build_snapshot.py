import csv
import datetime
from scraper.rss_feeds import RSS_FEEDS
from scraper.fetch_rss import fetch_rss_entries
from scraper.parse_request_page import scrape_request_page

def build_snapshot():
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"snapshots/foi_snapshot_{timestamp}.csv"

    rows = []

    for category, url in RSS_FEEDS.items():
        entries = fetch_rss_entries(url)

        for e in entries:
            request_url = e.link

            details = scrape_request_page(request_url)

            rows.append({
                "category": category,
                "title": e.title,
                "published": e.published,
                "request_url": request_url,
                **details
            })

    # Write CSV
    fieldnames = [
        "category", "title", "published", "request_url",
        "submitter", "authority", "status",
        "resolution_text", "attachments"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Snapshot written: {filename}")

