# Toronto Winter 2027 Internship Alert Bot

Watches a list of employer career sites for new internship postings that
match: **Toronto, ON** · **Winter 2027 (Jan–Apr)** · **internship, open to
grad students** — and pushes a notification straight to your iPhone the
moment a match appears.

## How it works

- `workday_client.py` / `ashby_client.py` call the employer's own public
  JSON job-search API directly (the same one their careers page's search
  box calls). This is fast, reliable, and doesn't break when a page's
  visual design changes.
- `generic_client.py` is a best-effort fallback for career sites without a
  clean public API — it scans page HTML for internship keywords. It can't
  see anything rendered by JavaScript, so treat these as "may miss some
  postings" until they're upgraded to dedicated clients.
- `main.py` runs every employer, filters results through `filters.py`,
  compares against `seen_jobs.json` so you're never re-alerted for the
  same posting, and pushes new matches via `notify.py`.
- GitHub Actions runs `main.py` every 30 minutes for free and commits the
  updated `seen_jobs.json` back to the repo — no server, no computer that
  has to stay on.

## Setup (about 10 minutes)

1. **Create a GitHub repo** and push these files to it (or ask me to walk
   you through `git init` if you're new to this).
2. **Install the ntfy app** on your iPhone (App Store, free, no account).
   Open it → tap **+** → subscribe to a topic name you make up — treat it
   like a password, e.g. `toronto-quant-alerts-f83jd2`.
3. **Set your topic** in `config.py`:
   ```python
   NTFY_TOPIC = "toronto-quant-alerts-f83jd2"
   ```
4. **Push the repo to GitHub** — the workflow in
   `.github/workflows/check_jobs.yml` will start running automatically on
   its 30-minute schedule. You can also trigger it manually from the
   repo's **Actions** tab (`Run workflow`) to test it immediately.
5. Done. New matching postings will hit your phone as they're found.

## Test it locally first (optional but recommended)

```bash
pip install -r requirements.txt
python main.py
```

Watch the console output — it prints `[ok]` per employer with how many
postings it found, and `[MATCH]` for anything that passed your filters.

## Extending it

- **Add a Workday employer:** add an entry to `WORKDAY_EMPLOYERS` in
  `config.py` — just the tenant/wd_server/site from its careers URL.
- **Add an Ashby employer:** same idea, add to `ASHBY_EMPLOYERS`.
- **Add a hard-to-scrape employer properly** (RBC, BMO, Amazon, etc. use
  JS-rendered boards the generic scraper can't fully see): the clean fix
  is a Playwright-based client that loads the page in a headless browser
  and intercepts its background API calls — same shape as
  `workday_client.py`, just with a browser in front. Happy to build one
  for any specific employer once you know which ones matter most.
- **Tune the filters:** `filters.py` — adjust `TERM_KEYWORDS`,
  `ROLE_KEYWORDS`, `LOCATION_KEYWORDS` in `config.py` to taste.

## Known limitations (worth knowing, and worth mentioning if you talk about this project)

- The generic HTML scraper misses JavaScript-rendered listings — several
  employers on your original list (RBC, BMO, Amazon, Scotiabank, KPMG,
  PwC, Deloitte, etc.) fall into this bucket today and will need
  per-employer clients for full coverage.
- "Winter 2027" and "open to grad students" are detected via keyword
  matching against whatever text each source exposes — it's a heuristic,
  not a guarantee, so borderline results are sent with a ⚠️ note rather
  than silently dropped or silently trusted.
- ntfy topics aren't authenticated — anyone who guesses/knows your topic
  name can subscribe. Pick something unguessable.

## For your resume

This is a legitimate automated data pipeline project. A reasonable bullet:

> Built an automated job-alert pipeline in Python that polls multiple
> companies' career-site APIs (Workday CXS, Ashby) on a serverless
> schedule (GitHub Actions), filters postings against custom criteria,
> deduplicates against persisted state, and delivers real-time push
> notifications via a pub/sub API — reducing manual job-search checking
> to zero.

Skills it demonstrates: API integration, data pipelines/ETL, scheduling
and automation (cron/CI), state management, filtering/heuristic logic,
and shipping something that actually runs unattended in production.
