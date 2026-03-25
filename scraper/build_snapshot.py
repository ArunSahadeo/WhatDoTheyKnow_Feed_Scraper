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
from scraper.internet_archive import snapshot_url


def build_snapshot():
    os.makedirs("snapshots", exist_ok=True)
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"snapshots/foi_snapshot_{timestamp}.csv"

    rows = []

    # RSS_FEEDS is expected to be a dict: {category: feed_url}
    for category, url in RSS_FEEDS.items():
        print(f"[SNAPSHOT] Category: {category}")
        print(f"[SNAPSHOT] Live feed URL: {url}")

        # 1. Try live feed first
        entries = fetch_rss_entries(url)

        # 2. If live feed fails → fallback to IA snapshot
        if len(entries) == 0:
            print("[SNAPSHOT] Live feed returned 0 entries. Falling back to IA snapshot...")
            ia_feed_url = snapshot_url(url, sleep_seconds=2.0)
            print(f"[SNAPSHOT] IA feed URL: {ia_feed_url}")
            entries = fetch_rss_entries(ia_feed_url)

        # 3. If still empty, skip category
        if len(entries) == 0:
            print("[SNAPSHOT] ERROR: Both live and IA feed returned 0 entries. Skipping category.")
            continue

        for e in entries:
            request_url = snapshot_url(e.link, sleep_seconds=2.0)
            print(f"[SNAPSHOT] Request URL (as stored by IA): {request_url}")
            details = scrape_request_page(request_url)

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
        "resolution_text",
        "attachments",
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[SNAPSHOT] Wrote {len(rows)} rows to {filename}")

if __name__ == "__main__":
    build_snapshot()
