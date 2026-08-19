import re
import config


def _text_blob(job: dict) -> str:
    return " ".join([
        job.get("title", ""),
        job.get("location", ""),
        job.get("posted", ""),
        job.get("description", ""),
    ]).lower()


def matches(job: dict) -> tuple[bool, str]:
    """
    Returns (is_match, note).
    note is "" for a clean match, or a warning string (e.g. possible
    undergrad-only restriction) that still gets sent but flagged.
    """
    blob = _text_blob(job)
    is_excluded = any(k in blob for k in config.EXCLUDE_KEYWORDS)
    if is_excluded:
        return False, ""
    
    is_role  =  bool(re.search(r'\b(intern|interns|internship|co-op|coop)\b', blob))
    if not is_role:
        return False, ""

    is_location = any(k in blob for k in config.LOCATION_KEYWORDS)
    if not is_location:
        return False, ""

    # Term match is soft: many postings say "Winter 2027" only in the full
    # description (which the generic scraper can't see), so title-only
    # sources without a term match still pass through with a flag instead
    # of being dropped, since a false negative here means missing a job.
    has_term = any(k in blob for k in config.TERM_KEYWORDS) or "2027" in blob
    note = ""
    if not has_term:
        note = "term not confirmed in listing — verify dates on posting"

    is_undergrad_hint = any(k in blob for k in config.UNDERGRAD_ONLY_HINTS)
    is_grad_friendly = any(k in blob for k in config.GRAD_FRIENDLY_HINTS)
    if is_undergrad_hint and not is_grad_friendly:
        note = (note + "; " if note else "") + "may be undergrad-only — verify eligibility"

    return True, note
