"""
URL validation guard to prevent Server-Side Request Forgery (SSRF).

Before the auditor fetches a user-supplied URL, :func:`validate_url` verifies
that:

* The scheme is ``http`` or ``https`` (no ``file://``, ``ftp://``, ``gopher://``,
  etc. that could be abused to read local files or pivot to other services).
* The hostname does not literally resolve to a host we consider "internal"
  (``localhost``, any name ending in ``.local`` or ``.internal``).
* Every IP address the hostname resolves to is a public, routable address.
  IPs in loopback, link-local (e.g. the cloud metadata endpoint
  ``169.254.169.254``), RFC1918 private ranges (``10/8``, ``172.16/12``,
  ``192.168/16``), multicast, reserved, or unspecified space are rejected.

Any rejection raises :class:`ValueError` with a clear message. The caller
(``WebsiteAuditor.audit``) should let the exception propagate.
"""

from __future__ import annotations

import ipaddress
import socket
from typing import Iterable
from urllib.parse import urlparse


ALLOWED_SCHEMES: frozenset[str] = frozenset({"http", "https"})

# Hostnames we refuse even if DNS happens to map them to a public address.
BLOCKED_HOSTNAME_SUFFIXES: tuple[str, ...] = (".local", ".internal")
BLOCKED_HOSTNAMES: frozenset[str] = frozenset({"localhost"})


def _iter_resolved_ips(hostname: str) -> Iterable[ipaddress._BaseAddress]:
    """Yield every IP address ``hostname`` resolves to.

    Uses ``socket.getaddrinfo`` so both A and AAAA records are considered.
    Raises :class:`ValueError` if DNS resolution fails — we refuse to fetch
    a URL we cannot verify.
    """
    try:
        addrinfos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Cannot resolve hostname '{hostname}': {exc}") from exc

    seen: set[str] = set()
    for family, _type, _proto, _canon, sockaddr in addrinfos:
        ip_str = sockaddr[0]
        # Strip IPv6 zone identifiers (e.g. "fe80::1%en0").
        ip_str = ip_str.split("%", 1)[0]
        if ip_str in seen:
            continue
        seen.add(ip_str)
        try:
            yield ipaddress.ip_address(ip_str)
        except ValueError:
            # Shouldn't happen for getaddrinfo results, but be defensive.
            continue


def _is_forbidden_ip(ip: ipaddress._BaseAddress) -> bool:
    """Return True if ``ip`` falls in a range we refuse to contact."""
    return (
        ip.is_loopback
        or ip.is_link_local
        or ip.is_private
        or ip.is_multicast
        or ip.is_reserved
        or ip.is_unspecified
    )


def validate_url(url: str) -> None:
    """Validate ``url`` is safe to fetch, or raise :class:`ValueError`.

    The function returns ``None`` on success. On failure it raises with a
    message describing which check failed so callers can surface it to users
    without leaking internals.
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string")

    parsed = urlparse(url.strip())

    scheme = (parsed.scheme or "").lower()
    if scheme not in ALLOWED_SCHEMES:
        raise ValueError(
            f"URL scheme '{scheme or '(missing)'}' is not allowed; "
            f"use one of: {', '.join(sorted(ALLOWED_SCHEMES))}"
        )

    hostname = (parsed.hostname or "").lower()
    if not hostname:
        raise ValueError("URL must include a hostname")

    if hostname in BLOCKED_HOSTNAMES:
        raise ValueError(f"Hostname '{hostname}' is not allowed")

    if any(hostname.endswith(suffix) for suffix in BLOCKED_HOSTNAME_SUFFIXES):
        raise ValueError(
            f"Hostname '{hostname}' uses a blocked suffix "
            f"({', '.join(BLOCKED_HOSTNAME_SUFFIXES)})"
        )

    # If the hostname is already a literal IP, urlparse returns it here too.
    # _iter_resolved_ips will just re-confirm via getaddrinfo, which is fine.
    resolved_any = False
    for ip in _iter_resolved_ips(hostname):
        resolved_any = True
        if _is_forbidden_ip(ip):
            raise ValueError(
                f"URL '{url}' resolves to disallowed IP {ip} "
                f"(internal/private/loopback/link-local/reserved range)"
            )

    if not resolved_any:
        raise ValueError(f"Hostname '{hostname}' did not resolve to any IP")
