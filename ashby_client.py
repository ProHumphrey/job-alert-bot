"""
Client for Ashby's public job-board JSON API.

Ashby-powered boards (https://jobs.ashbyhq.com/{org}) expose a public
read-only feed at:

    GET https://api.ashbyhq.com/posting-api/job-board/{org}
"""
import requests


def fetch_jobs(org: str):
    url = f"https://api.ashbyhq.com/posting-api/job-board/{org}"
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    normalized = []
    for job in data.get("jobs", []):
        normalized.append({
            "id": job.get("id"),
            "title": job.get("title", ""),
            "location": job.get("location", ""),
            "posted": job.get("publishedAt", ""),
            "url": job.get("jobUrl", ""),
            "description": job.get("descriptionPlain", "") or "",
        })
    return normalized
