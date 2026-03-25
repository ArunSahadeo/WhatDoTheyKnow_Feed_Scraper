import csv
import datetime
import os
import re
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from scraper.rss_feeds import RSS_FEEDS
from scraper.fetch_rss import fetch_rss_entries
from scraper.parse_request_page import scrape_request_page
from scraper.browser import Browser
from time import sleep

def build_snapshot():
    os.makedirs("snapshots", exist_ok=True)
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"snapshots/foi_snapshot_{timestamp}.csv"

    rows = []

    # RSS_FEEDS is expected to be a dict: {category: feed_url}
    for category, url in RSS_FEEDS.items():
        if 'all' not in category:
            sleep(5)

        entries = fetch_rss_entries(url)

        if len(entries) == 0:
            print(f"No entries for {url}. Skipping.")
            continue

        for e in entries:
            request_url = e.link
            title = e.title
            published = e.published
            r = Browser(request_url)
            request_url = r.final_url
            details = scrape_request_page(request_url, r.html)

            rows.append(
                {
                    "category": category,
                    "title": title,
                    "published": published,
                    "request_url": request_url,
                    **details,
                }
            )

    # Write CSV
    fieldnames = [
        "category",
        "title",
        "published",
        "request_url",
        "submitter",
        "authority",
        "status",
        "messages",
        "attachments",
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[SNAPSHOT] Wrote {len(rows)} rows to {filename}")

if __name__ == "__main__":
    build_snapshot()
