"""Switch config backup wrapper (``/switchconfig``)."""

from typing import Any, Dict, Iterable, List, Optional

from ruckus_smartzone.const import DEFAULT_PAGE_SIZE
from ruckus_smartzone.mac import normalize_mac
from ruckus_smartzone.switchm.base import SwitchmResource, switch_extra_filter


class ConfigBackupsResource(SwitchmResource):
    """Operations on switch configuration backups and master-backup drift alerts."""

    def query(
        self,
        criteria: Optional[Dict[str, Any]] = None,
        *,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> List[Dict[str, Any]]:
        """Return backups matching ``criteria``, every page."""
        return self.switchm.query("switchconfig", criteria, page_size=page_size)

    def list_switch(self, switch_id: str) -> List[Dict[str, Any]]:
        """Return a switch's backups (``id``, ``name``, ``type``, ``status``, ``timestamp``)."""
        return self.query(switch_extra_filter(normalize_mac(switch_id)))

    def backup(
        self, switch_ids: Iterable[str], *, master: Optional[bool] = None
    ) -> Optional[Dict[str, Any]]:
        """Start a config backup of each switch; ``master`` flags it as master.

        The backup runs asynchronously; a manual backup takes a couple of
        minutes to reach ``SUCCESS`` in :meth:`list_switch`.
        """
        ids = [normalize_mac(mac) for mac in switch_ids]
        if not ids:
            raise ValueError("at least one switch id is required")
        params = None if master is None else {"master": str(master).lower()}
        return self.switchm.post("switchconfig/backup", params=params, json=ids)

    def content(self, config_id: str) -> str:
        """Return a backup's content: the switch's running config as text."""
        return self.switchm.get_text(f"switchconfig/download/{config_id}")

    def delete(self, config_id: str) -> Optional[Dict[str, Any]]:
        """Delete one backup."""
        return self.switchm.delete(f"switchconfig/{config_id}")

    def master_alerts(self) -> List[Dict[str, Any]]:
        """Return the switches whose latest backup differs from their master backup.

        The comparison is a plain text diff of backups, so the controller's own
        pushes count as drift too.
        """
        return self.switchm.get_pages("switchconfig/backup/master/alert")

    def master_alert(self, switch_id: str) -> Optional[Dict[str, Any]]:
        """Return the diff between a switch's master and latest backup."""
        return self.switchm.get(
            f"switchconfig/backup/master/alert/{normalize_mac(switch_id)}"
        )
