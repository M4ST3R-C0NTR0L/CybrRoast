"""Tests for the SSRF URL guard."""

from __future__ import annotations

import socket
from typing import Iterable

import pytest

from cybrroast.url_guard import validate_url


def _fake_getaddrinfo(mapping: dict[str, list[str]]):
    """Return a stub for ``socket.getaddrinfo`` driven by ``mapping``.

    Each key is a hostname, each value is the list of IPs it should resolve to.
    Unknown hostnames raise ``socket.gaierror`` just like the real resolver.
    """

    def _fake(host, *_args, **_kwargs):
        if host in mapping:
            return [
                (socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, 0))
                for ip in mapping[host]
            ]
        raise socket.gaierror(-2, "Name or service not known")

    return _fake


@pytest.fixture
def patch_dns(monkeypatch):
    """Helper that patches ``socket.getaddrinfo`` with a fixed mapping."""

    def _apply(mapping: dict[str, list[str]]) -> None:
        monkeypatch.setattr(
            "cybrroast.url_guard.socket.getaddrinfo",
            _fake_getaddrinfo(mapping),
        )

    return _apply


class TestValidateUrlAllows:
    def test_allows_public_https_url(self, patch_dns):
        patch_dns({"example.com": ["93.184.216.34"]})
        # Should not raise.
        assert validate_url("https://example.com") is None

    def test_allows_public_http_url_with_path(self, patch_dns):
        patch_dns({"example.com": ["93.184.216.34"]})
        assert validate_url("http://example.com/some/path?q=1") is None


class TestValidateUrlRejects:
    def test_rejects_loopback_ip_literal(self):
        with pytest.raises(ValueError, match="disallowed IP"):
            validate_url("http://127.0.0.1")

    def test_rejects_link_local_metadata_endpoint(self):
        with pytest.raises(ValueError, match="disallowed IP"):
            validate_url("http://169.254.169.254")

    def test_rejects_rfc1918_10_dot(self):
        with pytest.raises(ValueError, match="disallowed IP"):
            validate_url("http://10.0.0.1")

    def test_rejects_rfc1918_192_168(self):
        with pytest.raises(ValueError, match="disallowed IP"):
            validate_url("http://192.168.1.1")

    def test_rejects_literal_localhost(self):
        with pytest.raises(ValueError, match="not allowed"):
            validate_url("http://localhost")

    def test_rejects_file_scheme(self):
        with pytest.raises(ValueError, match="scheme"):
            validate_url("file:///etc/passwd")

    def test_rejects_ftp_scheme(self):
        with pytest.raises(ValueError, match="scheme"):
            validate_url("ftp://example.com")

    def test_rejects_hostname_resolving_to_private_ip(self, patch_dns):
        # DNS rebinding style: public-looking hostname points at an RFC1918 IP.
        patch_dns({"sneaky.example": ["10.1.2.3"]})
        with pytest.raises(ValueError, match="disallowed IP"):
            validate_url("https://sneaky.example")

    def test_rejects_dot_internal_suffix(self):
        with pytest.raises(ValueError, match="blocked suffix"):
            validate_url("https://vault.internal")

    def test_rejects_dot_local_suffix(self):
        with pytest.raises(ValueError, match="blocked suffix"):
            validate_url("https://printer.local")

    def test_rejects_empty_url(self):
        with pytest.raises(ValueError, match="non-empty"):
            validate_url("")

    def test_rejects_missing_hostname(self):
        with pytest.raises(ValueError, match="hostname"):
            validate_url("http:///nohost")
