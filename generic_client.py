"""
Best-effort fallback for career sites that don't expose a clean JSON API.

This just fetches the page HTML and looks for link text that contains
internship-ish keywords. It will MISS anything rendered client-side by
JavaScript (many of these sites are React/Angular SPAs) — it's a starting
point, not a guarantee. Sites that need real coverage should get their own
client module later (same shape as workday_client.py).
"""
import requests
from bs4 import BeautifulSoup
import hashlib


def fetch_jobs(name: str, url: str):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
    except requests.RequestException:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    normalized = []
    for a in soup.find_all("a"):
        text = a.get_text(strip=True)
        if not text or len(text) < 5:
            continue
        low = text.lower()
        if "intern" in low or "co-op" in low or "coop" in low:
            href = a.get("href", "")
            if href and not href.startswith("http"):
                href = requests.compat.urljoin(url, href)
            job_id = hashlib.sha1((name + text + href).encode()).hexdigest()[:16]
            normalized.append({
                "id": job_id,
                "title": text,
                "location": "",  # not reliably available without per-site parsing
                "posted": "",
                "url": href or url,
            })
    return normalized
