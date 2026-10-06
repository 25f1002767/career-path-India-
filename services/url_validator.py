import re
from urllib.parse import urlparse
from typing import Dict, Any


class URLValidatorService:
    """
    Validates official opportunity and examination links.
    Ensures safe protocols, valid URLs, and flags suspicious schemes.
    Statuses: VALID, NEEDS_VERIFICATION, BROKEN, MISSING, REDIRECTED, UNKNOWN.
    """

    ALLOWED_SCHEMES = ("https", "http")
    BLOCKED_SCHEMES = ("javascript", "data", "file", "vbscript")

    @classmethod
    def validate_url(cls, url: str) -> Dict[str, Any]:
        if not url or not str(url).strip():
            return {
                "is_valid": False,
                "status": "MISSING",
                "reason": "URL is missing or empty."
            }

        url_str = str(url).strip()

        # Check for blocked pseudo-protocols
        for scheme in cls.BLOCKED_SCHEMES:
            if url_str.lower().startswith(f"{scheme}:"):
                return {
                    "is_valid": False,
                    "status": "BROKEN",
                    "reason": f"Disallowed protocol scheme: {scheme}"
                }

        try:
            parsed = urlparse(url_str)
            if not parsed.scheme or parsed.scheme.lower() not in cls.ALLOWED_SCHEMES:
                return {
                    "is_valid": False,
                    "status": "NEEDS_VERIFICATION",
                    "reason": f"Scheme '{parsed.scheme}' must be HTTP/HTTPS."
                }

            if not parsed.netloc:
                return {
                    "is_valid": False,
                    "status": "BROKEN",
                    "reason": "URL does not contain a valid network location/domain."
                }

            # Check for localhost / private IP
            domain = parsed.netloc.lower().split(":")[0]
            if domain in ("localhost", "127.0.0.1", "0.0.0.0") or domain.startswith("192.168.") or domain.startswith("10."):
                return {
                    "is_valid": False,
                    "status": "BROKEN",
                    "reason": "Local or private IP addresses are not permitted as official URLs."
                }

            # Valid government or educational domain recognition
            is_gov_or_nic = any(domain.endswith(tld) for tld in (".gov.in", ".nic.in", ".ac.in", ".edu.in", ".res.in", ".org.in", ".org", ".edu", ".in", ".com"))
            
            return {
                "is_valid": True,
                "status": "VALID" if is_gov_or_nic else "NEEDS_VERIFICATION",
                "clean_url": url_str,
                "domain": domain,
                "is_https": parsed.scheme.lower() == "https",
                "is_official_domain": any(domain.endswith(tld) for tld in (".gov.in", ".nic.in", ".ac.in", ".res.in"))
            }

        except Exception as e:
            return {
                "is_valid": False,
                "status": "BROKEN",
                "reason": f"URL parsing exception: {str(e)}"
            }
