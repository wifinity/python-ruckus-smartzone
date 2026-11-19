"""Configuration history and job wrappers.

Every config deployment is a transaction in the group's configuration
history: ``deployStatus`` goes ``STARTED`` → ``SUCCESS`` | ``FAILURE``. The
per-switch detail carries the generated CLI (``clis``) and, on failure, the
failing line in ``dispatchFailedReason``. Config deployments do not appear in
``/job``, which holds firmware and scheduled jobs.
"""

from typing import Any, Dict, List, Optional

from ruckus_smartzone.const import DEFAULT_PAGE_SIZE
from ruckus_smartzone.mac import normalize_mac
from ruckus_smartzone.switchm.base import (
    SwitchmResource,
    switch_extra_filter,
    switch_filter,
)


class ConfigHistoryResource(SwitchmResource):
    """Read a switch group's configuration deployment history."""

    def query(
        self,
        group_id: str,
        criteria: Optional[Dict[str, Any]] = None,
        *,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> List[Dict[str, Any]]:
        """Return every transaction in a group's history.

        The controller lists the whole group history in no time order and
        ignores filters and sort fields on this endpoint; sort on
        ``startTime`` when order matters.
        """
        return self.switchm.query(
            f"configurationHistory/query/{group_id}", criteria, page_size=page_size
        )

    def details(self, transaction_id: str) -> List[Dict[str, Any]]:
        """Return the per-switch detail entries of one transaction."""
        return self.switchm.query(
            "configurationHistory/detail/query",
            switch_filter("transactionId", transaction_id),
        )


class JobsResource(SwitchmResource):
    """Read firmware and scheduled jobs (``/job``)."""

    def query(
        self,
        criteria: Optional[Dict[str, Any]] = None,
        *,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> List[Dict[str, Any]]:
        """Return jobs matching ``criteria``, every page."""
        return self.switchm.query("job", criteria, page_size=page_size)

    def list_switch(self, switch_id: str) -> List[Dict[str, Any]]:
        """Return the jobs of one switch."""
        return self.query(switch_extra_filter(normalize_mac(switch_id)))

    def get(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Return one job."""
        return self.switchm.get(f"job/{job_id}")
