"""Resource wrappers for the SmartZone public API."""

from ruckus_smartzone.resources.access_points import (
    AccessPointsResource,
    MoveBatchResult,
    MoveResult,
)
from ruckus_smartzone.resources.ap_groups import APGroupsResource
from ruckus_smartzone.resources.wlan_groups import WLANGroupsResource
from ruckus_smartzone.resources.wlans import WLANsResource
from ruckus_smartzone.resources.zones import ZonesResource

__all__ = [
    "ZonesResource",
    "WLANsResource",
    "WLANGroupsResource",
    "AccessPointsResource",
    "APGroupsResource",
    "MoveResult",
    "MoveBatchResult",
]
