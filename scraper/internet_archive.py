import time
from datetime import datetime, timezone
from typing import Optional
import requests

SAVE_PAGE_NOW_ENDPOINT = "https://web.archive.org/save/"
WEB_ARCHIVE_ROOT = "https://web.archive.org"

def _timestamp_suffix() -> str:
    """Return a compact UTC timestamp for cache-busting."""
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def _with_ia_ts(url: str) -> str:
    """Append a timestamp param so IA treats each run as a new capture."""
    ts = _timestamp_suffix()
    return f"{url}&ia_ts={ts}" if "?" in url else f"{url}?ia_ts={ts}"

def snapshot_url(live_url: str, retries: int = 3, sleep_seconds: float = 2.0) -> str:
    """
    Send the live URL to Internet Archive Save Page Now and return
    the resulting snapshot URL. Retries on timeout. If IA fails,
    return the original live URL.
    """
    target = _with_ia_ts(live_url)
    save_url = SAVE_PAGE_NOW_ENDPOINT + target

    for attempt in range(1, retries + 1):
        print(f"[IA] Attempt {attempt}/{retries} for: {live_url}")
        print(f"[IA] Save Page Now URL:      {save_url}")

        try:
            resp = requests.get(
                save_url,
                timeout=180,            # IA is slow - give it time
                allow_redirects=False
            )
        except Exception as e:
            print(f"[IA] Error: {e}")
            if attempt < retries:
                print("[IA] Retrying...")
                time.sleep(3)
                continue
            print("[IA] All retries failed. Falling back to live URL.")
            return live_url

        snapshot_path: Optional[str] = (
            resp.headers.get("Content-Location")
            or resp.headers.get("Location")
        )

        if snapshot_path:
            if snapshot_path.startswith("http"):
                snapshot = snapshot_path
            else:
                snapshot = WEB_ARCHIVE_ROOT + snapshot_path

            print(f"[IA] Snapshot URL: {snapshot}")
            time.sleep(sleep_seconds)
            return snapshot

        print("[IA] No snapshot location found in headers.")
        if attempt < retries:
            print("[IA] Retrying...")
            time.sleep(3)

    print("[IA] Failed to obtain snapshot. Falling back to live URL.")
    return live_url
