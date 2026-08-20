"""Tests for logging configuration helpers."""

import logging

from ruckus_smartzone.logging_config import mask_sensitive_headers, set_log_level


def test_set_log_level_accepts_str_and_int() -> None:
    set_log_level("DEBUG")
    assert logging.getLogger("ruckus_smartzone").level == logging.DEBUG
    set_log_level(logging.INFO)
    assert logging.getLogger("ruckus_smartzone").level == logging.INFO


def test_mask_sensitive_headers() -> None:
    headers = {
        "Authorization": "Bearer secret-token",
        "Cookie": "JSESSIONID=abc123",
        "Content-Type": "application/json",
    }
    masked = mask_sensitive_headers(headers)
    assert masked["Authorization"] == "Bearer ***"
    assert masked["Cookie"] == "***"
    assert masked["Content-Type"] == "application/json"
