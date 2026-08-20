# 0002. Auth, session lifecycle and transport resilience

Date: 2026-08-20
Status: Accepted

## Context

The client authenticates to SmartZone with a **service ticket**: `POST
/serviceTicket` returns a ticket that is valid for 24 hours and, per the vendor
guide, is meant to be reused across calls. The ticket is carried as the
`serviceTicket` **URL query parameter** on every request except logon, and on
logoff (`DELETE /serviceTicket`).

Prior ad-hoc clients handled this poorly: some acquire a ticket and never log off
— leaking sessions against a session-capped controller — while others cache the
ticket for only a minute and re-authenticate constantly, and none mask the ticket,
so it lands in logs and exception text via the URL.

Two transport behaviours are also worth pinning down: a 429 is retried by reading
the `RateLimit-Reset` header; list endpoints page `index`/`listSize` over a
`{totalCount, hasMore, firstIndex, list}` shape; and a 403 carrying vendor
`errorCode` 211 means "not found".

## Decision

### Service ticket lifecycle

- Acquire lazily on first request and hold the ticket behind a `TicketCache`.
- Reuse the held ticket for its lifetime; **refresh reactively on a 401** (drop
  the ticket, re-acquire, retry the request once) rather than on a timer.
- Release on client close via `DELETE /serviceTicket`, best-effort and
  idempotent, so sessions are not leaked against a session-capped controller.
- The cache is a pluggable seam (`TicketCache` ABC) with an in-memory
  implementation only. A shared/Redis-backed implementation can slot in later;
  the seam exists so it lands without a client rewrite.

### Credential handling

The ticket is a URL query parameter, so masking targets the URL, not just
headers. `logging_config.mask_url()` redacts `serviceTicket` (case-insensitive)
wherever a request URL is logged; the client logs only masked URLs and never logs
response bodies, and disables the `httpx`/`httpcore` loggers so the transport
library cannot emit a raw URL. Exception messages carry the request method and
path (which hold no ticket), never the query string. A unit test asserts the
ticket reaches neither a log record nor an exception message.

### Transport resilience

- **Pagination:** `SmartZoneClient.paginate()` walks `index`/`listSize` (default
  100, clamped to the API maximum of 1000) over `{totalCount, hasMore,
  firstIndex, list}`, preferring `hasMore` and falling back to `totalCount`.
- **429:** read `RateLimit-Reset`, wait, and retry within the retry budget; raise
  `SmartZoneRateLimitError` once exhausted. No documented numeric limit exists, so
  handling stays reactive.
- **Controller busy / config-lock:** SmartZone serialises configuration writes, so
  a concurrent change can bounce a request. This is retried with bounded
  exponential backoff, then raised as `SmartZoneBusyError`.
- **Error mapping:** `raise_for_response()` maps HTTP status — and vendor
  `errorCode` where it changes meaning (403 + `errorCode` 211 → not found) — onto
  the `SmartZoneAPIError` hierarchy.

### Undocumented signals

The `v13_1` spec documents error responses by HTTP status only (400/403/422/500);
it defines no structured error body and no config-lock or rate-limit status. The
`errorCode`-211 rule and the busy signal are therefore **observed** behaviours,
not spec-derived. The busy signal is currently keyed on HTTP 423 and 503; its
exact form is confirmed by live verification below.

## Consequences

- `SmartZoneClient` is synchronous (`httpx.Client`) and used as a context
  manager.
- The pinned API version `v13_1` lives as a single constant (`const.API_VERSION`);
  the base URL is normalised to the versioned public API root.
- The resource wrappers (zones, WLANs, WLAN groups, access points) build on the
  low-level verbs and `paginate()`; the ticket lifecycle and resilience are not
  reimplemented per resource.

## Live verification

Verified against a SmartZone `v13_1` controller (SmartZone software `7.1.1.0.551`)
on 2026-08-20:

- **Logon and version.** A `v13_1` service ticket was issued; `controller_version`
  read back `7.1.1.0.551`, matching the anchor in ADR 0001.
- **Pagination.** `paginate("aps")` returned 1795 access points, spanning roughly
  18 pages of 100 — a real multi-page walk.
- **Masking.** The DEBUG request log rendered the ticket as
  `serviceTicket=%2A%2A%2A` (`***`); the raw ticket did not appear.
- **Release on close.** Capturing the ticket, calling `close()` (which sent
  `DELETE /serviceTicket`), then reusing that ticket returned **401** — the ticket
  is invalidated on close.

`GET /sessionManagement` was found to list only interactive admin sessions
(`authType: WEB_GUI`); the API service-ticket session does not appear there. So
`sessionManagement` is **not** a reliable check for an API ticket's state — the
reliable check is reusing the ticket and observing a 401, as above.

### Not verified

The controller-busy / config-lock signal was not exercised: forcing a
configuration lock on a live controller is unsafe. Busy retry stays keyed on HTTP
423/503 as an **assumption**, to be confirmed when a busy response is observed in
practice.
