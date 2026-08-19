"""
Config: employers to watch + what counts as a match.

Add/remove employers freely. Each employer has a "kind" that tells
main.py which client function to use to fetch its jobs:
  - "workday"  -> hits the company's public Workday CXS JSON API directly
  - "ashby"    -> hits the company's public Ashby job-board JSON API directly
  - "generic"  -> best-effort keyword search over the raw page HTML
                   (works for simple pages, will miss JS-rendered boards —
                   flagged in the run log so you know which ones to babysit)
"""

# ---- Workday-powered employers -------------------------------------------
# tenant/wd_server/site come from the employer's careers URL:
#   https://{tenant}.{wd_server}.myworkdayjobs.com/{site}
WORKDAY_EMPLOYERS = [
    {"name": "AIMCo",            "tenant": "aimco",    "wd_server": "wd10", "site": "AIMCoCareers"},
    {"name": "CIBC",             "tenant": "cibc",     "wd_server": "wd3",  "site": "campus"},
    {"name": "Manulife",         "tenant": "manulife",  "wd_server": "wd3",  "site": "MFCJH_Jobs"},
    {"name": "Neuberger Berman", "tenant": "nb",        "wd_server": "wd1",  "site": "nbcareers"},
    {"name": "Ontario Teachers' Pension Plan (OTPP)", "tenant": "otppb", "wd_server": "wd3", "site": "OntarioTeachers_Careers"},
    {"name": "TD",               "tenant": "td",        "wd_server": "wd3",  "site": "TD_Bank_Careers"},
]


# ---- Everything else: best-effort keyword scan over the page HTML --------
# These sites use custom/JS-heavy career portals (Amazon, RBC, BMO, Scotia,
# Deloitte, KPMG, PwC, etc). The generic scraper fetches the page and does a
# keyword search. It WILL miss postings that only load via JavaScript — for
# those you'll want to add a dedicated client later (same pattern as
# workday_client.py / ashby_client.py). Treat these as "best effort."
GENERIC_EMPLOYERS = [
    {"name": "RBC",        "url": "https://jobs.rbc.com/ca/en/featuredopportunities/student-early-talent-jobs"},
    {"name": "BMO Campus", "url": "https://jobs.bmo.com/ca/en/campus"},
    {"name": "Scotiabank", "url": "https://jobs.scotiabank.com/go/Student-&-New-Grad-Jobs/2298417/"},
    {"name": "CPP Investments", "url": "https://www.cppinvestments.com/careers/campus-candidates"},
    {"name": "OPTrust",    "url": "https://www.optrust.com/AboutOPTrust/Career-Opportunities.asp"},
    {"name": "IMCO",       "url": "https://www.imcoinvest.com/careers/opportunities/"},
    {"name": "HOOPP",      "url": "https://hoopp.com/about-hoopp/hoopp-careers/students-and-new-graduates"},
    {"name": "Picton Mahoney", "url": "https://pictonmahoney.bamboohr.com/careers/"},
    {"name": "Purpose Investments", "url": "https://www.purpose-unlimited.com/careers#positions"},
    {"name": "Amazon Toronto", "url": "https://www.amazon.jobs/en/locations/toronto-canada"},
    {"name": "Alpaca", "url": "https://alpaca.markets/hiring"},
]

# ---- Match rules -----------------------------------------------------
LOCATION_KEYWORDS = ["toronto", "ontario", "on, canada"]
TERM_KEYWORDS = ["winter 2027", "jan-apr 2027", "january 2027"]  # any one match = pass
ROLE_KEYWORDS = ["intern", "co-op", "coop"]  # must be an internship-type posting
# If a posting's text contains one of these AND does NOT also mention grad/masters,
# it gets flagged (not silently dropped) as possibly undergrad-only, since this
# is only a heuristic — you asked to exclude undergrad-only postings.
UNDERGRAD_ONLY_HINTS = ["undergraduate students only", "currently enrolled in an undergraduate"]
GRAD_FRIENDLY_HINTS = ["graduate", "master's", "masters", "mba", "phd"]

# ntfy.sh topic — pick a hard-to-guess name, it's not password protected.
# e.g. "toronto-quant-intern-alerts-8x2f1"
NTFY_TOPIC = "toronto-quant-alerts-f83jd2"

STATE_FILE = "seen_jobs.json"
