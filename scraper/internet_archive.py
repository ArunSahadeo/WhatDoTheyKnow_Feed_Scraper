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
    """
    Append a harmless timestamp query parameter so IA treats each run
    as a distinct capture request, avoiding deduplication.
    """
    ts = _timestamp_suffix()
    return f"{url}&ia_ts={ts}" if "?" in url else f"{url}?ia_ts={ts}"

def snapshot_url(live_url: str, sleep_seconds: float = 0.0) -> str:
    """
    Send the live URL to Internet Archive's Save Page Now endpoint and
    return the resulting snapshot URL (https://web.archive.org/...).

    If anything goes wrong, this function falls back to returning the
    original live_url so the rest of the pipeline can still run.

    This does NOT fetch the snapshot content; it only returns the URL.
    """
    target = _with_ia_ts(live_url)
    save_url = SAVE_PAGE_NOW_ENDPOINT + target

    print(f"[IA] Requesting snapshot for: {live_url}")
    print(f"[IA] Save Page Now URL:      {save_url}")

    try:
        # We don't want to follow redirects here; we want the headers.
        resp = requests.get(save_url, timeout=60, allow_redirects=False)
    except Exception as e:
        print(f"[IA] Error calling Save Page Now: {e}")
        print("[IA] Falling back to live URL.")
        return live_url

    print(f"[IA] Response status: {resp.status_code}")

    # IA usually returns a Content-Location header like:
    #   /web/20260325010101/https://www.whatdotheyknow.com/...
    snapshot_path: Optional[str] = resp.headers.get("Content-Location")

    if not snapshot_path:
        # Sometimes Location is used instead.
        snapshot_path = resp.headers.get("Location")

    if snapshot_path:
        if snapshot_path.startswith("http://") or snapshot_path.startswith("https://"):
            snapshot = snapshot_path
        else:
            snapshot = WEB_ARCHIVE_ROOT + snapshot_path

        print(f"[IA] Snapshot URL: {snapshot}")
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)
        return snapshot

    print("[IA] No snapshot location found in headers; falling back to live URL.")
    return live_url
