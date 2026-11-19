"""Switch Manager ("switchm") sub-client.

SmartZone manages ICX switches through a separate service with its own REST
API at ``/switchm/api/<version>``. It accepts the public API's service ticket,
so :class:`SwitchManager` sends its requests through the owning
:class:`~ruckus_smartzone.client.SmartZoneClient` transport: ticket, 401
refresh, rate-limit and busy backoff, and URL masking are shared.

Switch Manager writes return at once and deploy to the switch later; see
:class:`~ruckus_smartzone.switchm.deployments.DeploymentsResource` for waiting
on the deployment.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional
from urllib.parse import urlsplit

from ruckus_smartzone.const import API_VERSION, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from ruckus_smartzone.const import SWITCHM_API_PATH
from ruckus_smartzone.resources.base import collect_pages
from ruckus_smartzone.switchm.aaa import AAAServersResource
from ruckus_smartzone.switchm.authentication import (
    FlexAuthProfilesResource,
    SwitchAuthenticationResource,
)
from ruckus_smartzone.switchm.backups import ConfigBackupsResource
from ruckus_smartzone.switchm.cli_templates import CLITemplatesResource
from ruckus_smartzone.switchm.deployments import DeploymentsResource
from ruckus_smartzone.switchm.dns import DNSResource
from ruckus_smartzone.switchm.groups import SwitchGroupsResource
from ruckus_smartzone.switchm.history import ConfigHistoryResource, JobsResource
from ruckus_smartzone.switchm.ports import PortSettingsResource
from ruckus_smartzone.switchm.switches import SwitchesResource
from ruckus_smartzone.switchm.vlans import VLANsResource

if TYPE_CHECKING:
    from ruckus_smartzone.client import SmartZoneClient


def switchm_base_url(public_base_url: str) -> str:
    """Return the versioned Switch Manager root for a controller.

    ``https://host:8443/wsg/api/public/v13_1/`` →
    ``https://host:8443/switchm/api/v13_1/``.
    """
    parts = urlsplit(public_base_url)
    return f"{parts.scheme}://{parts.netloc}{SWITCHM_API_PATH}/{API_VERSION}/"


class SwitchManager:
    """Low-level verbs and resource wrappers for the Switch Manager API.

    Paths passed to the verbs are relative to ``/switchm/api/v13_1/``.
    """

    def __init__(self, client: "SmartZoneClient", base_url: str) -> None:
        """Initialize the sub-client.

        Args:
            client: The owning :class:`SmartZoneClient`, whose transport is used.
            base_url: The versioned Switch Manager root, with a trailing slash.
        """
        self._client = client
        self.base_url = base_url

        self.groups = SwitchGroupsResource(self)
        self.switches = SwitchesResource(self)
        self.vlans = VLANsResource(self)
        self.port_settings = PortSettingsResource(self)
        self.aaa_servers = AAAServersResource(self)
        self.dns = DNSResource(self)
        self.authentication = SwitchAuthenticationResource(self)
        self.flex_auth_profiles = FlexAuthProfilesResource(self)
        self.cli_templates = CLITemplatesResource(self)
        self.config_backups = ConfigBackupsResource(self)
        self.config_history = ConfigHistoryResource(self)
        self.jobs = JobsResource(self)
        self.deployments = DeploymentsResource(self)

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path.lstrip('/')}"

    def get(
        self, path: str, *, params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Issue a GET and return the parsed JSON body."""
        return self._client._request("GET", self._url(path), params=params)

    def get_text(self, path: str, *, params: Optional[Dict[str, Any]] = None) -> str:
        """Issue a GET and return the body as text."""
        return self._client._request_text("GET", self._url(path), params=params)

    def post(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
    ) -> Optional[Dict[str, Any]]:
        """Issue a POST and return the parsed JSON body."""
        return self._client._request("POST", self._url(path), params=params, json=json)

    def put(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
    ) -> Optional[Dict[str, Any]]:
        """Issue a PUT and return the parsed JSON body."""
        return self._client._request("PUT", self._url(path), params=params, json=json)

    def patch(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
    ) -> Optional[Dict[str, Any]]:
        """Issue a PATCH and return the parsed JSON body."""
        return self._client._request("PATCH", self._url(path), params=params, json=json)

    def delete(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
    ) -> Optional[Dict[str, Any]]:
        """Issue a DELETE and return the parsed JSON body."""
        return self._client._request(
            "DELETE", self._url(path), params=params, json=json
        )

    def query(
        self,
        path: str,
        criteria: Optional[Dict[str, Any]] = None,
        *,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> List[Dict[str, Any]]:
        """POST a query body page by page and return every listed item.

        Switch Manager lists are POSTs taking ``{filters, extraFilters,
        fullTextSearch, page, limit}``; the valid filter types differ by
        endpoint.

        Args:
            path: Query endpoint path, e.g. ``switch`` or ``vlans/query``.
            criteria: Query fields merged into every page's body.
            page_size: Items per page; clamped to the API maximum (1000).
        """

        def fetch(page: int, limit: int) -> Optional[Dict[str, Any]]:
            body = dict(criteria or {})
            body["page"] = page
            body["limit"] = limit
            return self.post(path, json=body)

        return collect_pages(fetch, limit=min(page_size, MAX_PAGE_SIZE))

    def get_pages(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> List[Dict[str, Any]]:
        """GET a list endpoint paged by ``page``/``limit`` query parameters."""

        def fetch(page: int, limit: int) -> Optional[Dict[str, Any]]:
            page_params = dict(params or {})
            page_params["page"] = page
            page_params["limit"] = limit
            return self.get(path, params=page_params)

        return collect_pages(fetch, limit=min(page_size, MAX_PAGE_SIZE))
