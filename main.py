"""
Job alert bot — checks watched employers for new Toronto Winter 2027
internship postings and pushes new matches to your iPhone via ntfy.

Run manually:   python main.py
Run on a schedule: see .github/workflows/check_jobs.yml (GitHub Actions,
free, runs every 30 min without needing your computer on).
"""
import json
import os
import sys

import config
import workday_client
import ashby_client
import generic_client
import filters
import notify


def load_seen() -> set:
    if os.path.exists(config.STATE_FILE):
        with open(config.STATE_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_seen(seen: set):
    with open(config.STATE_FILE, "w") as f:
        json.dump(sorted(seen), f, indent=2)


def collect_all_jobs():
    all_jobs = []

    for emp in config.WORKDAY_EMPLOYERS:
        try:
            jobs = workday_client.fetch_jobs(emp["tenant"], emp["wd_server"], emp["site"])
            for j in jobs:
                j["employer"] = emp["name"]
            all_jobs.extend(jobs)
            print(f"[ok] {emp['name']}: {len(jobs)} postings fetched")
        except Exception as e:
            print(f"[error] {emp['name']} (Workday): {e}", file=sys.stderr)

    for emp in config.ASHBY_EMPLOYERS:
        try:
            jobs = ashby_client.fetch_jobs(emp["org"])
            for j in jobs:
                j["employer"] = emp["name"]
            all_jobs.extend(jobs)
            print(f"[ok] {emp['name']}: {len(jobs)} postings fetched")
        except Exception as e:
            print(f"[error] {emp['name']} (Ashby): {e}", file=sys.stderr)

    for emp in config.GENERIC_EMPLOYERS:
        try:
            jobs = generic_client.fetch_jobs(emp["name"], emp["url"])
            for j in jobs:
                j["employer"] = emp["name"]
            all_jobs.extend(jobs)
            print(f"[ok] {emp['name']}: {len(jobs)} link(s) matched keywords (best-effort)")
        except Exception as e:
            print(f"[error] {emp['name']} (generic): {e}", file=sys.stderr)

    return all_jobs


def main():
    seen = load_seen()
    all_jobs = collect_all_jobs()

    new_matches = 0
    for job in all_jobs:
        job_key = f"{job['employer']}::{job['id']}"
        if job_key in seen:
            continue
        seen.add(job_key)  # mark as seen regardless of match, so we don't recheck it

        is_match, note = filters.matches(job)
        if not is_match:
            continue

        title = f"{job['employer']}: {job['title']}"
        body = job.get("location", "") or "Location not listed"
        if note:
            body += f"\n⚠️ {note}"

        print(f"[MATCH] {title} — {body}")
        notify.send(title, body, job.get("url"))
        new_matches += 1

    save_seen(seen)
    print(f"\nDone. {new_matches} new match(es) sent, {len(all_jobs)} total postings scanned, "
          f"{len(seen)} total seen historically.")


if __name__ == "__main__":
    main()
