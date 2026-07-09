"""
validators.py — shared input validation helpers for ResumeAI.

Usage:
    from validators import is_valid_email, is_valid_password, is_valid_phone, is_valid_url
"""

import re

EMAIL_RE = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
# Accepts optional country code, spaces/dashes, 10-15 digits total
PHONE_RE = re.compile(r"^\+?[0-9]{1,4}?[\s-]?[0-9]{10}$|^\+?[0-9]{10,15}$")
URL_RE = re.compile(
    r"^(https?:\/\/)?([\w-]+\.)+[\w-]{2,}(\/[\w\-._~:/?#\[\]@!$&'()*+,;=%]*)?$"
)


def is_valid_email(email: str) -> bool:
    """Basic RFC-ish email format check: someone@domain.tld"""
    if not email:
        return False
    return bool(EMAIL_RE.match(email.strip()))


def is_valid_password(password: str, min_length: int = 6) -> tuple[bool, str]:
    """
    Returns (is_valid, message).
    Requires: min length, at least 1 letter and 1 number.
    """
    if not password or len(password) < min_length:
        return False, f"Password must be at least {min_length} characters."
    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    return True, ""


def is_valid_phone(phone: str) -> bool:
    """Accepts 10-digit numbers, with optional country code / spaces / dashes."""
    if not phone:
        return False
    cleaned = phone.strip().replace(" ", "").replace("-", "")
    return bool(PHONE_RE.match(cleaned))


def is_valid_url(url: str) -> bool:
    """Loose check for domain-like URLs (linkedin.com/in/x, github.com/x, etc.)"""
    if not url:
        return False
    return bool(URL_RE.match(url.strip()))


LINKEDIN_HOST_RE = re.compile(r"^(https?:\/\/)?(www\.)?linkedin\.com(\/|$)", re.IGNORECASE)
GITHUB_HOST_RE = re.compile(r"^(https?:\/\/)?(www\.)?github\.com(\/|$)", re.IGNORECASE)


def is_valid_linkedin_url(url: str) -> bool:
    """Must be a real linkedin.com URL (anchored host match, not just a substring)."""
    if not url or not is_valid_url(url):
        return False
    return bool(LINKEDIN_HOST_RE.match(url.strip()))


def is_valid_github_url(url: str) -> bool:
    """Must be a real github.com URL (anchored host match, not just a substring)."""
    if not url or not is_valid_url(url):
        return False
    return bool(GITHUB_HOST_RE.match(url.strip()))


def is_valid_name(name: str) -> bool:
    """Letters, spaces, dots, apostrophes, hyphens only — at least 2 chars."""
    if not name or len(name.strip()) < 2:
        return False
    return bool(re.match(r"^[A-Za-z][A-Za-z .'-]+$", name.strip()))