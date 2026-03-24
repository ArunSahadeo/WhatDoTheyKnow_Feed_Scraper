import requests
from bs4 import BeautifulSoup

def scrape_request_page(url):
    r = requests.get(url, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    # Submitter
    submitter = soup.select_one(".requester a")
    submitter = submitter.text.strip() if submitter else None

    # Authority
    authority = soup.select_one(".public_body a")
    authority = authority.text.strip() if authority else None

    # Status
    status = soup.select_one(".request_status")
    status = status.text.strip() if status else None

    # Last message (resolution)
    messages = soup.select(".correspondence")
    resolution_text = None
    if messages:
        last_msg = messages[-1]
        resolution_text = last_msg.get_text(separator="\n").strip()

    # Attachments
    attachments = []
    for a in soup.select(".attachment a"):
        href = a.get("href")
        if href:
            attachments.append("https://www.whatdotheyknow.com" + href)

    return {
        "submitter": submitter,
        "authority": authority,
        "status": status,
        "resolution_text": resolution_text,
        "attachments": ";".join(attachments)
    }

