import csv
import datetime
import os
from scraper.rss_feeds import RSS_FEEDS
from scraper.fetch_rss import fetch_rss_entries
from scraper.parse_request_page import scrape_request_page
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import requests
import re

def build_snapshot():
    os.makedirs("snapshots", exist_ok=True)
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"snapshots/foi_snapshot_{timestamp}.csv"

    rows = []

    for category, url in RSS_FEEDS.items():
        entries = fetch_rss_entries(url)

        for e in entries:
            request_url = None
            title = e.title
            published = e.published

            authority = None
            submitter = None

            content = str(e.content[0].value).replace('&lt', '<').replace('&gt;', '>').replace('&quot;', '"')
            m = re.search('<a href="https://www.whatdotheyknow.com/body/[^"]+">', content)

            if m is not None:
                authority = str(m.group(0)).replace('<a href="https://www.whatdotheyknow.com/body/', '').replace('">', '')

            m = re.search('<a href="https://www.whatdotheyknow.com/user/[^"]+">', content)

            if m is not None:
                submitter = str(m.group(0)).replace('<a href="https://www.whatdotheyknow.com/user/', '').replace('">', '')


            if submitter and authority:
                r = requests.get("https://www.whatdotheyknow.com/search/requests?query=" + '"' + quote_plus(title) + '"' + "+requested_by:" + submitter + "+requested_from:" + authority)
                soup = BeautifulSoup(r.text, "html.parser")
                search_results = soup.select(".foi_results + .results_block > .request_listing")

                if len(search_results) > 0:
                    for result in search_results:
                        request_url = result.select_one(".request_left > .head > a").get("href")
                        if request_url.startswith("/"):
                            request_url = "https://www.whatdotheyknow.com" + request_url

            details = scrape_request_page(request_url)

            rows.append({
                "category": category,
                "title": title,
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

if __name__ == "__main__":
    build_snapshot()
