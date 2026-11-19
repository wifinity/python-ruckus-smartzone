"""Wait for Switch Manager config deployments to finish.

A Switch Manager write returns 2xx at once; the controller then deploys the
change to the switch as one or more transactions in the switch group's
configuration history. A 2xx does not mean the switch is configured.

:class:`DeploymentTracker` snapshots the group history before a write and,
after it, waits until every new transaction for the tracked switches has
finished. Transactions are recognised by id, not by time, so the caller's
clock does not have to match the controller's. The controller lists group
history in no time order, so a new transaction can appear anywhere in the
list and every poll reads the whole group history.
"""

import html
import time
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
)

from ruckus_smartzone.exceptions import (
    SmartZoneDeploymentError,
    SmartZoneDeploymentTimeoutError,
)
from ruckus_smartzone.mac import normalize_mac
from ruckus_smartzone.switchm.base import SwitchmResource

if TYPE_CHECKING:
    from ruckus_smartzone.switchm.manager import SwitchManager

T = TypeVar("T")

# Items per history page; the API maximum, so most groups take one request.
HISTORY_PAGE_SIZE = 1000

SUCCESS_STATUSES = frozenset({"SUCCESS", "APPLIED"})
FAILURE_STATUS = "FAILURE"

# Per-switch detail statuses that are not a failure.
_DISPATCH_OK = frozenset({"SUCCESS", "NO_CONFIG_CHANGE", "MERGED", "APPLIED"})


def _switch_ids(entry: Dict[str, Any]) -> Set[str]:
    raw = entry.get("switchIds") or ""
    ids = raw if isinstance(raw, list) else str(raw).split(",")
    return {str(mac).strip().upper() for mac in ids if str(mac).strip()}


def _failure_from_details(
    transaction: Dict[str, Any],
    details: List[Dict[str, Any]],
    transactions: List[Dict[str, Any]],
) -> SmartZoneDeploymentError:
    """Build the error for a failed transaction from its per-switch detail."""
    transaction_id = transaction.get("transactionId")
    failed = [d for d in details if d.get("dispatchStatus") not in _DISPATCH_OK]
    item = failed[0] if failed else (details[0] if details else {})
    reasons = item.get("dispatchFailedReason") or []
    reason = reasons[0] if reasons and isinstance(reasons[0], dict) else {}

    raw_line = str(reason.get("lineNumber") or "").strip()
    line = int(raw_line) if raw_line.isdigit() else None
    text = reason.get("message") or item.get("dispatchError") or ""
    switch_message = html.unescape(str(text)).strip() or None
    switch_id = item.get("switchId")

    where = f" on switch {switch_id}" if switch_id else ""
    at = f" at line {line}" if line is not None else ""
    why = f": {switch_message}" if switch_message else ""
    return SmartZoneDeploymentError(
        f"Deployment {transaction_id} ({transaction.get('configType')}) "
        f"failed{where}{at}{why}",
        transaction_id=transaction_id,
        switch_id=switch_id,
        line=line,
        switch_message=switch_message,
        transactions=transactions,
        details=details,
    )


class DeploymentTracker:
    """Tracks the deployment transactions a write starts in one switch group."""

    def __init__(
        self,
        switchm: "SwitchManager",
        group_id: str,
        switch_ids: Optional[Iterable[str]] = None,
    ) -> None:
        """Snapshot the group's history so later transactions can be told apart.

        Args:
            switchm: The owning :class:`SwitchManager`.
            group_id: Switch group the write deploys in.
            switch_ids: Only count transactions touching these switches; all
                transactions of the group when omitted.
        """
        self._switchm = switchm
        self.group_id = group_id
        self.switch_ids = (
            {normalize_mac(mac) for mac in switch_ids}
            if switch_ids is not None
            else None
        )
        self._known: Set[str] = {
            entry["transactionId"]
            for entry in self._history()
            if entry.get("transactionId")
        }

    def __enter__(self) -> "DeploymentTracker":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        return None

    def _history(self) -> List[Dict[str, Any]]:
        return self._switchm.config_history.query(
            self.group_id, page_size=HISTORY_PAGE_SIZE
        )

    def new_transactions(self) -> List[Dict[str, Any]]:
        """Return the tracked transactions that appeared after the snapshot."""
        found: List[Dict[str, Any]] = []
        for entry in self._history():
            if entry.get("transactionId") in self._known:
                continue
            if self.switch_ids is not None and not (
                _switch_ids(entry) & self.switch_ids
            ):
                continue
            found.append(entry)
        return found

    def wait(
        self,
        *,
        timeout: float = 300.0,
        poll_interval: float = 5.0,
        settle: float = 15.0,
    ) -> List[Dict[str, Any]]:
        """Wait until every new tracked transaction has finished.

        Returns once at least one transaction has appeared, all of them report
        ``SUCCESS`` (or ``APPLIED``), and no further transaction has appeared
        for ``settle`` seconds. One write can start several transactions (a
        port write with auth fields starts ``PORT_CONFIGURATION`` and
        ``AUTHENTICATION``), which may not appear together.

        Returns:
            One ``{transaction, details}`` dict per transaction, oldest first;
            ``details`` holds the per-switch entries with the generated
            ``clis``.

        Raises:
            SmartZoneDeploymentError: As soon as a transaction reports
                ``FAILURE``, with the failing line and the switch's message.
            SmartZoneDeploymentTimeoutError: If the transactions have not all
                finished within ``timeout`` seconds.
        """
        deadline = time.monotonic() + timeout
        seen = -1
        changed_at = time.monotonic()
        while True:
            now = time.monotonic()
            found = self.new_transactions()
            if len(found) != seen:
                seen = len(found)
                changed_at = now

            for entry in found:
                if entry.get("deployStatus") == FAILURE_STATUS:
                    details = self._switchm.config_history.details(
                        entry["transactionId"]
                    )
                    raise _failure_from_details(entry, details, found)

            finished = bool(found) and all(
                entry.get("deployStatus") in SUCCESS_STATUSES for entry in found
            )
            if finished and now - changed_at >= settle:
                found.sort(key=lambda entry: entry.get("startTime") or 0)
                return [
                    {
                        "transaction": entry,
                        "details": self._switchm.config_history.details(
                            entry["transactionId"]
                        ),
                    }
                    for entry in found
                ]

            if now >= deadline:
                state = (
                    ", ".join(
                        f"{e.get('transactionId')}={e.get('deployStatus')}"
                        for e in found
                    )
                    or "no transaction appeared"
                )
                raise SmartZoneDeploymentTimeoutError(
                    f"Deployment in group {self.group_id} not finished after "
                    f"{timeout}s ({state})",
                    transactions=found,
                )
            time.sleep(poll_interval)


class DeploymentsResource(SwitchmResource):
    """Entry point for tracking config deployments (``client.switchm.deployments``)."""

    def track(
        self, group_id: str, switch_ids: Optional[Iterable[str]] = None
    ) -> DeploymentTracker:
        """Snapshot a group's history before a write; call ``wait()`` after it.

        Usable as a context manager::

            with client.switchm.deployments.track(group_id, [mac]) as tracker:
                client.switchm.port_settings.update(port_id, {"portName": "x"})
            tracker.wait()
        """
        return DeploymentTracker(self.switchm, group_id, switch_ids)

    def run(
        self,
        group_id: str,
        write: Callable[[], T],
        *,
        switch_ids: Optional[Iterable[str]] = None,
        timeout: float = 300.0,
        poll_interval: float = 5.0,
        settle: float = 15.0,
    ) -> Tuple[T, List[Dict[str, Any]]]:
        """Run ``write`` and wait for the deployments it starts.

        Returns:
            ``(write's return value, the finished deployments)``.
        """
        tracker = self.track(group_id, switch_ids)
        result = write()
        deployments = tracker.wait(
            timeout=timeout, poll_interval=poll_interval, settle=settle
        )
        return result, deployments
