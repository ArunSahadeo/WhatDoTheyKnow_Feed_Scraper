import requests
from bs4 import BeautifulSoup
import os
import re
import json
import base64

def scrape_request_page(url, html):
    url = re.sub(r'#(?:incoming|outgoing)-\d+$', '', url)
    soup = BeautifulSoup(html, "html.parser")
    submitter = None
    authority = None
    status = None
    messages = []
    attachments = []

    # Submitter

    try:
        submitter = soup.select_one(".request-header__action-bar-container .request-header__subtitle a:first-of-type")
        submitter = submitter.text.strip() if submitter else None
    except:
        pass

    # Authority

    try:
        authority = soup.select_one(".request-header__action-bar-container .request-header__subtitle a:last-of-type")
        authority = authority.text.strip() if authority else None
    except:
        pass

    # Status

    try:
        status = soup.select_one("#request_status").get("class")[1].split('request-status-message--')[1]
    except:
        pass

    # Last message (resolution)

    try:
        correspondence_items = soup.select(".correspondence")

        if correspondence_items:
            for message in correspondence_items:
                author = message.select_one("div.correspondence__header > span").get_text().replace('\n', '').strip()
                author = re.sub(r'\s{2,}', ' ', author)
                published = message.select_one(".correspondence__header__date > time").get("datetime")
                message_type = "outgoing" if "outgoing" in message["class"] else "incoming"

                content = base64.b64encode(message.select_one('.correspondence_text').get_text(separator="\n").strip().encode())
                messages.append({"author": author, "published": published, "message_type": message_type, "content": content})
    except:
        pass

    # Attachments

    try:
        for attachment in soup.select(".attachment"):
            attachment_item_title = attachment.select_one(".attachment__name").text.strip()
            attachment_item_url = attachment.select_one(".attachment__meta a").get("href")

            if attachment_item_title and attachment_item_url:
                attachments.append({"title": attachment_item_title, "url": "https://www.whatdotheyknow.com" + attachment_item_url})
    except:
        pass

    if submitter is None or authority is None or status is None or not messages:
            import datetime
            os.makedirs("errors", exist_ok=True)

            try:
                request_slug = url.split('/request/')[1]
            except:
                request_slug = None

            if request_slug is not None:
                timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d")
                filename = f"errors/{request_slug}_{timestamp}.html"

                if submitter is None:
                    print(f"Submitter not set for {request_slug}")

                if authority is None:
                    print(f"Authority not set for {request_slug}")

                if status is None:
                    print(f"Status not set for {request_slug}")

                if not messages:
                    print(f"Correspondence not set for {request_slug}")

                f = open(filename, "w", encoding="utf-8")
                f.write(html)
                f.close()

    return {
        "submitter": submitter,
        "authority": authority,
        "status": status,
        "messages": messages,
        "attachments": attachments
    }
