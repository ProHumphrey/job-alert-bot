"""
Client for Workday's public CXS (Candidate Experience System) JSON API.

Every Workday-powered careers site (e.g. https://td.wd3.myworkdayjobs.com/...)
is a single-page app that itself calls a JSON endpoint at:

    POST https://{tenant}.{wd_server}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs

This calls that same endpoint directly instead of scraping HTML, so it's
fast and doesn't break when the page's visual layout changes.
"""
import requests

PAGE_SIZE = 20  # Workday hard-caps page size at 20


def fetch_jobs(tenant: str, wd_server: str, site: str, search_text: str = "", max_pages: int = 15):
    """Return a list of raw job postings (dicts) from a Workday tenant."""
    url = f"https://{tenant}.{wd_server}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Accept-Language": "en-US",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Referer": f"https://{tenant}.{wd_server}.myworkdayjobs.com/en-US/{site}",
    }

    all_jobs = []
    offset = 0
    for _ in range(max_pages):
        payload = {"appliedFacets": {}, "limit": PAGE_SIZE, "offset": offset, "searchText": search_text}
        resp = requests.post(url, json=payload, headers=headers, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        batch = data.get("jobPostings") or []
        all_jobs.extend(batch)

        offset += PAGE_SIZE
        total = data.get("total", 0)
        if not batch or offset >= total:
            break

    # Normalize to a common shape used by main.py
    normalized = []
    for job in all_jobs:
        normalized.append({
            "id": job.get("bulletFields", [None])[0] or job.get("externalPath"),
            "title": job.get("title", ""),
            "location": job.get("locationsText", ""),
            "posted": job.get("postedOn", ""),
            "url": f"https://{tenant}.{wd_server}.myworkdayjobs.com/en-US/{site}{job.get('externalPath', '')}",
        })
    return normalized
