"""Logging configuration and utilities for the Ruckus SmartZone client."""

import json
import logging
from typing import Any, Dict, Union

try:
    import httpx
except ImportError:
    httpx = None  # type: ignore[assignment]

# Sensitive header names that should be masked in logs
SENSITIVE_HEADERS = {"authorization", "cookie", "x-api-key"}

# Maximum length for response body in logs (truncate if longer)
MAX_LOG_BODY_LENGTH = 1000


def _normalize_log_level(level: Union[str, int]) -> int:
    """Normalize log level to integer.

    Args:
        level: Log level as string or integer

    Returns:
        Log level as integer
    """
    if isinstance(level, str):
        return getattr(logging, level.upper(), logging.INFO)
    return level


def set_log_level(level: Union[str, int]) -> None:
    """Set the log level for the ruckus_smartzone logger.

    Args:
        level: Log level as string ("DEBUG", "INFO", "WARNING", "ERROR",
               "CRITICAL") or integer (logging.DEBUG, logging.INFO, etc.)
    """
    level_int = _normalize_log_level(level)
    logger = logging.getLogger("ruckus_smartzone")

    # Set logger level (this propagates to handlers automatically)
    logger.setLevel(level_int)
    logger.propagate = True

    # Only add a handler if neither this logger nor root already have one,
    # so a caller's existing logging configuration is left untouched.
    if not logger.handlers and not logging.root.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(handler)

    # Silence httpx/httpcore request logs
    logging.getLogger("httpx").disabled = True
    logging.getLogger("httpcore").disabled = True


def get_logger(name: str) -> logging.Logger:
    """Get a logger with consistent configuration.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def mask_sensitive_headers(headers: Union[Dict[str, str], Any]) -> Dict[str, str]:
    """Mask sensitive header values in a dictionary.

    Args:
        headers: Headers dictionary or httpx.Headers object

    Returns:
        Dictionary with sensitive headers masked
    """
    if httpx and isinstance(headers, httpx.Headers):
        headers_dict = dict(headers.items())
    elif hasattr(headers, "items"):
        headers_dict = dict(headers.items())
    else:
        headers_dict = dict(headers)

    masked = {}
    for key, value in headers_dict.items():
        key_lower = key.lower()
        if key_lower in SENSITIVE_HEADERS:
            if (
                key_lower == "authorization"
                and isinstance(value, str)
                and value.startswith("Bearer ")
            ):
                masked[key] = "Bearer ***"
            else:
                masked[key] = "***"
        else:
            masked[key] = value

    return masked


def format_request_body(body: Any) -> str:
    """Format a request body for logging.

    Args:
        body: Request body (dict, str, bytes, etc.)

    Returns:
        Formatted string representation
    """
    if body is None:
        return "None"

    if isinstance(body, (dict, list)):
        try:
            return json.dumps(body, indent=2)
        except (TypeError, ValueError):
            return str(body)

    if isinstance(body, bytes):
        try:
            decoded = body.decode("utf-8")
            try:
                parsed = json.loads(decoded)
                return json.dumps(parsed, indent=2)
            except (json.JSONDecodeError, ValueError):
                return f"<bytes: {len(body)} bytes>"
        except UnicodeDecodeError:
            return f"<bytes: {len(body)} bytes>"

    return str(body)


def format_response_body(body: Any) -> str:
    """Format a response body for logging, truncating if too long.

    Args:
        body: Response body (dict, str, etc.)

    Returns:
        Formatted string representation (truncated if too long)
    """
    if body is None:
        return "None"

    if isinstance(body, dict):
        try:
            formatted = json.dumps(body, indent=2)
        except (TypeError, ValueError):
            formatted = str(body)
    elif isinstance(body, str):
        try:
            parsed = json.loads(body)
            formatted = json.dumps(parsed, indent=2)
        except (json.JSONDecodeError, ValueError):
            formatted = body
    else:
        formatted = str(body)

    if len(formatted) > MAX_LOG_BODY_LENGTH:
        truncated = formatted[:MAX_LOG_BODY_LENGTH]
        return f"{truncated}... (truncated, {len(formatted)} chars total)"

    return formatted
