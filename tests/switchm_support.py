"""Shared fixtures and helpers for the Switch Manager tests."""

import json
from typing import Any, List, Optional

import httpx
import respx

CONTROLLER = "https://smartzone.example:8443"
PUBLIC = f"{CONTROLLER}/wsg/api/public/v13_1"
SWITCHM = f"{CONTROLLER}/switchm/api/v13_1"

GROUP = "g-1"
MAC = "02:00:00:AA:BB:01"


def register_session(respx_mock: respx.MockRouter) -> None:
    respx_mock.post(f"{PUBLIC}/serviceTicket").mock(
        return_value=httpx.Response(200, json={"serviceTicket": "t-1"})
    )
    respx_mock.delete(f"{PUBLIC}/serviceTicket").mock(return_value=httpx.Response(204))


def page(
    items: List[Any], *, total: Optional[int] = None, has_more: Optional[bool] = None
) -> httpx.Response:
    body: dict = {"list": items}
    if total is not None:
        body["totalCount"] = total
    if has_more is not None:
        body["hasMore"] = has_more
    return httpx.Response(200, json=body)


def sent_json(route: respx.Route, index: int = -1) -> Any:
    """Return the JSON body of one recorded call of ``route``."""
    return json.loads(route.calls[index].request.content)
