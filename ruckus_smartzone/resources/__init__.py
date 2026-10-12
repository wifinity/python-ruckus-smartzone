"""Resource wrappers for the SmartZone public API."""

from ruckus_smartzone.resources.access_points import (
    AccessPointsResource,
    MoveBatchResult,
    MoveResult,
)
from ruckus_smartzone.resources.ap_groups import APGroupsResource
from ruckus_smartzone.resources.dpsk import DELETE_EXPIRED_INTERVALS, DPSKResource
from ruckus_smartzone.resources.firewall_profiles import FirewallProfilesResource
from ruckus_smartzone.resources.precedence_profiles import PrecedenceProfilesResource
from ruckus_smartzone.resources.wlan_groups import WLANGroupsResource
from ruckus_smartzone.resources.wlans import WLANsResource
from ruckus_smartzone.resources.zones import ZonesResource

__all__ = [
    "ZonesResource",
    "WLANsResource",
    "WLANGroupsResource",
    "AccessPointsResource",
    "APGroupsResource",
    "FirewallProfilesResource",
    "PrecedenceProfilesResource",
    "DPSKResource",
    "DELETE_EXPIRED_INTERVALS",
    "MoveResult",
    "MoveBatchResult",
]
