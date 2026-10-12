# Documentation index

## Agent and operations

- [AGENTS.md](AGENTS.md) — codebase map for agents and contributors
- [README.md](../README.md) — install and usage
- [adr/0001-api-version-and-spec-availability.md](adr/0001-api-version-and-spec-availability.md) — API version + spec-availability decision
- [adr/0002-auth-session-and-transport.md](adr/0002-auth-session-and-transport.md) — service-ticket lifecycle, credential masking, transport resilience
- [adr/0003-resource-wrappers-zones-wlans-wlangroups.md](adr/0003-resource-wrappers-zones-wlans-wlangroups.md) — zone/WLAN/WLAN-group resource layer; rename-preserves-membership proof
- [adr/0004-access-points.md](adr/0004-access-points.md) — access-point resource layer; MAC normalisation, move chunking, pre-flight zone guard
- [adr/0005-ap-groups.md](adr/0005-ap-groups.md) — AP-group resource layer; radio→WLAN-group overrides, zone-guarded membership, PUT full-replace
- [adr/0006-firewall-and-precedence-profiles.md](adr/0006-firewall-and-precedence-profiles.md) — firewall/precedence profile read layer; global scope, name→id resolution
- [adr/0007-dpsk-keys.md](adr/0007-dpsk-keys.md) — WLAN DPSK key layer; create via batchGenUnbound, delete via POST idList, multipart upload

## Repository root

- [AGENTS.md](../AGENTS.md) — thin entry point
- [.agents/memory/python-ruckus-smartzone-repository-memory.md](../.agents/memory/python-ruckus-smartzone-repository-memory.md) — detailed memory
