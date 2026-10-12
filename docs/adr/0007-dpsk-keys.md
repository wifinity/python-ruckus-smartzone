# 0007. DPSK key resource wrapper

Date: 2026-10-12
Status: Accepted

## Context

A DPSK-enabled WLAN authenticates each user with their own passphrase (a DPSK
key). The WLAN itself is created through the dict-first `client.wlans.create`;
the keys live in a separate per-WLAN collection that callers need to create,
look up, rename and remove.

The `v13_1` spec shapes the surface as:

- `GET /rkszones/{zoneId}/wlans/{id}/dpsk` — list, `index`/`listSize` paging over
  `{totalCount, hasMore, firstIndex, list}`.
- `GET /rkszones/{zoneId}/wlans/{id}/dpsk/{dpskId}` — detail, typed as the same
  paged *list* shape (`dpsk_getDpskInfoList`) rather than a single object.
- `PATCH …/dpsk/{dpskId}` — body `dpsk_updateDpsk`, whose only property is
  `userName`.
- `POST …/dpsk` — **deletes** keys: body `{idList: [...]}`, response
  `{resultCount}`. There is no per-key `DELETE`.
- `POST …/dpsk/batchGenUnbound` — the only JSON create: `{amount, passphraseList,
  userName, vlanId, userRoleId, groupDpsk}`, response `{resultCount,
  dpskInfoList}`. The spec says `amount` above 1 suffixes `userName` with
  `-1`, `-2`, …; the controller actually uses a zero-based `_0`, `_1`, ….
  There is no single-key create.
- `POST …/dpsk/upload` — `multipart/form-data` with an `uploadFile` CSV part.
- `GET /rkszones/{zoneId}/dpsk` — every key in the zone across its WLANs.
- `GET`/`PUT /rkszones/{zoneId}/deleteExpiredDpsk` — zone setting
  `deleteExpiredDpsk` ∈ `Never`, `AfterOneDay`, `AfterSixMonths`.

`dpsk_dpskInfo` (the key object) declares no properties in the spec; the live
controller returns `id` (UUID), `userName`, `passphrase`, `vlanId`, `userRoleId`,
`groupDpsk`, `macAddress`, `wlanId`, `creationDateTime`, `expirationDateTime`.

## Decision

- A `DPSKResource` reached as `client.dpsk`, dict-first like the other wrappers.
  The request bodies are small and fixed, so methods take typed keyword arguments
  and map them to the camelCase body, sending only the arguments supplied.
- `generate` wraps `batchGenUnbound`; `create` is its one-key form
  (`amount=1`, optional single-element `passphraseList`, optional `group_dpsk`)
  and returns the created key, raising `SmartZoneAPIError` when the controller
  reports none.
- `delete_many` POSTs the `idList` and returns the deleted count; an empty id list
  makes no request. `delete` is its one-id form.
- `update` sends exactly `{userName}`.
- `get` unwraps a single-item `list` to the key itself and raises
  `SmartZoneNotFoundError` on an empty one; a plain object passes through.
- `find_by_user_name` matches `userName` exactly with the same not-found /
  duplicate semantics as the shared `find_one_by_name` (which keys on `name`).
- `set_delete_expired` validates the interval client-side before any request.
- `upload` takes CSV text or bytes. `SmartZoneClient.post` accepts a `files`
  argument passed through to `httpx`; content is held as bytes so the 401
  ticket-refresh retry resends the same body.
- The zone-wide `POST /query/dpsk` and `GET /rkszones/{zoneId}/dpskEnabledWlans`
  are left out until a caller needs them.

## Consequences

- The controller does not enforce unique user names, so callers create keys
  idempotently by `find_by_user_name` → `create` on `SmartZoneNotFoundError`;
  `find_by_user_name` raising `ValueError` signals duplicates already exist.
- Deleting a key is a POST, so request logs and permission audits show a POST to
  the collection rather than a DELETE.
- Renaming is the only in-place edit; changing a key's passphrase or VLAN means
  deleting and recreating it.

## Live verification

Run against auto1 (`v13_1`, SmartZone 7.1.1.0.551) on 2026-10-12 in a throwaway
WLAN in the PRODUCT_TEST zone; every object was removed afterwards.

- **DPSK WLAN creation.** `POST /rkszones/{zoneId}/wlans` with a `dpsk` block
  returns HTTP 500 (`errorCode 0`, no message), with or without
  `encryption.mfp`. Creating a plain WPA2 WLAN
  (`encryption: {method: WPA2, algorithm: AES, passphrase, mfp: disabled}`) and
  then `PATCH {dpsk: {dpskEnabled: true}}` succeeds; the WLAN reports
  `dpskType: Secure`, `length: 62`, `expiration: Unlimited`,
  `dpskFromType: CreateTime`.
- **create / generate.** One key with a given passphrase, one generated with a
  VLAN, a batch of three, and group keys (`groupDpsk: true`) with given and
  generated passphrases all succeed (HTTP 201). Batch names are suffixed `_0`,
  `_1`, `_2`; a one-key create is not suffixed.
- **Uniqueness.** A reused passphrase is rejected with HTTP 422 (`errorCode 302`,
  "passphrase is already existed") for individual and group keys. A duplicate
  `userName` is accepted.
- **Reads.** `list` and `list_zone` page normally. The detail `GET` returns the
  paged list shape, which `get` unwraps. An unknown key id returns 403
  `errorCode 211`, mapped to `SmartZoneNotFoundError`.
- **update.** `PATCH {userName}` returns 204; the key keeps its id and passphrase.
- **upload.** The CSV header (from `GET /rkszones/downloadDpskCsvSample`) is
  `User Name,MAC Address,VLAN ID,User Role,Passphrase,Group DPSK`; empty MAC binds
  the key to its first user's MAC, `Y` in the last column makes a group key. A
  two-row upload returns 201 with `resultCount` 2. An upload containing a reused
  passphrase is rejected as a whole (422), creating none of its rows.
- **delete.** `delete` returns 1, `delete_many` returns the count removed, and
  deleting an id that no longer exists returns 0 without error.
- **delete-expired.** `GET` returns `{deleteExpiredDpsk: "Never"}`; writing the
  same value back returns 204.
