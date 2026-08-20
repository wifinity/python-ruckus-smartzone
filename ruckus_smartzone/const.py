"""Shared constants for the Ruckus SmartZone client."""

# Pinned public API version. The controller also serves v11_0/v11_1/v12_0/v13_0.
API_VERSION = "v13_1"

# Public API prefix; the versioned base path is PUBLIC_API_PATH/API_VERSION.
PUBLIC_API_PATH = "/wsg/api/public"

# The service ticket is carried as this URL query parameter on every request
# (except logon), and on logoff.
SERVICE_TICKET_PARAM = "serviceTicket"

# Pagination: index/listSize with this shape of list response.
DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 1000
