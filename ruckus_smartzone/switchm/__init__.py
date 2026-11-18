"""Switch Manager ("switchm") support: ICX switches managed through SmartZone."""

from ruckus_smartzone.switchm.base import AUTHENTICATION_TYPES, build_body
from ruckus_smartzone.switchm.cli_templates import TEMPLATE_KINDS
from ruckus_smartzone.switchm.deployments import DeploymentTracker
from ruckus_smartzone.switchm.manager import SwitchManager, switchm_base_url

__all__ = [
    "AUTHENTICATION_TYPES",
    "TEMPLATE_KINDS",
    "DeploymentTracker",
    "SwitchManager",
    "build_body",
    "switchm_base_url",
]
