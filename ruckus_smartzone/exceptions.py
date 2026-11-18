"""Custom exceptions for the Ruckus SmartZone API client."""

import html
from typing import Any, Dict, List, Optional


class SmartZoneAPIError(Exception):
    """Base exception for all Ruckus SmartZone API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            status_code: HTTP status code if available
            response_data: Response data if available
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data


class SmartZoneAuthenticationError(SmartZoneAPIError):
    """Raised when authentication fails (401)."""

    def __init__(
        self,
        message: str = "Authentication failed",
        response_data: Optional[Dict] = None,
    ) -> None:
        """Initialize authentication error."""
        super().__init__(message, status_code=401, response_data=response_data)


class SmartZonePermissionError(SmartZoneAPIError):
    """Raised when the caller lacks permission (403)."""

    def __init__(
        self,
        message: str = "Permission denied",
        response_data: Optional[Dict] = None,
    ) -> None:
        """Initialize permission error."""
        super().__init__(message, status_code=403, response_data=response_data)


class SmartZoneNotFoundError(SmartZoneAPIError):
    """Raised when a resource is not found (404)."""

    def __init__(
        self,
        message: str = "Resource not found",
        response_data: Optional[Dict] = None,
    ) -> None:
        """Initialize not found error."""
        super().__init__(message, status_code=404, response_data=response_data)


class SmartZoneValidationError(SmartZoneAPIError):
    """Raised when request validation fails (422)."""

    def __init__(
        self,
        message: str = "Validation error",
        response_data: Optional[Dict] = None,
        errors: Optional[List[Dict]] = None,
    ) -> None:
        """Initialize validation error.

        Args:
            message: Error message
            response_data: Response data if available
            errors: List of validation errors
        """
        super().__init__(message, status_code=422, response_data=response_data)
        self.errors = errors or []


class SmartZoneConnectionError(SmartZoneAPIError):
    """Raised when the connection to the API fails."""

    def __init__(
        self,
        message: str = "Connection error",
        original_error: Optional[Exception] = None,
    ) -> None:
        """Initialize connection error.

        Args:
            message: Error message
            original_error: Original exception that caused this error
        """
        super().__init__(message)
        self.original_error = original_error


class SmartZoneRateLimitError(SmartZoneAPIError):
    """Raised when the controller rate-limits the caller (429).

    The client backs off and retries while attempts remain; this surfaces only
    once retries are exhausted.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        response_data: Optional[Dict] = None,
        retry_after: Optional[int] = None,
    ) -> None:
        """Initialize rate-limit error.

        Args:
            message: Error message
            response_data: Response data if available
            retry_after: Seconds the controller asked the caller to wait, from
                the ``RateLimit-Reset`` header, if present
        """
        super().__init__(message, status_code=429, response_data=response_data)
        self.retry_after = retry_after


class SmartZoneBusyError(SmartZoneAPIError):
    """Raised when the controller is busy serialising a configuration change.

    The client backs off and retries while attempts remain; this surfaces only
    once retries are exhausted.
    """

    def __init__(
        self,
        message: str = "Controller busy",
        status_code: Optional[int] = None,
        response_data: Optional[Dict] = None,
    ) -> None:
        """Initialize busy error."""
        super().__init__(message, status_code=status_code, response_data=response_data)


class SmartZoneZoneMismatchError(SmartZoneAPIError):
    """Raised when an AP is not in the zone the caller expected.

    A client-side pre-flight refusal: move and update take an ``expected_zone_id``
    and this is raised before any write when one or more APs sit elsewhere, so a
    wrong MAC cannot touch an AP outside the caller's intended zone.
    """

    def __init__(
        self,
        message: str,
        mismatches: Optional[Dict[str, Optional[str]]] = None,
    ) -> None:
        """Initialize zone-mismatch error.

        Args:
            message: Error message.
            mismatches: Map of AP MAC to the zone id it is actually in (``None``
                when the AP has no zone), for each AP that failed the check.
        """
        super().__init__(message)
        self.mismatches = mismatches or {}


class SmartZoneBusinessRuleError(SmartZoneAPIError):
    """Raised when the Switch Manager refuses a request on a business rule.

    The controller answers these with an HTTP 500 whose body carries a stable
    ``error.msgKey`` (for example
    ``server.switch.portSettings.cannot.enable.flexible.auth.without.switch.authentication``).
    Branch on :attr:`msg_key`, not on the message text.
    """

    def __init__(
        self,
        message: str,
        msg_key: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict] = None,
        msg_values: Optional[Any] = None,
    ) -> None:
        """Initialize business-rule error.

        Args:
            message: Error message.
            msg_key: The controller's ``error.msgKey``.
            status_code: HTTP status code of the response.
            response_data: Parsed response body.
            msg_values: The controller's ``error.msgValues``, if any.
        """
        super().__init__(message, status_code=status_code, response_data=response_data)
        self.msg_key = msg_key
        self.msg_values = msg_values


# Switch-side refusal text when a push collides with an open CLI config session.
LOCAL_CONFIG_CONFLICT_TEXT = "ongoing local configuration change"


class SmartZoneDeploymentError(SmartZoneAPIError):
    """Raised when a Switch Manager configuration deployment fails.

    Switch Manager writes return at once and deploy to the switch later. A
    deployment that reports ``FAILURE`` raises this with the failing CLI line
    and the switch's error text. Lines before the failing one stay applied on
    the switch; there is no rollback.
    """

    def __init__(
        self,
        message: str,
        *,
        transaction_id: Optional[str] = None,
        switch_id: Optional[str] = None,
        line: Optional[int] = None,
        switch_message: Optional[str] = None,
        transactions: Optional[List[Dict]] = None,
        details: Optional[List[Dict]] = None,
    ) -> None:
        """Initialize deployment error.

        Args:
            message: Error message.
            transaction_id: Transaction that failed.
            switch_id: Switch that reported the failure.
            line: One-based number of the CLI line that failed, if reported.
            switch_message: The switch's error text for that line.
            transactions: Configuration-history entries seen for the write.
            details: Per-switch detail entries of the failed transaction.
        """
        super().__init__(message)
        self.transaction_id = transaction_id
        self.switch_id = switch_id
        self.line = line
        self.switch_message = switch_message
        self.transactions = transactions or []
        self.details = details or []

    @property
    def local_config_conflict(self) -> bool:
        """Whether the switch refused the push for an open local CLI session.

        Such a push can be retried once the CLI session leaves config mode.
        """
        return LOCAL_CONFIG_CONFLICT_TEXT in (self.switch_message or "").lower()


class SmartZoneDeploymentTimeoutError(SmartZoneDeploymentError):
    """Raised when a deployment has not finished within the caller's timeout.

    ``transactions`` holds the configuration-history entries seen so far; an
    empty list means no transaction appeared at all.
    """


# SmartZone returns a 403 with this vendor error code for objects the caller is
# entitled to but that do not exist; it is treated as "not found".
NOT_FOUND_ERROR_CODE = 211


def _error_code(response_data: Optional[Dict]) -> Optional[int]:
    """Return the vendor ``errorCode`` from a response body, if present."""
    if not isinstance(response_data, dict):
        return None
    code = response_data.get("errorCode")
    if isinstance(code, bool):
        return None
    if isinstance(code, int):
        return code
    if isinstance(code, str) and code.isdigit():
        return int(code)
    return None


def _envelope_error(response_data: Optional[Dict]) -> Dict[str, Any]:
    """Return the ``error`` object of a Switch Manager response envelope.

    Switch Manager errors arrive as ``{success: false, error: {message,
    msgKey, msgValues}}``; any other body yields an empty dict.
    """
    if not isinstance(response_data, dict):
        return {}
    error = response_data.get("error")
    return error if isinstance(error, dict) else {}


def _envelope_message(error: Dict[str, Any]) -> Optional[str]:
    """Return the envelope's message with HTML entities decoded, if any."""
    message = error.get("message")
    if not isinstance(message, str) or not message.strip():
        return None
    return html.unescape(message).strip()


def raise_for_response(status_code: int, response_data: Optional[Dict] = None) -> None:
    """Raise the exception mapped to an error response.

    Maps HTTP status (and the vendor ``errorCode`` where it changes meaning) to
    the matching :class:`SmartZoneAPIError` subclass. A 403 carrying
    ``errorCode`` 211 is raised as :class:`SmartZoneNotFoundError`. A body whose
    ``error`` object carries a ``msgKey`` (Switch Manager business-rule refusal)
    is raised as :class:`SmartZoneBusinessRuleError`, unless the status is one
    of the auth, not-found or rate-limit statuses. An ``error.message`` becomes
    the exception message.

    Args:
        status_code: HTTP status code of the response
        response_data: Parsed response body, if any
    """
    error = _envelope_error(response_data)
    message = _envelope_message(error)
    if status_code == 401:
        raise SmartZoneAuthenticationError(response_data=response_data)
    if status_code == 403:
        if _error_code(response_data) == NOT_FOUND_ERROR_CODE:
            raise SmartZoneNotFoundError(response_data=response_data)
        raise SmartZonePermissionError(response_data=response_data)
    if status_code == 404:
        raise SmartZoneNotFoundError(response_data=response_data)
    if status_code == 429:
        raise SmartZoneRateLimitError(response_data=response_data)
    msg_key = error.get("msgKey")
    if isinstance(msg_key, str) and msg_key:
        raise SmartZoneBusinessRuleError(
            message or msg_key,
            msg_key,
            status_code=status_code,
            response_data=response_data,
            msg_values=error.get("msgValues"),
        )
    if status_code == 422:
        raise SmartZoneValidationError(
            message or "Validation error", response_data=response_data
        )
    raise SmartZoneAPIError(
        message or f"SmartZone API request failed with status {status_code}",
        status_code=status_code,
        response_data=response_data,
    )
