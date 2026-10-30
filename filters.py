import re
import config


def _has(patterns, text):
    return any(re.search(p, text) for p in patterns)


def matches(job: dict) -> tuple[bool, str]:
    title = job.get("title", "").lower()
    blob = " ".join([title, job.get("location", ""), job.get("description", "")]).lower()

    if any(k in blob for k in config.EXCLUDE_KEYWORDS):
        return False, ""
    if _has(config.EXCLUDE_TITLE_PATTERNS, title):
        return False, ""
    if not _has(config.ROLE_PATTERNS, title):
        return False, ""
    if not any(k in blob for k in config.LOCATION_KEYWORDS):
        return False, ""
    return True, ""