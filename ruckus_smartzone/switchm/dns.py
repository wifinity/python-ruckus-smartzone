"""Switch group DNS config wrapper (``/dnsConfig``)."""

from typing import Any, Dict, Optional

from ruckus_smartzone.switchm.base import SwitchmResource


class DNSResource(SwitchmResource):
    """Operations on a switch group's DNS server config."""

    def get(self, group_id: str) -> Optional[Dict[str, Any]]:
        """Return a group's DNS config, ``{dns: {ip}, createdTime, updatedTime}``.

        A group with no DNS config answers with an empty ``ip`` and a zero
        ``createdTime``.
        """
        return self.switchm.get(f"dnsConfig/{group_id}")

    def create(self, group_id: str, ip: str) -> Optional[Dict[str, Any]]:
        """Create a group's DNS config."""
        return self.switchm.post("dnsConfig", json={"id": group_id, "dns": {"ip": ip}})

    def update(self, group_id: str, ip: str) -> Optional[Dict[str, Any]]:
        """Change a group's DNS server."""
        return self.switchm.put(f"dnsConfig/{group_id}", json={"dns": {"ip": ip}})

    def delete(self, group_id: str) -> Optional[Dict[str, Any]]:
        """Delete a group's DNS config."""
        return self.switchm.delete(f"dnsConfig/{group_id}")
