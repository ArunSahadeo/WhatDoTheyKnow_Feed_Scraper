import requests
from bs4 import BeautifulSoup

def scrape_request_page(url):
    r = requests.get(url)
    print(f"The resolved URL and status code: {r.url}, {r.status_code}")
    soup = BeautifulSoup(r.text, "html.parser")

    # Submitter
    submitter = soup.select(".request-header__action-bar-container .request-header__subtitle a:first-child")
    submitter = submitter.text.strip() if submitter else None

    # Authority
    authority = soup.select(".request-header__action-bar-container .request-header__subtitle a:last-child")
    authority = authority.text.strip() if authority else None

    valid_statuses = [
        'waiting_response',
        'not_held',
        'rejected',
        'partially_successful',
        'successful',
        'waiting_clarification',
        'gone_postal',
        'internal_review',
        'error_message',
        'requires_admin',
        'user_withdrawn'
    ]

    # Status
    status = soup.select_one("#request_status").get("class").split('request-status-message--')[1]

    if status not in valid_statuses:
        print(f"The invalid status: {status}")
        status = None

    # Last message (resolution)
    messages = soup.select(".correspondence")
    resolution_text = None
    if messages:
        last_msg = messages[-1]
        resolution_text = last_msg.get_text(separator="\n").strip()

    # Attachments
    attachments = []
    for attachment in soup.select(".attachment"):
        attachment_item_title = attachment.select(".attachment__name").text.strip()
        attachment_item_url = attachment.select_one(".attachment__meta a").get("href")

        if attachment_item_title and attachment_item_title_url:
            attachments.append({"title": attachment_item_title, "url": "https://www.whatdotheyknow.com" + attachment_item_url})

    return {
        "submitter": submitter,
        "authority": authority,
        "status": status,
        "resolution_text": resolution_text,
        "attachments": attachments
    }
