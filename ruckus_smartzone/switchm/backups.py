"""Switch config backup wrapper (``/switchconfig``)."""

from typing import Any, Dict, Iterable, List, Optional

from ruckus_smartzone.const import DEFAULT_PAGE_SIZE
from ruckus_smartzone.exceptions import SmartZoneAPIError
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
        """Queue a config backup of each switch; ``master`` flags it as master.

        The controller starts queued backups only on five-minute boundaries, so
        one can take up to five minutes to reach ``SUCCESS`` in
        :meth:`list_switch`. :meth:`backup_now` starts one at once.
        """
        ids = [normalize_mac(mac) for mac in switch_ids]
        if not ids:
            raise ValueError("at least one switch id is required")
        params = None if master is None else {"master": str(master).lower()}
        return self.switchm.post("switchconfig/backup", params=params, json=ids)

    def backup_now(self, switch_id: str, switch_name: Optional[str] = None) -> str:
        """Start a config backup of one switch at once and return its backup id.

        Unlike :meth:`backup` it does not wait for the next five-minute
        boundary: the backup usually reaches ``SUCCESS`` in
        :meth:`list_switch` within about ten seconds.

        Raises:
            SmartZoneAPIError: The controller refused the backup or returned no
                backup id.
        """
        body: Dict[str, Any] = {"switchId": normalize_mac(switch_id)}
        if switch_name is not None:
            body["switchName"] = switch_name
        result = self.switchm.post("switchconfig/backup/manual", json=body) or {}
        error = result.get("errorMessage")
        backup_id = result.get("configBackupId")
        if error or not isinstance(backup_id, str) or not backup_id:
            raise SmartZoneAPIError(
                f"manual config backup of {body['switchId']} failed: {error or 'no backup id returned'}",
                response_data=result,
            )
        return backup_id

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
