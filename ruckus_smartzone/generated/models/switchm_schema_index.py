"""Auto-generated schema index from the Swagger 2.0 spec.
Do not edit manually.
"""

SWITCHM_SCHEMA_INDEX: dict[str, dict] = {
    "aaaServers_AAAServer": {
        "additionalProperties": False,
        "properties": {
            "acctPort": {
                "description": "AAA server " "accounting port",
                "type": "integer",
            },
            "altoId": {"description": "Alto Id", "type": "string"},
            "authPort": {
                "description": "AAA server " "authentication " "port",
                "type": "integer",
            },
            "createdTime": {
                "description": "The create " "time of the " "AAA server",
                "format": "int64",
                "type": "integer",
            },
            "creatorId": {"description": "AAA server " "creator Id", "type": "string"},
            "creatorUsername": {
                "description": "AAA " "server " "creator " "name",
                "type": "string",
            },
            "groupId": {
                "description": "Group ID of the " "AAA server",
                "type": "string",
            },
            "id": {"description": "AAA server ID", "type": "string"},
            "ip": {"description": "AAA server IP address", "type": "string"},
            "level": {
                "description": "Access level of AAA " "server",
                "enum": ["READ_WRITE", "PORT_CONFIG", "READ_ONLY"],
                "type": "string",
            },
            "name": {"description": "Name of the AAA " "server", "type": "string"},
            "password": {"description": "Password for " "local user", "type": "string"},
            "purpose": {
                "description": "AAA server " "purpose",
                "enum": [
                    "DEFAULT",
                    "AUTHENTICATION_ONLY",
                    "AUTHORIZATION_ONLY",
                    "ACCOUNTING_ONLY",
                ],
                "type": "string",
            },
            "secret": {"description": "AAA server secret", "type": "string"},
            "serverType": {
                "description": "The server " "tpye of the " "AAA server",
                "enum": ["RADIUS", "TACACS_PLUS", "LOCAL"],
                "type": "string",
            },
            "updatedTime": {
                "description": "The modify " "time of the " "AAA server",
                "format": "int64",
                "type": "integer",
            },
            "updaterId": {"description": "AAA server " "updater Id", "type": "string"},
            "updaterUsername": {
                "description": "AAA " "server " "updater " "name",
                "type": "string",
            },
            "username": {"description": "Username for " "local user", "type": "string"},
        },
        "type": "object",
    },
    "aaaServers_aaaServersQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "AAA "
                "Server "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "AAA "
                "Server "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "AAA "
                "Servers "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/aaaServers_AAAServer"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "AAA " "Servers " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total "
                "AAA "
                "Servers "
                "count "
                "in "
                "this "
                "response",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "aaaServers_createAdminAAAServer": {
        "additionalProperties": False,
        "properties": {
            "acctPort": {
                "description": "AAA " "server " "accounting " "port",
                "type": "integer",
            },
            "altoId": {"description": "Alto Id", "type": "string"},
            "authPort": {
                "description": "AAA " "server " "authentication " "port",
                "type": "integer",
            },
            "ip": {"description": "AAA server " "IP address", "type": "string"},
            "level": {
                "description": "Access " "level of " "AAA " "server",
                "enum": ["READ_WRITE", "PORT_CONFIG", "READ_ONLY"],
                "type": "string",
            },
            "name": {
                "description": "Name of " "the AAA " "server",
                "pattern": '^(?:(?!").)*$',
                "type": "string",
            },
            "password": {
                "description": "Password " "for " "local " "user",
                "pattern": "^(?:(?!!).)*$",
                "type": "string",
            },
            "purpose": {
                "description": "AAA " "server " "purpose",
                "enum": [
                    "DEFAULT",
                    "AUTHENTICATION_ONLY",
                    "AUTHORIZATION_ONLY",
                    "ACCOUNTING_ONLY",
                ],
                "type": "string",
            },
            "secret": {"description": "AAA " "server " "secret", "type": "string"},
            "serverType": {
                "description": "The " "server " "tpye " "of " "the " "AAA " "server",
                "enum": ["RADIUS", "TACACS_PLUS", "LOCAL"],
                "type": "string",
            },
            "username": {
                "description": "Username " "for " "local " "user",
                "pattern": '^(?:(?!")(?!\\s).)*$',
                "type": "string",
            },
        },
        "type": "object",
    },
    "aaaServers_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "aaaSettings_AAASetting": {
        "additionalProperties": False,
        "properties": {
            "accounting": {
                "additionalProperties": False,
                "description": "Accounting " "service",
                "properties": {
                    "commands": {
                        "additionalProperties": False,
                        "description": "Commands " "service",
                        "properties": {
                            "level": {
                                "description": "Access " "level " "of " "command",
                                "enum": ["READ_WRITE", "PORT_CONFIG", "READ_ONLY"],
                                "type": "string",
                            },
                            "server1": {
                                "description": "Primary " "server " "type",
                                "enum": ["RADIUS", "TACACS_PLUS"],
                                "type": "string",
                            },
                            "server2": {
                                "description": "Secondary " "server " "type",
                                "enum": ["RADIUS", "TACACS_PLUS"],
                                "type": "string",
                            },
                        },
                        "type": "object",
                    },
                    "enabledCommandAccounting": {
                        "description": "Command " "Enabled",
                        "type": "boolean",
                    },
                    "enabledExecAccounting": {
                        "description": "Exec " "Enabled",
                        "type": "boolean",
                    },
                    "exec": {
                        "additionalProperties": False,
                        "description": "Exec " "service",
                        "properties": {
                            "server1": {
                                "description": "Primary " "server " "type",
                                "enum": ["RADIUS", "TACACS_PLUS"],
                                "type": "string",
                            },
                            "server2": {
                                "description": "Secondary " "server " "type",
                                "enum": ["RADIUS", "TACACS_PLUS"],
                                "type": "string",
                            },
                        },
                        "type": "object",
                    },
                },
                "type": "object",
            },
            "altoId": {"description": "Alto Id", "type": "string"},
            "authentication": {
                "additionalProperties": False,
                "description": "Authentication " "service",
                "properties": {
                    "enableTelnetAuthn": {
                        "description": "Telnet " "Enabled",
                        "type": "boolean",
                    },
                    "enabledSSHAuthn": {
                        "description": "SSH " "Enabled",
                        "type": "boolean",
                    },
                    "firstPref": {
                        "description": "Primary " "server " "type",
                        "enum": ["RADIUS", "TACACS_PLUS", "LOCAL"],
                        "type": "string",
                    },
                    "secondPref": {
                        "description": "Secondary " "server " "type",
                        "enum": ["RADIUS", "TACACS_PLUS", "LOCAL"],
                        "type": "string",
                    },
                    "thirdPref": {
                        "description": "Third " "server " "type",
                        "enum": ["RADIUS", "TACACS_PLUS", "LOCAL"],
                        "type": "string",
                    },
                },
                "type": "object",
            },
            "authorization": {
                "additionalProperties": False,
                "description": "Authorization " "service",
                "properties": {
                    "commands": {
                        "additionalProperties": False,
                        "description": "Commands " "service",
                        "properties": {
                            "level": {
                                "description": "Access " "level " "of " "command",
                                "enum": ["READ_WRITE", "PORT_CONFIG", "READ_ONLY"],
                                "type": "string",
                            },
                            "server1": {
                                "description": "Primary " "server " "type",
                                "enum": ["RADIUS", "TACACS_PLUS"],
                                "type": "string",
                            },
                            "server2": {
                                "description": "Secondary " "server " "type",
                                "enum": ["RADIUS", "TACACS_PLUS"],
                                "type": "string",
                            },
                        },
                        "type": "object",
                    },
                    "enabledCommandAuthz": {
                        "description": "Command " "Enabled",
                        "type": "boolean",
                    },
                    "enabledExecAuthz": {
                        "description": "Exec " "Enabled",
                        "type": "boolean",
                    },
                    "exec": {
                        "additionalProperties": False,
                        "description": "Exec " "Service",
                        "properties": {
                            "server1": {
                                "description": "Primary " "server " "type",
                                "enum": ["RADIUS", "TACACS_PLUS"],
                                "type": "string",
                            },
                            "server2": {
                                "description": "Secondary " "server " "type",
                                "enum": ["RADIUS", "TACACS_PLUS"],
                                "type": "string",
                            },
                        },
                        "type": "object",
                    },
                },
                "type": "object",
            },
        },
        "type": "object",
    },
    "aaaSettings_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "aclConfig_ACLConfig": {
        "additionalProperties": False,
        "properties": {
            "aclRule": {
                "items": {"$ref": "#/definitions/aclConfig_ACLRule"},
                "type": "array",
            },
            "aclType": {
                "description": "ACL Type",
                "enum": ["STANDARD", "EXTENDED"],
                "type": "string",
            },
            "altoId": {"description": "Alto Id", "type": "string"},
            "createdTime": {
                "description": "The create " "time of the " "AccessControl",
                "format": "int64",
                "type": "integer",
            },
            "familyId": {"description": "Family Id", "type": "string"},
            "groupId": {"description": "Switch Group Id", "type": "string"},
            "id": {"description": "Id", "type": "string"},
            "name": {"description": "ACL Name/ID", "type": "string"},
            "pushTime": {
                "description": "Puch Schedule " "Time",
                "format": "int64",
                "type": "integer",
            },
            "pushTimeType": {
                "description": "Puch Config " "Type",
                "enum": ["NOW", "SCHEDULE"],
                "type": "string",
            },
            "switchId": {"description": "Switch Id", "type": "string"},
            "updatedTime": {
                "description": "The modify " "time of the " "AccessControl",
                "format": "int64",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "aclConfig_ACLConfigsQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "AccessControl "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "AccessControl "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "AccessControl "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/aclConfig_ACLConfig"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "AccessControl " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total "
                "AccessControl "
                "count "
                "in "
                "this "
                "response",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "aclConfig_ACLRule": {
        "additionalProperties": False,
        "properties": {
            "action": {
                "description": "The action of " "AccessControl Rule",
                "enum": ["PERMIT", "DENY"],
                "type": "string",
            },
            "destNetwork": {
                "description": "The destination " "network of " "AccessControl " "Rule",
                "type": "string",
            },
            "destPort": {
                "description": "The destination " "port of " "AccessControl Rule",
                "type": "string",
            },
            "dscpMarking": {
                "description": "The DSCP value "
                "to be used for "
                "marking of "
                "AccessControl "
                "Rule",
                "type": "integer",
            },
            "dscpMatching": {
                "description": "The DSCP value "
                "for matching of "
                "AccessControl "
                "Rule",
                "type": "integer",
            },
            "internalPriority": {
                "description": "The QoS " "priority of " "AccessControl " "Rule",
                "type": "integer",
            },
            "protocol": {
                "description": "The protocol of " "AccessControl Rule",
                "enum": ["IP", "TCP", "UDP"],
                "type": "string",
            },
            "seq": {
                "description": "The seq of AccessControl " "Rule",
                "type": "integer",
            },
            "srcNetwork": {
                "description": "The source " "network of " "AccessControl " "Rule",
                "type": "string",
            },
            "srcPort": {
                "description": "The source port of " "AccessControl Rule",
                "type": "string",
            },
            "trafficPolicy": {
                "description": "The Traffic " "Policy Id of " "AccessControl " "Rule",
                "type": "string",
            },
        },
        "type": "object",
    },
    "aclConfig_createACLConfig": {
        "additionalProperties": False,
        "properties": {
            "aclRule": {
                "items": {"$ref": "#/definitions/aclConfig_ACLRule"},
                "type": "array",
            },
            "aclType": {
                "description": "ACL Type",
                "enum": ["STANDARD", "EXTENDED"],
                "type": "string",
            },
            "altoId": {"description": "Alto Id", "type": "string"},
            "familyId": {"description": "Family Id", "type": "string"},
            "groupId": {"description": "Switch Group " "Id", "type": "string"},
            "name": {"description": "ACL Name/ID", "type": "string"},
            "pushTime": {
                "description": "Puch " "Schedule " "Time",
                "format": "int64",
                "type": "integer",
            },
            "pushTimeType": {
                "description": "Puch " "Config " "Type",
                "enum": ["NOW", "SCHEDULE"],
                "type": "string",
            },
            "switchId": {"description": "Switch Id", "type": "string"},
            "switchIdList": {
                "description": "Switch " "ID List",
                "items": {"type": "string"},
                "type": "array",
            },
        },
        "type": "object",
    },
    "aclConfig_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "aclConfig_updateACLConfig": {
        "additionalProperties": False,
        "properties": {
            "aclRule": {
                "items": {"$ref": "#/definitions/aclConfig_ACLRule"},
                "type": "array",
            },
            "aclType": {
                "description": "ACL Type",
                "enum": ["STANDARD", "EXTENDED"],
                "type": "string",
            },
            "altoId": {"description": "Alto Id", "type": "string"},
            "pushTime": {
                "description": "Puch " "Schedule " "Time",
                "format": "int64",
                "type": "integer",
            },
            "pushTimeType": {
                "description": "Puch " "Config " "Type",
                "enum": ["NOW", "SCHEDULE"],
                "type": "string",
            },
        },
        "type": "object",
    },
    "authentication_Authentication": {
        "additionalProperties": False,
        "properties": {
            "altoId": {
                "description": "Alto Id " "of the " "Authentication",
                "type": "string",
            },
            "authDefaultVlan": {
                "description": "The "
                "VLAN "
                "where "
                "authenticated "
                "clients "
                "get "
                "placed "
                "in",
                "type": "integer",
                "x-isnullable": True,
            },
            "authEnable": {
                "description": "Flexible "
                "Authentication "
                "is "
                "enabled "
                "or "
                "disabled",
                "type": "boolean",
            },
            "createdTime": {
                "description": "The " "create " "time " "of " "the " "Authentication",
                "type": "integer",
            },
            "groupId": {
                "description": "Switch " "group Id " "of the " "Authentication",
                "type": "string",
            },
            "guestVlan": {
                "description": "The "
                "VLAN "
                "where "
                "clients "
                "get "
                "placed "
                "when "
                "there "
                "is no "
                "response "
                "from "
                "the "
                "client",
                "type": "integer",
                "x-isnullable": True,
            },
            "id": {
                "description": "Identifier of " "the " "Authentication",
                "type": "string",
            },
            "updatedTime": {
                "description": "The " "modify " "time " "of " "the " "Authentication",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "authentication_UpdateAuthentication": {
        "additionalProperties": False,
        "properties": {
            "altoId": {
                "description": "Alto " "Id " "of " "the " "Authentication",
                "type": "string",
            },
            "authDefaultVlan": {
                "description": "The "
                "VLAN "
                "where "
                "authenticated "
                "clients "
                "get "
                "placed "
                "in",
                "type": "integer",
                "x-isnullable": True,
            },
            "authEnable": {
                "description": "Flexible "
                "Authentication "
                "is "
                "enabled "
                "or "
                "disabled",
                "type": "boolean",
            },
            "guestVlan": {
                "description": "The "
                "VLAN "
                "where "
                "clients "
                "get "
                "placed "
                "when "
                "there "
                "is "
                "no "
                "response "
                "from "
                "the "
                "client",
                "type": "integer",
                "x-isnullable": True,
            },
        },
        "type": "object",
    },
    "authentication_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "bgpEvpn_attributeEntriesRequest": {
        "additionalProperties": False,
        "properties": {
            "ip": {"description": "IP Address", "type": "string"},
            "mac": {"description": "MAC " "Address", "type": "string"},
            "vni": {"description": "VNI", "type": "integer"},
        },
        "type": "object",
    },
    "bgpEvpn_bgpEvpnListResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {"description": "Extra", "type": "object"},
            "firstIndex": {"description": "First " "index", "type": "integer"},
            "hasMore": {"description": "Has more", "type": "boolean"},
            "list": {
                "items": {"$ref": "#/definitions/bgpEvpn_simpleBgpEvpn"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Raw " "data " "total " "count",
                "type": "integer",
            },
            "totalCount": {"description": "Total " "count", "type": "integer"},
        },
        "type": "object",
    },
    "bgpEvpn_bgpNeighbor": {
        "additionalProperties": False,
        "properties": {
            "overlayGatewayId": {
                "description": "Overlay "
                "Gateway "
                "ID, "
                "format is "
                "[mac_loopbackId_loopbackIp]",
                "type": "string",
            },
            "overlayGatewayName": {
                "description": "Overlay " "Gateway " "Name",
                "type": "string",
            },
            "overlayGatewaySameAsBgp": {
                "description": "Overlay " "Gateway " "Is " "Same " "As " "BGP",
                "type": "boolean",
            },
            "sourceInterfaceId": {
                "description": "Source "
                "Interface "
                "ID, "
                "format "
                "is "
                "[mac_loopbackId_loopbackIp]",
                "type": "string",
            },
            "switchId": {"description": "Switch ID", "type": "string"},
            "vlans": {"description": "Overlay Gateway " "VLANs", "type": "string"},
            "vniStart": {
                "description": "Overlay Gateway " "VNI Start",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "bgpEvpn_bgpNeighborBo": {
        "additionalProperties": False,
        "properties": {
            "bgpNeighbors": {
                "items": {"$ref": "#/definitions/bgpEvpn_neighborBo"},
                "type": "array",
            },
            "localAs": {"description": "BGP eVPN " "Local-As", "type": "integer"},
            "totalEstablishedNeighbors": {
                "description": "Total " "Established " "Neighbors",
                "type": "integer",
            },
            "totalImetRoutes": {
                "description": "Total " "iMET " "Routesresources.properties",
                "type": "integer",
            },
            "totalMacRoutes": {"description": "Total " "Routes", "type": "integer"},
            "totalNeighbors": {"description": "Total " "Neighbors", "type": "integer"},
        },
        "type": "object",
    },
    "bgpEvpn_bgpNeighborResult": {
        "additionalProperties": False,
        "properties": {
            "overlayGatewayId": {
                "description": "Overlay "
                "Gateway "
                "ID, "
                "format "
                "is "
                "[mac_loopbackId_loopbackIp]",
                "type": "string",
            },
            "overlayGatewayName": {
                "description": "Overlay " "Gateway " "Name",
                "type": "string",
            },
            "overlayGatewaySameAsBgp": {
                "description": "Overlay " "Gateway " "Is " "Same " "As " "BGP",
                "type": "boolean",
            },
            "sourceInterfaceId": {
                "description": "Source "
                "Interface "
                "ID, "
                "format "
                "is "
                "[mac_loopbackId_loopbackIp]",
                "type": "string",
            },
            "switchId": {"description": "Switch ID", "type": "string"},
            "switchName": {"description": "Switch " "Name", "type": "string"},
            "vlans": {"description": "Overlay " "Gateway VLANs", "type": "string"},
            "vniStart": {
                "description": "Overlay " "Gateway VNI " "Start",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "bgpEvpn_commonResult": {
        "additionalProperties": False,
        "properties": {
            "data": {"type": "string"},
            "error": {"$ref": "#/definitions/bgpEvpn_errorObject"},
            "extra": {"type": "object"},
            "metaData": {"type": "object"},
            "success": {"type": "boolean"},
        },
        "type": "object",
    },
    "bgpEvpn_createBgpEvpnProfile": {
        "additionalProperties": False,
        "properties": {
            "ethernetSegments": {
                "description": "BGP " "eVPN " "Ethernet " "Segments",
                "items": {"$ref": "#/definitions/bgpEvpn_ethernetSegment"},
                "type": "array",
            },
            "groupId": {"description": "BGP eVPN " "group ID", "type": "string"},
            "ibgpNeighbors": {
                "description": "BGP " "eVPN " "Neighbors",
                "items": {"$ref": "#/definitions/bgpEvpn_bgpNeighbor"},
                "type": "array",
            },
            "localAs": {"description": "BGP eVPN " "Local-As", "type": "integer"},
            "name": {"description": "BGP eVPN " "Profile name", "type": "string"},
            "routeReflectServer": {"$ref": "#/definitions/bgpEvpn_bgpNeighbor"},
        },
        "type": "object",
    },
    "bgpEvpn_createEvpnInstance": {
        "additionalProperties": False,
        "properties": {
            "arpSuppressionEnable": {
                "description": "BGP "
                "eBVPN "
                "Instance "
                "ARP "
                "Suppression "
                "enable",
                "type": "boolean",
            },
            "macDuplicateExpire": {
                "description": "BGP " "eBVPN " "Instance " "MAC " "duplicate " "expire",
                "type": "string",
            },
            "macDuplicateLimit": {
                "description": "BGP " "eBVPN " "Instance " "MAC " "duplicate " "limit",
                "type": "string",
            },
            "routeTargetDistinguisher": {
                "description": "BGP "
                "eBVPN "
                "Instance "
                "Route "
                "Target "
                "Distinguisher",
                "type": "string",
            },
            "routeTargetExport": {
                "description": "BGP " "eBVPN " "Instance " "Route " "Target " "Export",
                "type": "string",
            },
            "routeTargetImportList": {
                "description": "BGP "
                "eBVPN "
                "Instance "
                "Route "
                "Target "
                "Import "
                "List",
                "items": {"type": "string"},
                "type": "array",
            },
            "vlanId": {
                "description": "BGP eBVPN " "Instance " "VLAN",
                "type": "integer",
            },
            "vni": {"description": "BGP eBVPN " "Instance VNI", "type": "integer"},
        },
        "type": "object",
    },
    "bgpEvpn_createEvpnInstances": {
        "additionalProperties": False,
        "properties": {
            "evpnInstances": {
                "description": "BGP " "eVPN " "Instances",
                "items": {"$ref": "#/definitions/bgpEvpn_createEvpnInstance"},
                "type": "array",
            }
        },
        "type": "object",
    },
    "bgpEvpn_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "bgpEvpn_errorObject": {
        "additionalProperties": False,
        "properties": {
            "list": {"items": {"type": "string"}, "type": "array"},
            "message": {"type": "string"},
            "msgKey": {"type": "string"},
        },
        "type": "object",
    },
    "bgpEvpn_ethernetSegment": {
        "additionalProperties": False,
        "properties": {
            "esi": {"description": "Ethernet Segment " "Identifier", "type": "string"},
            "id": {"description": "Ethernet Segment ID", "type": "string"},
            "lacpMacAddress": {
                "description": "LACP " "MAC " "Address",
                "type": "string",
            },
            "lacpPortKey": {"description": "LACP Port " "Key", "type": "string"},
            "lagId": {
                "description": "LAG Id for " "Ethernet Segment",
                "type": "string",
            },
            "localDiscriminator": {
                "description": "Local " "Discriminator",
                "type": "string",
            },
            "macAddress": {"description": "MAC Address", "type": "string"},
            "redundancyMode": {
                "description": "Ethernet "
                "Segment's "
                "Redundancy "
                "Mode, "
                "SINGLE_ACTIVE "
                "or "
                "ALL_ACTIVE",
                "enum": ["ALL_ACTIVE", "SINGLE_ACTIVE"],
                "type": "string",
            },
            "switchIds": {
                "description": "Switches at " "Ethernet " "Segment",
                "items": {"type": "string"},
                "type": "array",
            },
            "type": {
                "description": "Ethernet Segment " "Type, only accept " "0, 1 or 3",
                "enum": ["0", "1", "3"],
                "type": "string",
            },
        },
        "type": "object",
    },
    "bgpEvpn_evpnInstanceListResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {"description": "Extra", "type": "object"},
            "firstIndex": {"description": "First " "index", "type": "integer"},
            "hasMore": {"description": "Has " "more", "type": "boolean"},
            "list": {
                "items": {"$ref": "#/definitions/bgpEvpn_updateEvpnInstance"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Raw " "data " "total " "count",
                "type": "integer",
            },
            "totalCount": {"description": "Total " "count", "type": "integer"},
        },
        "type": "object",
    },
    "bgpEvpn_getBgpEvpnProfile": {
        "additionalProperties": False,
        "properties": {
            "ethernetSegments": {
                "description": "BGP " "eVPN " "Ethernet " "Segments",
                "items": {"$ref": "#/definitions/bgpEvpn_ethernetSegment"},
                "type": "array",
            },
            "ibgpNeighbors": {
                "description": "BGP " "eVPN " "Neighbors",
                "items": {"$ref": "#/definitions/bgpEvpn_bgpNeighborResult"},
                "type": "array",
            },
            "id": {"description": "BGP eVPN Profile " "ID", "type": "string"},
            "localAs": {"description": "BGP eVPN " "Local-As", "type": "integer"},
            "name": {"description": "BGP eVPN name", "type": "string"},
            "routeReflectServer": {"$ref": "#/definitions/bgpEvpn_bgpNeighborResult"},
        },
        "type": "object",
    },
    "bgpEvpn_macAddressTableRequest": {
        "additionalProperties": False,
        "properties": {"mac": {"description": "MAC Address", "type": "string"}},
        "type": "object",
    },
    "bgpEvpn_neighborBo": {
        "additionalProperties": False,
        "properties": {
            "connectionState": {"description": "Connection " "State", "type": "string"},
            "imetRoutes": {"description": "iMET Routes", "type": "integer"},
            "ip": {"description": "IP Address", "type": "string"},
            "macRoutes": {"description": "MAC Routes", "type": "integer"},
            "remoteAs": {"description": "Remote-As", "type": "integer"},
            "uptime": {"description": "Uptime", "type": "string"},
        },
        "type": "object",
    },
    "bgpEvpn_simpleBgpEvpn": {
        "additionalProperties": False,
        "properties": {
            "id": {"description": "BGP eVPN Profile ID", "type": "string"},
            "localAs": {
                "description": "BGP eVPN Profile " "Local-As",
                "type": "integer",
            },
            "name": {"description": "BGP eVPN Profile " "name", "type": "string"},
            "switches": {
                "description": "BGP eVPN " "Profile " "Switches",
                "items": {"type": "string"},
                "type": "array",
            },
            "type": {"description": "BGP eVPN Profile " "Type", "type": "string"},
        },
        "type": "object",
    },
    "bgpEvpn_updateBgpEvpnProfile": {
        "additionalProperties": False,
        "properties": {
            "ethernetSegments": {
                "description": "BGP " "eVPN " "Ethernet " "Segments",
                "items": {"$ref": "#/definitions/bgpEvpn_ethernetSegment"},
                "type": "array",
            },
            "groupId": {"description": "BGP eVPN " "group ID", "type": "string"},
            "ibgpNeighbors": {
                "description": "BGP " "eVPN " "Neighbors",
                "items": {"$ref": "#/definitions/bgpEvpn_bgpNeighbor"},
                "type": "array",
            },
            "id": {"description": "BGP eVPN " "Profile ID", "type": "string"},
            "localAs": {"description": "BGP eVPN " "Local-As", "type": "integer"},
            "name": {"description": "BGP eVPN " "name", "type": "string"},
            "routeReflectServer": {"$ref": "#/definitions/bgpEvpn_bgpNeighbor"},
        },
        "type": "object",
    },
    "bgpEvpn_updateEvpnInstance": {
        "additionalProperties": False,
        "properties": {
            "arpSuppressionEnable": {
                "description": "BGP " "eBVPN " "ARP " "Suppression " "Enable",
                "type": "boolean",
            },
            "id": {"description": "BGP eBVPN " "Instance ID", "type": "string"},
            "macDuplicateExpire": {
                "description": "BGP " "eBVPN " "Instance " "MAC " "duplicate " "expire",
                "type": "string",
            },
            "macDuplicateLimit": {
                "description": "BGP " "eBVPN " "Instance " "MAC " "duplicate " "limit",
                "type": "string",
            },
            "routeTargetDistinguisher": {
                "description": "BGP "
                "eBVPN "
                "Instance "
                "Route "
                "Target "
                "Distinguisher",
                "type": "string",
            },
            "routeTargetExport": {
                "description": "BGP " "eBVPN " "Instance " "Route " "Target " "Export",
                "type": "string",
            },
            "routeTargetImportList": {
                "description": "BGP "
                "eBVPN "
                "Instance "
                "Route "
                "Target "
                "Import "
                "List",
                "items": {"type": "string"},
                "type": "array",
            },
            "vlanId": {
                "description": "BGP eBVPN " "Instance " "VLAN",
                "type": "integer",
            },
            "vni": {"description": "BGP eBVPN " "Instance VNI", "type": "integer"},
        },
        "type": "object",
    },
    "bgpEvpn_updateEvpnInstances": {
        "additionalProperties": False,
        "properties": {
            "evpnInstances": {
                "description": "BGP " "eVPN " "Instances",
                "items": {"$ref": "#/definitions/bgpEvpn_updateEvpnInstance"},
                "type": "array",
            }
        },
        "type": "object",
    },
    "bgpEvpn_vxlanMapping": {
        "additionalProperties": False,
        "properties": {
            "arpSuppressionEnable": {
                "description": "BGP " "eBVPN " "ARP " "Suppression " "Enable",
                "type": "boolean",
            },
            "routeTargetDistinguisher": {
                "description": "BGP " "eBVPN " "Route " "Target " "Distinguisher",
                "type": "string",
            },
            "routeTargetExport": {
                "description": "BGP " "eBVPN " "Route " "Target " "Export",
                "type": "string",
            },
            "routeTargetImportList": {
                "description": "BGP " "eBVPN " "Route " "Target " "Import " "List",
                "items": {"type": "string"},
                "type": "array",
            },
            "status": {"description": "State", "type": "string"},
            "tunnelIp": {"description": "Tunnel IP", "type": "string"},
            "vlan": {"description": "VLAN ID", "type": "integer"},
            "vni": {"description": "VNI", "type": "integer"},
        },
        "type": "object",
    },
    "bgpEvpn_vxlanMappings": {
        "additionalProperties": False,
        "properties": {
            "extra": {"description": "Extra", "type": "object"},
            "firstIndex": {"description": "First index", "type": "integer"},
            "hasMore": {"description": "Has more", "type": "boolean"},
            "list": {
                "items": {"$ref": "#/definitions/bgpEvpn_vxlanMapping"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Raw " "data " "total " "count",
                "type": "integer",
            },
            "totalCount": {"description": "Total count", "type": "integer"},
        },
        "type": "object",
    },
    "breakoutPorts_breakoutPorts": {
        "additionalProperties": False,
        "properties": {
            "ports": {
                "description": "All ports on " "this switch",
                "items": {"$ref": "#/definitions/breakoutPorts_portBreakout"},
                "type": "array",
            }
        },
        "type": "object",
    },
    "breakoutPorts_portBreakout": {
        "additionalProperties": False,
        "properties": {
            "isBreakout": {
                "description": "The flag "
                "is used "
                "to "
                "indicate "
                "whether "
                "the port "
                "is "
                "configured "
                "as a "
                "Breakout "
                "Port",
                "type": "boolean",
            },
            "port": {"description": "Port", "type": "string"},
        },
        "type": "object",
    },
    "breakoutPorts_upsertBreakoutPorts": {
        "additionalProperties": False,
        "properties": {
            "configuredBreakoutPorts": {
                "description": "Switch " "ports " "to " "configure " "Breakout " "Port",
                "items": {"type": "string"},
                "type": "array",
            }
        },
        "type": "object",
    },
    "cliTemplates_cliTemplateCommonVariable": {
        "additionalProperties": False,
        "properties": {
            "domainId": {
                "description": "CliTemplate "
                "Common "
                "Variable "
                "belong "
                "to "
                "domain "
                "ID",
                "type": "string",
            },
            "id": {
                "description": "CliTemplate " "Common " "Variable " "ID",
                "type": "string",
            },
            "name": {
                "description": "CliTemplate " "Common " "Variable " "Name",
                "type": "string",
            },
            "type": {
                "description": "CliTemplate " "Common " "Variable " "Type",
                "type": "string",
            },
            "value": {
                "description": "CliTemplate " "Common " "Variable " "Value",
                "type": "string",
            },
        },
        "type": "object",
    },
    "cliTemplates_cliTemplateCommonVariableQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {"description": "Extra", "type": "object"},
            "firstIndex": {"description": "First " "index", "type": "integer"},
            "hasMore": {"description": "Has " "more", "type": "boolean"},
            "list": {
                "items": {
                    "$ref": "#/definitions/cliTemplates_cliTemplateCommonVariable"
                },
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Raw " "data " "total " "count",
                "type": "integer",
            },
            "totalCount": {"description": "Total " "count", "type": "integer"},
        },
        "type": "object",
    },
    "cliTemplates_cliTemplateConfig": {
        "additionalProperties": False,
        "properties": {
            "cli": {"description": "CliTemplate " "cli", "type": "string"},
            "groupId": {"description": "Switch " "Group " "Id", "type": "string"},
            "id": {"description": "CliTemplate " "Id", "type": "string"},
            "name": {"description": "CliTemplate " "Name", "type": "string"},
            "overwrite": {
                "description": "If "
                "overwrite "
                "flag "
                "set "
                "to "
                "true, "
                "first "
                "time "
                "joined "
                "switch "
                "will "
                "overwrite "
                "by "
                "CLI "
                "config",
                "type": "boolean",
            },
            "pushTime": {
                "description": "CliTemplate " "Config " "Push " "Time",
                "format": "int64",
                "type": "integer",
            },
            "pushTimeType": {
                "description": "CliTemplate " "Config " "Push " "Time " "Type",
                "enum": ["NOW", "SCHEDULE"],
                "type": "string",
            },
            "reload": {
                "description": "If true, "
                "after "
                "switch "
                "applied "
                "CLI "
                "Template "
                "will "
                "reload",
                "type": "boolean",
            },
            "switchList": {
                "items": {"$ref": "#/definitions/cliTemplates_switchResult"},
                "type": "array",
            },
            "switches": {
                "description": "Switch " "list " "for " "CLI " "Template " "used",
                "type": "string",
            },
            "variables": {
                "items": {"$ref": "#/definitions/cliTemplates_variable"},
                "type": "array",
            },
        },
        "type": "object",
    },
    "cliTemplates_cliTemplateConfigListResult": {
        "additionalProperties": False,
        "properties": {
            "groupId": {
                "description": "CliTemplateConfig " "Group " "Id",
                "type": "string",
            },
            "id": {"description": "CliTemplateConfig " "Id", "type": "string"},
            "name": {"description": "CliTemplateConfig " "Name", "type": "string"},
            "pushTime": {
                "description": "CliTemplateConfig " "Push " "Time",
                "format": "int64",
                "type": "integer",
            },
            "switches": {
                "description": "CliTemplateConfig " "Deploy " "Switches",
                "type": "string",
            },
        },
        "type": "object",
    },
    "cliTemplates_cliTemplateModelQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra " "information " "for " "switch " "model " "list",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "switch "
                "model "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "sample "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicates "
                "if "
                "there "
                "are "
                "more "
                "switch "
                "model "
                "after "
                "the "
                "currently "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/cliTemplates_familyResult"},
                "type": "array",
            },
            "rawDataTotalCount": {"description": "List " "count", "type": "integer"},
            "totalCount": {"description": "Total " "list " "count", "type": "integer"},
        },
        "type": "object",
    },
    "cliTemplates_cliTemplateSampleQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra " "information " "for " "sample " "list",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "sample "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "sample "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicates "
                "if "
                "there "
                "are "
                "more "
                "sample "
                "after "
                "the "
                "currently "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/cliTemplates_sampleResult"},
                "type": "array",
            },
            "rawDataTotalCount": {"description": "List " "count", "type": "integer"},
            "totalCount": {"description": "Total " "list " "count", "type": "integer"},
        },
        "type": "object",
    },
    "cliTemplates_cliTemplates": {
        "additionalProperties": False,
        "properties": {
            "cliTemplateConfigId": {
                "description": "CliTemplate " "config " "Id",
                "type": "string",
            },
            "cliTemplateConfigs": {
                "items": {
                    "$ref": "#/definitions/cliTemplates_cliTemplateConfigListResult"
                },
                "type": "array",
            },
            "groupId": {
                "description": "Switch Group " "Id for CLI " "Config used",
                "type": "string",
            },
            "id": {"description": "CliTemplate Id", "type": "string"},
            "overwrite": {
                "description": "If "
                "overwrite "
                "flag set "
                "to true, "
                "first time "
                "joined "
                "switch "
                "will "
                "overwrite "
                "by CLI "
                "config",
                "type": "boolean",
            },
            "searchModels": {
                "description": "Switch " "model " "list " "for CLI " "Config " "used",
                "type": "string",
            },
            "searchName": {"description": "CliTemplate " "Name", "type": "string"},
        },
        "type": "object",
    },
    "cliTemplates_cliTemplatesQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra " "information " "for " "cliTemplate " "list",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "cliTemplate "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "sample "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicates "
                "if "
                "there "
                "are "
                "more "
                "cliTemplate "
                "after "
                "the "
                "currently "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/cliTemplates_cliTemplates"},
                "type": "array",
            },
            "rawDataTotalCount": {"description": "List " "count", "type": "integer"},
            "totalCount": {"description": "Total " "list " "count", "type": "integer"},
        },
        "type": "object",
    },
    "cliTemplates_createCliTemplateCommonVariables": {
        "additionalProperties": False,
        "properties": {
            "variables": {
                "items": {
                    "$ref": "#/definitions/cliTemplates_cliTemplateCommonVariable"
                },
                "type": "array",
            }
        },
        "type": "object",
    },
    "cliTemplates_createProvisionCliTemplate": {
        "additionalProperties": False,
        "properties": {
            "cli": {"description": "CLI " "Config's " "CLI", "type": "string"},
            "groupId": {"description": "Switch " "Group " "Id", "type": "string"},
            "models": {
                "description": "CLI " "Config " "applied " "model",
                "type": "string",
            },
            "name": {"description": "CLI " "Config's " "Name", "type": "string"},
            "overwrite": {
                "description": "If "
                "true, "
                "when "
                "switch "
                "rejoin "
                "SZ "
                "first "
                "time "
                "will "
                "overwrite "
                "with "
                "CLI "
                "Config",
                "type": "boolean",
            },
            "variables": {
                "description": "CLI " "Config's " "variables",
                "type": "string",
            },
        },
        "type": "object",
    },
    "cliTemplates_createUpdateCliTemplate": {
        "additionalProperties": False,
        "properties": {
            "cli": {"description": "CLI " "Template's " "CLI", "type": "string"},
            "cliTemplateId": {
                "description": "CLI " "Template's " "ID",
                "type": "string",
            },
            "groupId": {"description": "Switch " "Group " "Id", "type": "string"},
            "name": {"description": "CLI " "Template's " "Name", "type": "string"},
            "pushTime": {
                "description": "Push " "Time",
                "format": "int64",
                "type": "integer",
            },
            "pushTimeType": {
                "description": "Push " "Time " "Type",
                "enum": ["NOW", "SCHEDULE"],
                "type": "string",
            },
            "reload": {
                "description": "If "
                "true, "
                "after "
                "switch "
                "applied "
                "CLI "
                "Template "
                "will "
                "reload",
                "type": "boolean",
            },
            "switches": {
                "description": "CLI " "Template " "applied " "switches",
                "type": "string",
            },
            "variables": {
                "description": "CLI " "Template's " "variables",
                "type": "string",
            },
        },
        "type": "object",
    },
    "cliTemplates_deleteCliTemplateCommonVariables": {
        "additionalProperties": False,
        "properties": {
            "idList": {
                "description": "CliTemplate "
                "Common "
                "Variable "
                "ID "
                "list "
                "to "
                "delete.",
                "items": {"type": "string"},
                "type": "array",
            }
        },
        "type": "object",
    },
    "cliTemplates_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "cliTemplates_familyResult": {
        "additionalProperties": False,
        "properties": {
            "familyName": {"description": "Switch " "family " "name", "type": "string"},
            "models": {
                "items": {"$ref": "#/definitions/cliTemplates_modelResult"},
                "type": "array",
            },
        },
        "type": "object",
    },
    "cliTemplates_modelResult": {
        "additionalProperties": False,
        "properties": {
            "editable": {
                "description": "If true, " "switch can " "apply CLI " "Config",
                "type": "boolean",
            },
            "model": {"description": "Switch model " "name", "type": "string"},
        },
        "type": "object",
    },
    "cliTemplates_queryCriteriaSuperSet": {
        "allOf": [
            {"$ref": "#/definitions/common_queryCriteria"},
            {
                "properties": {
                    "extraFilters": {
                        "description": '"AND" '
                        "condition "
                        "for "
                        "multiple "
                        "filters",
                        "items": {
                            "additionalProperties": False,
                            "properties": {
                                "type": {
                                    "description": "Filters "
                                    "for "
                                    "specific "
                                    "attribute",
                                    "enum": ["DOMAIN", "SWITCH_GROUP", "cliType"],
                                    "type": "string",
                                },
                                "value": {
                                    "description": "Value " "to " "search",
                                    "type": "string",
                                },
                            },
                            "type": "object",
                        },
                        "type": "array",
                    }
                }
            },
        ]
    },
    "cliTemplates_sampleResult": {
        "additionalProperties": False,
        "properties": {
            "cli": {"description": "Cli sample", "type": "string"},
            "id": {"description": "Cli sample ID", "type": "string"},
            "name": {"description": "Cli sample name", "type": "string"},
            "version": {
                "description": "Cli sample " "version " "number",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "cliTemplates_switchResult": {
        "additionalProperties": False,
        "properties": {
            "switchId": {"description": "Switch Id", "type": "string"},
            "switchName": {"description": "Switch " "Name", "type": "string"},
        },
        "type": "object",
    },
    "cliTemplates_variable": {
        "additionalProperties": False,
        "properties": {
            "name": {"description": "Variable name", "type": "string"},
            "type": {
                "description": "Variable type, only "
                "support STRING, "
                "RANGE and ADDRESS",
                "type": "string",
            },
            "value": {
                "description": "Variable value. If "
                "type equals RANG, "
                "value will be "
                "startValue:endValue, "
                "If type equals "
                "ADDRESS, value "
                "will be "
                "startIp_endIP_subNetMask",
                "type": "string",
            },
        },
        "type": "object",
    },
    "common_bulkCreateResult": {
        "additionalProperties": False,
        "properties": {"idList": {"$ref": "#/definitions/common_idList"}},
        "type": "object",
    },
    "common_bulkDeleteRequest": {
        "additionalProperties": False,
        "properties": {"idList": {"$ref": "#/definitions/common_idList"}},
        "type": "object",
    },
    "common_createResult": {
        "additionalProperties": False,
        "properties": {"id": {"type": "string"}},
        "type": "object",
    },
    "common_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "common_filterOperator": {
        "enum": ["eq", "gt", "lt", "gte", "lte"],
        "type": "string",
    },
    "common_fullTextSearch": {
        "additionalProperties": False,
        "properties": {
            "fields": {
                "description": "Specific fields " "to search",
                "items": {"type": "string"},
                "type": "array",
            },
            "type": {
                "description": "Search logic " "operator",
                "enum": ["AND", "OR"],
                "type": "string",
            },
            "value": {"description": "Text or number to " "search", "type": "string"},
        },
        "type": "object",
    },
    "common_idList": {"items": {"type": "string"}, "type": "array"},
    "common_queryCriteria": {
        "additionalProperties": False,
        "properties": {
            "attributes": {
                "description": "Get specific " "columns only",
                "items": {"type": "string"},
                "type": "array",
            },
            "criteria": {
                "description": "Add backward " "compatibility " "for UI framework",
                "type": "string",
            },
            "expandDomains": {
                "description": "Whether to "
                "expand "
                "domains "
                "into sub "
                "domains/ "
                "zones or "
                "not",
                "type": "boolean",
            },
            "extraFilters": {},
            "extraNotFilters": {},
            "extraTimeRange": {"$ref": "#/definitions/common_timeRange"},
            "filters": {},
            "fullTextSearch": {"$ref": "#/definitions/common_fullTextSearch"},
            "limit": {
                "description": "Size of one page",
                "minimum": 1,
                "type": "integer",
            },
            "options": {},
            "page": {
                "description": "Page number to get",
                "minimum": 1,
                "type": "integer",
            },
            "query": {
                "description": "Add backward " "compatibility for " "UI framework",
                "type": "string",
            },
            "sortInfo": {
                "additionalProperties": False,
                "description": "About sorting",
                "properties": {
                    "dir": {"enum": ["ASC", "DESC"], "type": "string"},
                    "sortColumn": {"type": "string"},
                },
                "type": "object",
            },
        },
        "type": "object",
    },
    "common_queryCriteriaSuperSet": {
        "allOf": [
            {"$ref": "#/definitions/common_queryCriteria"},
            {
                "properties": {
                    "extraFilters": {
                        "description": '"AND" '
                        "condition "
                        "for "
                        "multiple "
                        "filters",
                        "items": {
                            "additionalProperties": False,
                            "properties": {
                                "operator": {
                                    "$ref": "#/definitions/common_filterOperator"
                                },
                                "type": {
                                    "description": "Filters "
                                    "for "
                                    "specific "
                                    "attribute",
                                    "enum": [
                                        "CONTROLBLADE",
                                        "DATABLADE",
                                        "DOMAIN",
                                        "ZONE",
                                        "THIRD_PARTY_ZONE",
                                        "APGROUP",
                                        "WLANGROUP",
                                        "INDOORMAP",
                                        "AP",
                                        "WLAN",
                                        "ProtocolType",
                                        "TIMERANGE",
                                        "RADIOID",
                                        "WLANID",
                                        "CATEGORY",
                                        "CLIENT",
                                        "CP",
                                        "DP",
                                        "CLUSTER",
                                        "NODE",
                                        "BLADE",
                                        "SYNCEDSTATUS",
                                        "OSTYPE",
                                        "APP",
                                        "PORT",
                                        "STATUS",
                                        "REGISTRATIONSTATE",
                                        "GATEWAY",
                                        "APIPADDRESS",
                                        "CLIENTIPADDRESS",
                                        "SEVERITY",
                                        "ACKNOWLEDGED",
                                        "MVNOID",
                                        "USER",
                                        "USERID",
                                        "WLANNAME",
                                        "AUDITIPADDRESS",
                                        "AUDITUSERUUID",
                                        "AUDITOBJECT",
                                        "AUDITACTION",
                                        "AUDITTENANTUUID",
                                        "AUDITOBJECTUUID",
                                        "AUTHTYPE",
                                        "AUDITTYPE",
                                        "H20SuppportEnabled",
                                        "AaaSuppportEnabled",
                                        "GppSuppportEnabled",
                                        "Type",
                                        "RogueMac",
                                        "SSID",
                                        "ALARMSTATE",
                                        "DEVICENAME",
                                        "SWITCH",
                                        "SWITCH_GROUP",
                                        "ZoneAffinityProfileId",
                                        "FIRMWARE_TYPE",
                                        "SCHEDULED_TIME",
                                        "VLAN",
                                        "FAMILY_ID",
                                        "SWITCH_ID",
                                        "transactionId",
                                        "hasLayerThreeConfig",
                                        "clientAuthType",
                                        "clientIpv4Addr",
                                        "clientIpv6Addr",
                                        "clientMac",
                                        "clientUserName",
                                        "switchName",
                                        "ADMIN_STATUS",
                                        "PORT_STATUS",
                                        "POE_ENABLED",
                                        "cliType",
                                        "dispatchStatus",
                                        "configType",
                                        "yang",
                                        "removeYang",
                                        "reservedField1",
                                        "FIRMWARE",
                                        "dot1XIpv4Addr",
                                        "dot1XIpv6Addr",
                                    ],
                                    "type": "string",
                                },
                                "value": {
                                    "description": "Value " "to " "search",
                                    "type": "string",
                                },
                            },
                            "type": "object",
                        },
                        "type": "array",
                    },
                    "extraNotFilters": {
                        "description": '"NOT" '
                        "condition "
                        "for "
                        "multiple "
                        "filters",
                        "items": {
                            "additionalProperties": False,
                            "properties": {
                                "type": {
                                    "description": "Filters "
                                    "for "
                                    "specific "
                                    "attribute",
                                    "enum": [
                                        "CONTROLBLADE",
                                        "DATABLADE",
                                        "DOMAIN",
                                        "ZONE",
                                        "THIRD_PARTY_ZONE",
                                        "APGROUP",
                                        "WLANGROUP",
                                        "INDOORMAP",
                                        "AP",
                                        "WLAN",
                                        "ProtocolType",
                                        "TIMERANGE",
                                        "RADIOID",
                                        "WLANID",
                                        "CATEGORY",
                                        "CLIENT",
                                        "CP",
                                        "DP",
                                        "CLUSTER",
                                        "NODE",
                                        "BLADE",
                                        "SYNCEDSTATUS",
                                        "OSTYPE",
                                        "APP",
                                        "PORT",
                                        "STATUS",
                                        "REGISTRATIONSTATE",
                                        "GATEWAY",
                                        "APIPADDRESS",
                                        "CLIENTIPADDRESS",
                                        "SEVERITY",
                                        "ACKNOWLEDGED",
                                        "MVNOID",
                                        "USER",
                                        "USERID",
                                        "WLANNAME",
                                        "AUDITIPADDRESS",
                                        "AUDITUSERUUID",
                                        "AUDITOBJECT",
                                        "AUDITACTION",
                                        "AUDITTENANTUUID",
                                        "AUDITOBJECTUUID",
                                        "AUTHTYPE",
                                        "AUDITTYPE",
                                        "H20SuppportEnabled",
                                        "AaaSuppportEnabled",
                                        "GppSuppportEnabled",
                                        "Type",
                                        "RogueMac",
                                        "SSID",
                                        "ALARMSTATE",
                                        "DEVICENAME",
                                        "SWITCH",
                                        "ZoneAffinityProfileId",
                                        "FIRMWARE_TYPE",
                                        "SCHEDULED_TIME",
                                        "VLAN",
                                        "FAMILY_ID",
                                        "SWITCH_ID",
                                        "switchStatus.alerts",
                                        "switchStatus.status",
                                        "transactionId",
                                        "hasLayerThreeConfig",
                                        "reservedField1",
                                        "dispatchStatus",
                                        "configType",
                                        "clis",
                                        "yang",
                                        "removeYang",
                                        "clientType",
                                        "aclType",
                                    ],
                                    "type": "string",
                                },
                                "value": {
                                    "description": "Value " "not " "to " "search",
                                    "type": "string",
                                },
                            },
                            "type": "object",
                        },
                        "type": "array",
                    },
                    "filters": {
                        "description": "Filters "
                        "used "
                        "to "
                        "select "
                        "specific "
                        "resource "
                        "scope",
                        "items": {
                            "additionalProperties": False,
                            "properties": {
                                "operator": {
                                    "$ref": "#/definitions/common_filterOperator"
                                },
                                "type": {
                                    "description": "Group " "type",
                                    "enum": [
                                        "SYSTEM",
                                        "CATEGORY",
                                        "CONTROLBLADE",
                                        "DATABLADE",
                                        "DOMAIN",
                                        "ZONE",
                                        "THIRD_PARTY_ZONE",
                                        "APGROUP",
                                        "WLANGROUP",
                                        "INDOORMAP",
                                        "AP",
                                        "WLAN",
                                        "BLADE",
                                        "SYNCEDSTATUS",
                                        "REGISTRATIONSTATE",
                                        "STATUS",
                                        "SWITCH_GROUP",
                                        "FAMILY_ID",
                                        "PORT",
                                        "SWITCH_ID_PORT_IDENTIFIER",
                                        "transactionId",
                                        "dispatchStatus",
                                        "configType",
                                        "yang",
                                        "removeYang",
                                        "switchId",
                                    ],
                                    "type": "string",
                                },
                                "value": {
                                    "description": "Group " "ID",
                                    "type": "string",
                                },
                            },
                            "type": "object",
                        },
                        "type": "array",
                    },
                    "options": {
                        "additionalProperties": False,
                        "description": "Specified " "feature " "required " "informaion",
                        "properties": {
                            "INCLUDE_RBAC_METADATA": {
                                "description": "Whether "
                                "to "
                                "include "
                                "RBAC "
                                "metadata "
                                "or "
                                "not",
                                "type": "boolean",
                            },
                            "TENANT_ID": {
                                "description": "Specify "
                                "Tenant "
                                "ID "
                                "for "
                                "query",
                                "type": "string",
                            },
                            "acct_includeNa": {
                                "description": "Include "
                                "Not "
                                "Available "
                                "acct "
                                "service "
                                "option "
                                "while "
                                "returning "
                                "result",
                                "type": "boolean",
                            },
                            "acct_testableOnly": {
                                "description": "Only "
                                "get "
                                "testable "
                                "service "
                                "type",
                                "type": "boolean",
                            },
                            "acct_type": {
                                "description": "Accounting "
                                "service "
                                "types "
                                "to "
                                "get, "
                                "use "
                                "comma "
                                "to "
                                "separate, "
                                "Ex: "
                                "RADIUS,CGF",
                                "type": "string",
                            },
                            "auth_hostedAaaSupportedEnabled": {
                                "description": "Indicate "
                                "if "
                                "Hosted "
                                "AAA "
                                "Support "
                                "is "
                                "enabled",
                                "type": "boolean",
                            },
                            "auth_includeAdGlobal": {
                                "description": "If "
                                "AD "
                                "is "
                                "in "
                                "list, "
                                "include "
                                "only "
                                "AD "
                                "with "
                                "Global "
                                "Catalog "
                                "configured",
                                "type": "boolean",
                            },
                            "auth_includeGuest": {
                                "description": "Include "
                                "Guest "
                                "auth "
                                "service "
                                "while "
                                "returning "
                                "result",
                                "type": "boolean",
                            },
                            "auth_includeLocalDb": {
                                "description": "Include "
                                "LocalDB "
                                "auth "
                                "service "
                                "while "
                                "returning "
                                "result",
                                "type": "boolean",
                            },
                            "auth_includeNa": {
                                "description": "Include "
                                "Not "
                                "Available "
                                "auth "
                                "service "
                                "option "
                                "while "
                                "returning "
                                "result",
                                "type": "boolean",
                            },
                            "auth_plmnIdentifierEnabled": {
                                "description": "Indicate "
                                "if "
                                "Configure "
                                "PLMN "
                                "identifier "
                                "is "
                                "enabled",
                                "type": "boolean",
                            },
                            "auth_realmType": {
                                "description": "To "
                                "get "
                                "specific "
                                "authentication "
                                "service "
                                "information "
                                "for "
                                "configuring "
                                "realm "
                                "based "
                                "authentication "
                                "profile",
                                "enum": ["ALL", "RADIUS"],
                                "type": "string",
                            },
                            "auth_testableOnly": {
                                "description": "Only "
                                "get "
                                "testable "
                                "service "
                                "type",
                                "type": "boolean",
                            },
                            "auth_type": {
                                "description": "Authentication "
                                "service "
                                "types "
                                "to "
                                "get, "
                                "use "
                                "comma "
                                "to "
                                "separate, "
                                "Ex: "
                                "RADIUS,AD",
                                "type": "string",
                            },
                            "forwarding_type": {
                                "description": "Forwarding "
                                "service "
                                "types "
                                "to "
                                "get, "
                                "use "
                                "comma "
                                "to "
                                "separate, "
                                "Ex: "
                                "L2oGRE,TTGPDG,Bridge,Advanced",
                                "type": "string",
                            },
                            "globalFilterId": {
                                "description": "Specify "
                                "GlobalFilter "
                                "ID "
                                "for "
                                "query",
                                "type": "string",
                            },
                            "inMap": {
                                "description": "Specify "
                                "inMap "
                                "status "
                                "for "
                                "query",
                                "type": "boolean",
                            },
                            "includeSharedResources": {
                                "description": "Whether "
                                "to "
                                "include "
                                "the "
                                "resources "
                                "of "
                                "parent "
                                "domain "
                                "or "
                                "not",
                                "type": "boolean",
                            },
                            "includeUsers": {
                                "description": "Should "
                                "also "
                                "retrieve "
                                "users "
                                "or "
                                "not",
                                "type": "boolean",
                            },
                        },
                        "type": "object",
                    },
                }
            },
        ]
    },
    "common_rbacMetadata": {
        "properties": {
            "rbacMetadata": {
                "items": {"additionalProperties": {"type": "string"}, "properties": {}},
                "type": "array",
            }
        },
        "type": "object",
    },
    "common_timeRange": {
        "additionalProperties": False,
        "properties": {
            "end": {"description": "end time for collecting " "data", "type": "number"},
            "field": {
                "description": "time field for " "collecting data",
                "enum": ["insertionTime", "startTime", "endTime"],
                "type": "string",
            },
            "interval": {"description": "time interval in " "second", "type": "number"},
            "start": {
                "description": "start time for " "collecting data",
                "type": "number",
            },
        },
        "type": "object",
    },
    "configBackup_backupIds": {
        "items": {"description": "Config backup id", "type": "string"},
        "type": "array",
    },
    "configBackup_cfgbk": {
        "additionalProperties": False,
        "properties": {
            "endTimestamp": {
                "description": "the end " "timestamp of " "the config " "backup",
                "format": "int64",
                "type": "integer",
            },
            "failureReason": {
                "description": "Failure "
                "reason of the "
                "config backup "
                "and config "
                "restore",
                "type": "string",
            },
            "id": {
                "description": "the identifier of the " "config backup",
                "type": "string",
            },
            "latestDiffFromMaster": {
                "description": "the "
                "indicator "
                "of the "
                "latest "
                "backup "
                "different "
                "from "
                "the "
                "master "
                "backup",
                "type": "boolean",
            },
            "master": {"description": "the master config " "backup", "type": "boolean"},
            "name": {
                "description": "the name of the config " "backup",
                "type": "string",
            },
            "restoreStatus": {
                "description": "Status of " "config " "restore",
                "type": "string",
            },
            "restoreTimestamp": {
                "description": "the " "timestamp " "of the " "config " "restore",
                "format": "int64",
                "type": "integer",
            },
            "status": {
                "description": "the status of the " "config backup",
                "type": "string",
            },
            "switchName": {
                "description": "Switch Name of " "the config " "backup",
                "type": "string",
            },
            "timestamp": {
                "description": "the start " "timestamp of the " "config backup",
                "format": "int64",
                "type": "integer",
            },
            "type": {"description": "Scheduled or Manual", "type": "string"},
        },
        "type": "object",
    },
    "configBackup_configBackupContent": {
        "additionalProperties": False,
        "properties": {
            "config": {
                "description": "Content " "of the " "ConfigBackup",
                "type": "string",
            },
            "id": {
                "description": "the " "identifier " "of the " "ConfigBackup " "Content",
                "type": "string",
            },
            "name": {
                "description": "Name of " "the " "ConfigBackup " "Content",
                "type": "string",
            },
        },
        "type": "object",
    },
    "configBackup_configBackupDiff": {
        "additionalProperties": False,
        "properties": {
            "configBackup1": {"$ref": "#/definitions/configBackup_configBackupContent"},
            "configBackup2": {"$ref": "#/definitions/configBackup_configBackupContent"},
        },
        "type": "object",
    },
    "configBackup_configBackupDiffInput": {
        "additionalProperties": False,
        "properties": {
            "configBackupId1": {
                "description": "The "
                "first "
                "config "
                "backup "
                "id "
                "of "
                "diff "
                "input",
                "type": "string",
            },
            "configBackupId2": {
                "description": "The "
                "second "
                "config "
                "backup "
                "id "
                "of "
                "diff "
                "input",
                "type": "string",
            },
        },
        "type": "object",
    },
    "configBackup_configBackupInfo": {
        "additionalProperties": False,
        "properties": {
            "configBackupId": {
                "description": "the " "config " "backup " "id",
                "type": "string",
            },
            "errorMessage": {
                "description": "the " "error " "message " "if " "config " "backup",
                "type": "string",
            },
            "switchId": {
                "description": "the " "switch " "id of " "config " "backup",
                "type": "string",
            },
        },
        "type": "object",
    },
    "configBackup_createBackupResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {"$ref": "#/definitions/common_rbacMetadata"},
            "firstIndex": {
                "description": "Index " "of " "first " "index " "in " "current " "page",
                "type": "integer",
            },
            "hasMore": {
                "description": "Has " "more " "data " "or " "not",
                "type": "boolean",
            },
            "list": {
                "items": {
                    "additionalProperties": False,
                    "properties": {
                        "configBackupId": {
                            "description": "Identifier " "of " "config " "backup",
                            "type": "string",
                        },
                        "errorMessage": {
                            "description": "Error " "message",
                            "type": "string",
                        },
                        "switchId": {
                            "description": "Identifier " "of " "switch",
                            "type": "string",
                        },
                    },
                    "type": "object",
                },
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "ConfigBackupInfo " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Current " "ConfigBackupInfo " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "configBackup_goldenAlertItem": {
        "additionalProperties": False,
        "properties": {
            "switchGroupName": {
                "description": "switch's " "group " "name",
                "type": "string",
            },
            "switchId": {"description": "switch " "ID", "type": "string"},
            "switchName": {"description": "switch's " "name", "type": "string"},
        },
        "type": "object",
    },
    "configBackup_goldenBackupAlert": {
        "additionalProperties": False,
        "properties": {
            "extra": {"$ref": "#/definitions/common_rbacMetadata"},
            "firstIndex": {
                "description": "Index " "of " "first " "index " "in " "current " "page",
                "type": "integer",
            },
            "hasMore": {
                "description": "Has " "more " "data or " "not",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/configBackup_goldenAlertItem"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "ConfigBackupInfo " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Current " "ConfigBackupInfo " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "configBackup_goldenConfigBackupDiff": {
        "additionalProperties": False,
        "properties": {
            "configBackup1": {"$ref": "#/definitions/configBackup_configBackupContent"},
            "configBackup2": {"$ref": "#/definitions/configBackup_configBackupContent"},
            "masterBackupId": {
                "description": "master " "backup " "ID",
                "type": "string",
            },
        },
        "type": "object",
    },
    "configBackup_goldenRequest": {
        "items": {"$ref": "#/definitions/configBackup_goldenRequestItem"},
        "type": "array",
    },
    "configBackup_goldenRequestItem": {
        "additionalProperties": False,
        "properties": {
            "backupId": {"description": "backup " "ID", "type": "string"},
            "switchId": {"description": "switch " "ID", "type": "string"},
        },
        "type": "object",
    },
    "configBackup_list": {
        "additionalProperties": False,
        "properties": {
            "extra": {"$ref": "#/definitions/common_rbacMetadata"},
            "firstIndex": {
                "description": "Index of the "
                "first "
                "ConfigBackup "
                "returned out of "
                "the complete "
                "ConfigBackup list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator of whether "
                "there are more "
                "ConfigBackup after "
                "the current "
                "displayed list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/configBackup_cfgbk"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "ConfigBackup " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "ConfigBackup " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "configBackup_stringResult": {"type": "string"},
    "configBackup_switchIdNamePair": {
        "additionalProperties": False,
        "properties": {
            "switchId": {
                "description": "the " "switch " "id of " "config " "backup",
                "type": "string",
            },
            "switchName": {
                "description": "the " "switch " "name " "of " "config " "backup",
                "type": "string",
            },
        },
        "type": "object",
    },
    "configBackup_switchIds": {
        "items": {"description": "Switch id", "type": "string"},
        "type": "array",
    },
    "deployLogItem_ConfigurationHistoryDetailQueryResult": {
        "additionalProperties": False,
        "properties": {
            "firstIndex": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "configs "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "configs "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "configs "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "items": {"$ref": "#/definitions/deployLogItem_deployLogItem"},
                "type": "array",
            },
            "totalCount": {
                "description": "Total " "records " "count " "in " "this " "response",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "deployLogItem_createDeployLogItem": {
        "items": {"$ref": "#/definitions/deployLogItem_deployLogItem"},
        "type": "array",
    },
    "deployLogItem_deployLogItem": {
        "additionalProperties": False,
        "properties": {
            "clis": {"description": "CLI Command", "type": "string"},
            "configFeature": {
                "description": "Config " "Feature",
                "enum": ["VLAN", "ACL", "STATIC_ROUTE"],
                "type": "string",
            },
            "configType": {
                "description": "Config " "Type",
                "enum": [
                    "PROVISIONING",
                    "GLOBAL",
                    "AAA_SETTING",
                    "AAA_SERVER",
                    "COMMON",
                    "MODEL",
                    "SWITCH_SETTINGS",
                    "COPY_CONFIGS",
                    "LAG_SETTINGS",
                    "VE_PORTS",
                    "LOCAL_SYNC",
                    "PORT_CONFIGURATION",
                    "OVERWRITE_CONFIGURATION",
                    "STACK",
                    "SYSLOG_SERVER_CONFIGS",
                    "SNMPV3_CONFIGURATION",
                    "DNS_SERVER",
                    "SYSLOG_SERVER",
                    "MSP_CONFIGURATION",
                    "SWITCH_GROUP_CONFIGS",
                    "PRE_DELETE_CONFIGS",
                    "GEO_REDUNDANCY",
                    "SWITCH_OVER",
                    "CLI_PROVISIONING",
                    "CLI_UPDATE",
                    "CLEAN",
                    "ALL_CONFIG",
                    "COMPLEMENT",
                    "PORT_TEMPLATE",
                    "VXLAN",
                    "WEB_AUTHENTICATION",
                    "AUTHENTICATION",
                    "FLEXIBLE_AUTHENTICATION_PROFILE",
                ],
                "type": "string",
            },
            "dispatchError": {
                "description": "Error " "of " "Deployment",
                "type": "string",
            },
            "dispatchFailedReason": {
                "description": "Deployment " "Fail " "Description",
                "items": {"$ref": "#/definitions/deployLogItem_dispatchFailedReason"},
                "type": "array",
            },
            "dispatchStatus": {
                "description": "Status " "of " "Deployment",
                "enum": [
                    "PENDING",
                    "IN_PROGRESS",
                    "SUCCESS",
                    "FAILED",
                    "PENDING_LOCAL_SYNC",
                    "FAILED_NO_RESPONSE",
                    "MERGED",
                    "FAILED_SAVE_FLASH",
                    "NO_CONFIG_CHANGE",
                    "OFFLINE",
                    "ROAMED",
                    "APPLIED",
                ],
                "type": "string",
            },
            "endTime": {
                "description": "Deployment " "end " "datetime",
                "format": "int64",
                "type": "integer",
            },
            "groupId": {"type": "string"},
            "id": {
                "description": "Switch " "Deployment " "History Id",
                "type": "string",
            },
            "nodeId": {"type": "string"},
            "removeYang": {
                "description": "Removed " "Yang " "Template",
                "type": "string",
            },
            "reservedField1": {"type": "string"},
            "serialNumber": {
                "description": "Serical " "Number " "of " "Switch",
                "type": "string",
            },
            "startTime": {
                "description": "Deployment " "begin " "datetime",
                "format": "int64",
                "type": "integer",
            },
            "switchId": {"description": "Switch Id", "type": "string"},
            "switchName": {"description": "Switch " "Name", "type": "string"},
            "transactionId": {
                "description": "Transaction " "Id " "of " "depolyment",
                "type": "string",
            },
            "updateUser": {"type": "string"},
            "yang": {"description": "Yang Template", "type": "string"},
        },
        "type": "object",
    },
    "deployLogItem_dispatchFailedReason": {
        "additionalProperties": False,
        "properties": {
            "lineNumber": {
                "description": "Line " "Number " "Fail " "to " "Execute " "Cmd",
                "type": "string",
                "x-isnullable": True,
            },
            "message": {
                "description": "Deployment " "Fail " "Message",
                "type": "string",
                "x-isnullable": True,
            },
            "status": {
                "description": "Deployment " "Fail " "Status",
                "type": "string",
                "x-isnullable": True,
            },
        },
        "type": "object",
    },
    "deployLogItem_stringResult": {"type": "string"},
    "deployLog_ConfigurationHistoryQueryResult": {
        "additionalProperties": False,
        "properties": {
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "config "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "configs "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "description": "The " "list " "of " "configs " "in " "this " "response",
                "items": {"$ref": "#/definitions/deployLog_deployLog"},
                "type": "array",
            },
            "totalCount": {
                "description": "Total " "records " "count " "in " "this " "response",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "deployLog_createDeployLog": {
        "items": {"$ref": "#/definitions/deployLog_deployLog"},
        "type": "array",
    },
    "deployLog_deployLog": {
        "additionalProperties": False,
        "properties": {
            "configFeature": {
                "description": "Config " "Feature",
                "enum": ["VLAN", "ACL", "STATIC_ROUTE"],
                "type": "string",
            },
            "configType": {
                "description": "Config Type",
                "enum": [
                    "PROVISIONING",
                    "GLOBAL",
                    "AAA_SETTING",
                    "AAA_SERVER",
                    "COMMON",
                    "MODEL",
                    "SWITCH_SETTINGS",
                    "COPY_CONFIGS",
                    "LAG_SETTINGS",
                    "VE_PORTS",
                    "LOCAL_SYNC",
                    "PORT_CONFIGURATION",
                    "OVERWRITE_CONFIGURATION",
                    "STACK",
                    "SYSLOG_SERVER_CONFIGS",
                    "SNMPV3_CONFIGURATION",
                    "DNS_SERVER",
                    "SYSLOG_SERVER",
                    "MSP_CONFIGURATION",
                    "SWITCH_GROUP_CONFIGS",
                    "PRE_DELETE_CONFIGS",
                    "GEO_REDUNDANCY",
                    "SWITCH_OVER",
                    "CLI_PROVISIONING",
                    "CLI_UPDATE",
                    "CLEAN",
                    "ALL_CONFIG",
                    "COMPLEMENT",
                    "PORT_TEMPLATE",
                    "VXLAN",
                    "WEB_AUTHENTICATION",
                    "AUTHENTICATION",
                    "FLEXIBLE_AUTHENTICATION_PROFILE",
                ],
                "type": "string",
            },
            "deployScope": {
                "description": "Deploy Scope",
                "enum": [
                    "PRE_PROVISION",
                    "PROVISION",
                    "GROUP",
                    "PORT",
                    "SWITCH",
                    "COPY",
                    "OVERWRITE",
                    "SNMPV3",
                ],
                "type": "string",
            },
            "deployStatus": {
                "description": "Deploy Status",
                "enum": [
                    "PENDING",
                    "STARTED",
                    "SUCCESS",
                    "FAILURE",
                    "PENDING_PRE_PROVISION",
                    "PENDING_LOCAL_SYNC",
                    "APPLIED",
                ],
                "type": "string",
            },
            "endTime": {
                "description": "Deploy End Time",
                "format": "int64",
                "type": "integer",
            },
            "groupId": {"description": "Switch Group ID", "type": "string"},
            "id": {"description": "ID", "type": "string"},
            "modelFamily": {"description": "Switch Model " "Family", "type": "string"},
            "nodeId": {"type": "string"},
            "nodeName": {"type": "string"},
            "reservedField1": {"type": "string"},
            "scheduled": {
                "description": "Schedule",
                "format": "int64",
                "type": "integer",
            },
            "startTime": {
                "description": "Deploy Start " "Time",
                "format": "int64",
                "type": "integer",
            },
            "summary": {"$ref": "#/definitions/deployLog_deployLogStatusSummary"},
            "switchIds": {"description": "Switch ID", "type": "string"},
            "transactionId": {
                "description": "Deploy " "Transaction " "ID",
                "type": "string",
            },
            "updateUser": {"type": "string"},
            "yang": {"description": "YANG Model", "type": "string"},
        },
        "type": "object",
    },
    "deployLog_deployLogStatusSummary": {
        "additionalProperties": False,
        "properties": {
            "applied": {
                "description": "Deployment " "Applied " "Counter",
                "type": "integer",
            },
            "failed": {
                "description": "Deployment " "Fail " "Counter",
                "type": "integer",
            },
            "failedNoResponse": {
                "description": "Deployment " "Fail " "No " "Response " "Counter",
                "type": "integer",
            },
            "failedSaveFlash": {
                "description": "Deployment " "Fail " "to " "Save " "Flash",
                "type": "integer",
            },
            "success": {
                "description": "Deployment " "Success " "Counter",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "deployLog_stringResult": {"type": "string"},
    "dnsConfig_createDnsConfig": {
        "additionalProperties": False,
        "properties": {
            "dns": {"$ref": "#/definitions/dnsConfig_dnsConfigObject"},
            "id": {"description": "Switch Group Id", "type": "string"},
        },
        "type": "object",
    },
    "dnsConfig_dnsConfig": {
        "additionalProperties": False,
        "properties": {
            "createdTime": {
                "description": "The create " "time of the " "DNS Config",
                "type": "integer",
            },
            "dns": {"$ref": "#/definitions/dnsConfig_dnsConfigObject"},
            "updatedTime": {
                "description": "The modify " "time of the " "DNS Config",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "dnsConfig_dnsConfigObject": {
        "additionalProperties": False,
        "properties": {"ip": {"description": "DNS Config IP", "type": "string"}},
        "type": "object",
    },
    "dnsConfig_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "dnsConfig_updateDnsConfig": {
        "additionalProperties": False,
        "properties": {"dns": {"$ref": "#/definitions/dnsConfig_dnsConfigObject"}},
        "type": "object",
    },
    "eventConfig_eventConfig": {
        "additionalProperties": False,
        "properties": {
            "criteria": {
                "description": "Threshold of " "each Switch " "custom event " "config",
                "type": "integer",
            },
            "description": {
                "description": "Description "
                "of each "
                "Switch "
                "custom "
                "event "
                "config",
                "type": "string",
            },
            "id": {"description": "Identifier of event " "config", "type": "integer"},
            "name": {
                "description": "Name of each " "Switch custom " "event config",
                "type": "string",
            },
            "severity": {
                "description": "Severity of " "each Switch " "custom event " "config",
                "enum": ["Warning", "Major", "Critical"],
                "type": "string",
            },
            "textPattern": {
                "description": "User "
                "defined "
                "text "
                "pattern of "
                "each "
                "Switch "
                "custom "
                "event "
                "config",
                "type": "string",
            },
            "timeWindow": {
                "description": "Detection "
                "time "
                "woindow of "
                "each Switch "
                "custom "
                "event "
                "config",
                "enum": [60, 120, 240, 480, 720, 1440, 2880],
                "type": "integer",
            },
            "type": {
                "description": "Type of each " "Switch custom " "event config",
                "enum": ["CPU", "Memory", "TextPattern"],
                "type": "string",
            },
        },
        "type": "object",
    },
    "eventConfig_getEventConfigList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra "
                "information "
                "of "
                "responsed "
                "Switch "
                "custom "
                "event "
                "config "
                "list",
                "type": "object",
            },
            "firstIndex": {
                "description": "First "
                "index "
                "of "
                "responsed "
                "Switch "
                "custom "
                "event "
                "config "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "Switch "
                "event "
                "config",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/eventConfig_eventConfig"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "List "
                "of "
                "responsed "
                "Switch "
                "custom "
                "event "
                "config",
                "type": "integer",
            },
            "totalCount": {
                "description": "Count "
                "of  "
                "responsed "
                "Switch "
                "custom "
                "event "
                "config",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "eventConfig_modifyEventConfig": {
        "additionalProperties": False,
        "properties": {
            "criteria": {
                "description": "Threshold "
                "of each "
                "Switch "
                "custom "
                "event "
                "config",
                "type": "integer",
            },
            "description": {
                "description": "Description "
                "of "
                "each "
                "Switch "
                "custom "
                "event "
                "config",
                "type": "string",
            },
            "name": {
                "description": "Name of " "each Switch " "custom " "event " "config",
                "type": "string",
            },
            "severity": {
                "description": "Severity "
                "of each "
                "Switch "
                "custom "
                "event "
                "config",
                "enum": ["Warning", "Major", "Critical"],
                "type": "string",
            },
            "textPattern": {
                "description": "User "
                "defined "
                "text "
                "pattern "
                "of "
                "each "
                "Switch "
                "custom "
                "event "
                "config",
                "type": "string",
            },
            "timeWindow": {
                "description": "Detection "
                "time "
                "woindow "
                "of "
                "each "
                "Switch "
                "custom "
                "event "
                "config",
                "enum": [60, 120, 240, 480, 720, 1440, 2880],
                "type": "integer",
            },
            "type": {
                "description": "Type of " "each Switch " "custom " "event " "config",
                "enum": ["CPU", "Memory", "TextPattern"],
                "type": "string",
            },
        },
        "type": "object",
    },
    "eventConfig_queryResponse": {
        "additionalProperties": False,
        "properties": {
            "data": {
                "description": "Response data " "message of " "Public API",
                "type": "object",
            },
            "error": {
                "description": "Response error " "message of " "Public API",
                "type": "object",
            },
            "extra": {
                "description": "Extra " "information of " "Public API " "response",
                "type": "object",
            },
            "metaData": {
                "description": "Meta-data " "of Public " "API " "response",
                "type": "object",
            },
            "success": {
                "description": "Response " "success " "message of " "Public API",
                "type": "boolean",
            },
        },
        "type": "object",
    },
    "eventManagement_eventDataList": {
        "additionalProperties": False,
        "properties": {
            "hasMore": {"type": "boolean"},
            "list": {
                "items": {"$ref": "#/definitions/eventManagement_singleEventSetting"},
                "type": "array",
            },
            "rawDataTotalCount": {"type": "integer"},
            "totalCount": {"type": "integer"},
        },
        "type": "object",
    },
    "eventManagement_eventDataResponse": {
        "additionalProperties": False,
        "properties": {
            "data": {"$ref": "#/definitions/eventManagement_eventDataList"},
            "error": {
                "description": "The " "error " "message " "of " "http " "request",
                "type": "string",
            },
            "extra": {
                "description": "Extra "
                "information "
                "for "
                "event "
                "management "
                "setting",
                "type": "string",
            },
            "success": {
                "description": "The " "status " "of " "http " "request",
                "type": "boolean",
            },
        },
        "type": "object",
    },
    "eventManagement_eventEmailSetting": {
        "additionalProperties": False,
        "properties": {
            "emailEnabled": {
                "description": "Enable/Disable " "Email " "sending " "function",
                "type": "boolean",
            },
            "mailTo": {"description": "E-mail " "recipients", "type": "string"},
        },
        "type": "object",
    },
    "eventManagement_eventSettingList": {
        "additionalProperties": False,
        "items": {"$ref": "#/definitions/eventManagement_singleEventSetting"},
        "type": "array",
    },
    "eventManagement_singleEventSetting": {
        "additionalProperties": False,
        "properties": {
            "category": {"description": "Event " "category", "type": "string"},
            "configPageDesc": {"description": "Event " "description", "type": "string"},
            "eventCode": {"description": "Event " "code", "type": "integer"},
            "severity": {"description": "Event " "severity", "type": "string"},
            "switchGroupOverride": {
                "description": "Enable/Disable "
                "override "
                "event "
                "system "
                "settings "
                "by "
                "switch "
                "group "
                "level",
                "type": "boolean",
            },
            "triggerEmail": {
                "description": "Enable/Disable "
                "Email "
                "sending "
                "for "
                "this "
                "event",
                "type": "boolean",
            },
            "type": {"description": "Event " "type", "type": "string"},
        },
        "type": "object",
    },
    "firmware_firmwaresQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra " "information " "for " "Firmware " "list",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "firmware "
                "list "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "Firmware "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "Firmwares "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/firmware_switchFirmware"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Firmware " "list " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "Firmware " "list " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "firmware_scheduleIds": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra information " "for Schedule Ids " "list",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index of the "
                "first Schedule "
                "Ids returned "
                "out of the "
                "complete "
                "ConfigBackup "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator of "
                "whether there are "
                "more Schedule Ids "
                "after the current "
                "displayed list",
                "type": "boolean",
            },
            "list": {"items": {"type": "string"}, "type": "array"},
            "rawDataTotalCount": {
                "description": "Firmware " "list " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total Schedule " "Ids count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "firmware_switchFirmware": {
        "additionalProperties": False,
        "properties": {
            "switchModels": {
                "items": {"$ref": "#/definitions/firmware_switchModel"},
                "type": "array",
            },
            "version": {
                "description": "Firmware " "version of the " "Switch",
                "type": "string",
            },
        },
        "type": "object",
    },
    "firmware_switchModel": {
        "additionalProperties": False,
        "properties": {
            "imageFileNames": {
                "description": "Name of " "the Switch " "Image File",
                "items": {"type": "string"},
                "type": "array",
            },
            "name": {"description": "Name of the Switch " "Model", "type": "string"},
        },
        "type": "object",
    },
    "flexibleAuthenticationProfile_CreateFlexibleAuthenticationProfile": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "Alto " "ID", "type": "string"},
            "authDefaultVlan": {
                "description": "Authentication " "default " "VLAN",
                "type": "integer",
                "x-isnullable": True,
            },
            "authFailAction": {
                "description": "Authentication " "fail " "action",
                "type": "string",
            },
            "authTimeoutAction": {
                "description": "Authentication " "timeout " "action",
                "type": "string",
            },
            "authenticationType": {
                "description": "Authentication " "type",
                "type": "string",
            },
            "changeAuthOrder": {
                "description": "Change " "authentication " "order",
                "type": "boolean",
            },
            "criticalVlan": {
                "description": "Critical " "VLAN",
                "type": "integer",
                "x-isnullable": True,
            },
            "dot1XPortControl": {
                "description": "Dot " "1X " "port " "control",
                "type": "string",
                "x-isnullable": True,
            },
            "groupId": {"description": "Group " "ID", "type": "string"},
            "id": {"description": "ID", "type": "string"},
            "profileName": {"description": "Profile " "name", "type": "string"},
            "restrictedVlan": {
                "description": "Restricted " "VLAN",
                "type": "integer",
                "x-isnullable": True,
            },
        },
        "type": "object",
    },
    "flexibleAuthenticationProfile_FlexibleAuthenticationProfile": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "Alto " "ID", "type": "string"},
            "authDefaultVlan": {
                "description": "Authentication " "default " "VLAN",
                "type": "integer",
                "x-isnullable": True,
            },
            "authFailAction": {
                "description": "Authentication " "fail " "action",
                "type": "string",
            },
            "authTimeoutAction": {
                "description": "Authentication " "timeout " "action",
                "type": "string",
            },
            "authenticationType": {
                "description": "Authentication " "type",
                "type": "string",
            },
            "changeAuthOrder": {
                "description": "Change " "authentication " "order",
                "type": "boolean",
            },
            "createdTime": {"description": "Created " "time", "type": "integer"},
            "criticalVlan": {
                "description": "Critical " "VLAN",
                "type": "integer",
                "x-isnullable": True,
            },
            "dot1XPortControl": {
                "description": "Dot " "1X " "port " "control",
                "type": "string",
                "x-isnullable": True,
            },
            "groupId": {"description": "Group " "ID", "type": "string"},
            "id": {"description": "ID", "type": "string"},
            "profileName": {"description": "Profile " "name", "type": "string"},
            "restrictedVlan": {
                "description": "Restricted " "VLAN",
                "type": "integer",
                "x-isnullable": True,
            },
            "updatedTime": {"description": "Updated " "time", "type": "integer"},
        },
        "type": "object",
    },
    "flexibleAuthenticationProfile_FlexibleAuthenticationProfileQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {"description": "Extra", "type": "object"},
            "firstIndex": {"description": "First " "index", "type": "integer"},
            "hasMore": {"description": "Has " "more", "type": "boolean"},
            "list": {
                "items": {
                    "$ref": "#/definitions/flexibleAuthenticationProfile_FlexibleAuthenticationProfile"
                },
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Raw " "data " "total " "count",
                "type": "integer",
            },
            "totalCount": {"description": "Total " "count", "type": "integer"},
        },
        "type": "object",
    },
    "flexibleAuthenticationProfile_UpdateFlexibleAuthenticationProfile": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "Alto " "ID", "type": "string"},
            "authDefaultVlan": {
                "description": "Authentication " "default " "VLAN",
                "type": "integer",
                "x-isnullable": True,
            },
            "authFailAction": {
                "description": "Authentication " "fail " "action",
                "type": "string",
            },
            "authTimeoutAction": {
                "description": "Authentication " "timeout " "action",
                "type": "string",
            },
            "authenticationType": {
                "description": "Authentication " "type",
                "type": "string",
            },
            "changeAuthOrder": {
                "description": "Change " "authentication " "order",
                "type": "boolean",
            },
            "criticalVlan": {
                "description": "Critical " "VLAN",
                "type": "integer",
                "x-isnullable": True,
            },
            "dot1XPortControl": {
                "description": "Dot " "1X " "port " "control",
                "type": "string",
                "x-isnullable": True,
            },
            "groupId": {"description": "Group " "ID", "type": "string"},
            "profileName": {"description": "Profile " "name", "type": "string"},
            "restrictedVlan": {
                "description": "Restricted " "VLAN",
                "type": "integer",
                "x-isnullable": True,
            },
        },
        "type": "object",
    },
    "flexibleAuthenticationProfile_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "groupModelConfig_groupConfigAuditId": {
        "additionalProperties": False,
        "properties": {
            "id": {
                "description": "The "
                "identifier "
                "of the "
                "Group "
                "Model "
                "Config",
                "type": "string",
            },
            "name": {
                "description": "The " "name " "of " "the " "Group " "Model " "Config",
                "type": "string",
            },
        },
        "type": "object",
    },
    "groupModelConfig_groupModelConfig": {
        "additionalProperties": False,
        "properties": {
            "createdTime": {
                "description": "The "
                "create "
                "time "
                "of "
                "the "
                "Group "
                "Model "
                "Config",
                "format": "int64",
                "type": "integer",
            },
            "familyId": {"description": "Family " "Id", "type": "string"},
            "groupId": {"description": "Group " "Id", "type": "string"},
            "hasAclConfig": {
                "description": "Indicates "
                "if "
                "there "
                "is "
                "any "
                "ACLConfig "
                "in "
                "the "
                "Group "
                "Model "
                "Config",
                "type": "boolean",
            },
            "hasConfigured": {
                "description": "Indicates "
                "if "
                "there "
                "is "
                "any "
                "config "
                "in "
                "the "
                "Group "
                "Model "
                "Config",
                "type": "boolean",
            },
            "hasSelected": {
                "description": "Indicates "
                "if "
                "this "
                "Group "
                "Model "
                "Config "
                "has "
                "been "
                "selected",
                "type": "boolean",
            },
            "hasStaticRouteConfig": {
                "description": "Indicates "
                "if "
                "there "
                "is "
                "any "
                "StaticRoute "
                "in "
                "the "
                "Group "
                "Model "
                "Config",
                "type": "boolean",
            },
            "hasVlanConfig": {
                "description": "Indicates "
                "if "
                "there "
                "is "
                "any "
                "VlanConfig "
                "in "
                "the "
                "Group "
                "Model "
                "Config",
                "type": "boolean",
            },
            "id": {"description": "Id", "type": "string"},
            "updatedTime": {
                "description": "The "
                "update "
                "time "
                "of "
                "the "
                "Group "
                "Model "
                "Config",
                "format": "int64",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "groupModelConfig_groupModelConfigQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "Group "
                "Model "
                "Config "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "Group "
                "Model "
                "Configs "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "Group "
                "Model "
                "Configs "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/groupModelConfig_groupModelConfig"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "Group " "Model " "Configs " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total "
                "Group "
                "Model "
                "Configs "
                "count "
                "in "
                "this "
                "response",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "groupModelConfig_selectedIds": {
        "additionalProperties": False,
        "properties": {
            "selectedIdList": {"items": {"type": "string"}, "type": "array"}
        },
        "type": "object",
    },
    "groupModelConfig_updateGroupConfigResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "updated "
                "Group "
                "Model "
                "Config "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "Group "
                "Model "
                "Configs "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "updated "
                "Group "
                "Model "
                "Configs "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/groupModelConfig_groupConfigAuditId"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "updated " "Group " "Model " "Configs " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total "
                "updated "
                "Group "
                "Model "
                "Configs "
                "count "
                "in "
                "this "
                "response",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "group_auditId": {
        "additionalProperties": False,
        "properties": {
            "id": {"description": "Audit Id", "type": "string"},
            "name": {"description": "Audit name", "type": "string"},
        },
        "type": "object",
    },
    "group_auditIdList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra information for " "audit id list",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index of the "
                "first audit id "
                "returned out of "
                "the complete "
                "audit id list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicates if there "
                "are more audit id "
                "after the currently "
                "displayed list",
                "type": "boolean",
            },
            "list": {"items": {"$ref": "#/definitions/group_auditId"}, "type": "array"},
            "rawDataTotalCount": {
                "description": "Audit Id " "count",
                "type": "integer",
            },
            "totalCount": {"description": "Total Audit Id " "count", "type": "integer"},
        },
        "type": "object",
    },
    "group_clientObjectID": {
        "additionalProperties": False,
        "properties": {
            "extraValues": {
                "description": "Extra values " "of the client",
                "type": "object",
            },
            "id": {"description": "Identifier of the " "client", "type": "string"},
            "label": {"description": "Label of the client", "type": "string"},
            "type": {"description": "Type of the client", "type": "string"},
        },
        "type": "object",
    },
    "group_cloneConfigByGroup": {
        "additionalProperties": False,
        "properties": {
            "destination": {"items": {"type": "string"}, "type": "array"},
            "source": {"description": "Source", "type": "string"},
        },
        "type": "object",
    },
    "group_cloneConfigBySwitch": {
        "additionalProperties": False,
        "properties": {
            "config": {"description": "Config", "type": "string"},
            "destination": {"items": {"type": "string"}, "type": "array"},
            "source": {"description": "Source", "type": "string"},
        },
        "type": "object",
    },
    "group_errorObject": {
        "additionalProperties": False,
        "properties": {
            "list": {"items": {"type": "string"}, "type": "array"},
            "message": {"type": "string"},
            "msgKey": {"type": "string"},
        },
        "type": "object",
    },
    "group_getConfigBySwitch": {
        "additionalProperties": False,
        "properties": {
            "id": {"description": "ID", "type": "string"},
            "source": {"description": "Source", "type": "string"},
        },
        "type": "object",
    },
    "group_groupConfigBackupSchedule": {
        "additionalProperties": False,
        "properties": {
            "dateOfMonth": {
                "description": "The "
                "date "
                "of "
                "the "
                "switch "
                "group "
                "backup "
                "schedule",
                "type": "integer",
            },
            "dayOfWeek": {
                "description": "The "
                "day "
                "of "
                "week "
                "of "
                "the "
                "switch "
                "group "
                "backup "
                "schedule",
                "enum": [
                    "SUNDAY",
                    "MONDAY",
                    "TUESDAY",
                    "WEDNESDAY",
                    "THURSDAY",
                    "FRIDAY",
                    "SATURDAY",
                ],
                "type": "string",
            },
            "hour": {
                "description": "The hour "
                "of the "
                "switch "
                "group "
                "backup "
                "schedule",
                "type": "integer",
            },
            "id": {
                "description": "Identifier "
                "of the "
                "switch "
                "group "
                "backup "
                "schedule",
                "type": "string",
            },
            "interval": {
                "description": "Interval "
                "of "
                "the "
                "switch "
                "group "
                "backup "
                "schedule",
                "enum": ["MONTHLY", "WEEKLY", "DAILY"],
                "type": "string",
            },
            "minute": {
                "description": "The "
                "minute "
                "of the "
                "switch "
                "group "
                "backup "
                "schedule",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "group_groupsByIdsQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "data": {"$ref": "#/definitions/group_queryResultList"},
            "error": {"$ref": "#/definitions/group_errorObject"},
            "extra": {"description": "Any " "additional " "response", "type": "object"},
            "metaData": {
                "description": "Metadata " "of " "query " "result " "list",
                "type": "object",
            },
            "success": {
                "description": "Query " "result " "success " "or " "not",
                "type": "boolean",
            },
        },
        "type": "object",
    },
    "group_queryResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra information " "for query result " "list",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index of the "
                "first query "
                "result "
                "returned out "
                "of the "
                "complete "
                "query result "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicates if "
                "there are more "
                "query result "
                "after the "
                "currently "
                "displayed list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/group_clientObjectID"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Query " "result " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total query " "result count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "group_switchGroup": {
        "additionalProperties": False,
        "properties": {
            "createDatetime": {
                "description": "Create " "datetime of " "the switch " "group",
                "format": "int64",
                "type": "integer",
            },
            "creatorId": {
                "description": "Creator Id of the " "switch group",
                "type": "string",
            },
            "description": {
                "description": "Description of " "the switch group",
                "type": "string",
            },
            "domainId": {
                "description": "Identifier of the "
                "management domain "
                "to which the switch "
                "group belong",
                "type": "string",
            },
            "enableStrongCert": {
                "description": "Enable " "SSH/TLS key " "enhance " "mode",
                "type": "boolean",
            },
            "enableTwoFactor": {
                "description": "Enable two "
                "factor "
                "authentication. "
                "Only support "
                "FIPS mode",
                "type": "boolean",
            },
            "firmware": {
                "description": "Firmware of the " "switch group",
                "type": "string",
            },
            "id": {
                "description": "Identifier of the switch " "group",
                "type": "string",
            },
            "levelOne": {
                "description": "Level one  of the " "switch group",
                "type": "boolean",
            },
            "levelTwo": {
                "description": "Level two of the " "switch group",
                "type": "boolean",
            },
            "name": {"description": "Name of the switch " "group", "type": "string"},
            "sampledInstant": {
                "description": "Sampled " "instant of " "the switch " "group",
                "type": "object",
            },
            "schedule": {"$ref": "#/definitions/group_groupConfigBackupSchedule"},
            "switchGroupLevelOneId": {
                "description": "Level " "one Id " "of the " "switch " "group",
                "type": "string",
            },
            "switchGroupLevelTwoId": {
                "description": "Level " "two Id " "of the " "switch " "group",
                "type": "string",
            },
            "tenantId": {
                "description": "Tenant Id of the " "switch group",
                "type": "string",
            },
        },
        "type": "object",
    },
    "group_switchGroupFirmwareByDomain": {
        "additionalProperties": False,
        "properties": {
            "domainId": {"description": "Domain " "Id", "type": "string"},
            "firmware": {"description": "Firmware " "Version", "type": "string"},
        },
        "type": "object",
    },
    "group_updateSwitchGroupByPut": {
        "additionalProperties": False,
        "properties": {
            "createDatetime": {
                "description": "Create " "datetime " "of " "the " "switch " "group",
                "format": "int64",
                "type": "integer",
            },
            "creatorId": {
                "description": "Creator " "Id of " "the " "switch " "group",
                "type": "string",
            },
            "description": {
                "description": "Description " "of " "the " "switch " "group",
                "type": "string",
            },
            "domainId": {
                "description": "Identifier "
                "of the "
                "management "
                "domain "
                "to which "
                "the "
                "switch "
                "group "
                "belong",
                "type": "string",
            },
            "enableStrongCert": {
                "description": "Enable " "SSH/TLS " "key " "enhance " "mode",
                "type": "boolean",
            },
            "enableTwoFactor": {
                "description": "Enable "
                "two "
                "factor "
                "authentication. "
                "Only "
                "support "
                "FIPS "
                "mode",
                "type": "boolean",
            },
            "firmware": {
                "description": "Firmware " "of the " "switch " "group",
                "type": "string",
            },
            "id": {"description": "Id of the " "switch group", "type": "string"},
            "levelOne": {
                "description": "Level " "one  of " "the " "switch " "group",
                "type": "boolean",
            },
            "levelTwo": {
                "description": "Level " "two of " "the " "switch " "group",
                "type": "boolean",
            },
            "name": {"description": "Name of the " "switch group", "type": "string"},
            "sampledInstant": {
                "description": "Sampled " "instant " "of " "the " "switch " "group",
                "type": "object",
            },
            "switchGroupLevelOneId": {
                "description": "Level " "one " "Id " "of " "the " "switch " "group",
                "type": "string",
            },
            "switchGroupLevelTwoId": {
                "description": "Level " "two " "Id " "of " "the " "switch " "group",
                "type": "string",
            },
            "tenantId": {
                "description": "Tenant " "Id of " "the " "switch " "group",
                "type": "string",
            },
        },
        "type": "object",
    },
    "health_aggMetrics": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra information for " "Aggregation Metrics",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index of the "
                "first Aggregation "
                "Metrics returned "
                "out of the "
                "complete ICX "
                "Metrics list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicates if there "
                "are more Aggregation "
                "Metrics after the "
                "currently displayed "
                "list",
                "type": "boolean",
            },
            "list": {"items": {"$ref": "#/definitions/health_aggs"}, "type": "array"},
            "rawDataTotalCount": {
                "description": "Aggregation " "Metrics " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total of " "Aggregation " "Metrics count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "health_aggs": {
        "additionalProperties": False,
        "properties": {
            "id": {
                "description": "Identifier of the aggregation " "value",
                "type": "string",
            },
            "key": {"description": "Key of the aggregation value", "type": "string"},
            "value": {
                "description": "Metrics of the aggregation " "value",
                "type": "number",
            },
        },
        "type": "object",
    },
    "health_fan": {
        "additionalProperties": False,
        "properties": {
            "serialNumber": {"type": "string"},
            "slotNumber": {"description": "Fan slot number", "type": "integer"},
            "status": {"description": "Fan status", "type": "string"},
            "type": {"description": "Fan type", "type": "string"},
        },
        "type": "object",
    },
    "health_icxMetrics": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra information for " "ICX Metrics",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index of the "
                "first ICX Metrics "
                "returned out of "
                "the complete ICX "
                "Metrics list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicates if there "
                "are more ICX Metrics "
                "after the currently "
                "displayed list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/health_metrics"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "ICX " "Metrics " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total of ICX " "Metrics count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "health_metrics": {
        "additionalProperties": False,
        "properties": {
            "avg": {"description": "Average metrics", "type": "number"},
            "max": {"description": "Max metrics", "type": "number"},
            "min": {"description": "Min metrics", "type": "number"},
            "timestamp": {"description": "Timestamp", "type": "string"},
        },
        "type": "object",
    },
    "health_powerSupply": {
        "additionalProperties": False,
        "properties": {
            "serialNumber": {"type": "string"},
            "slotNumber": {
                "description": "Power supply " "slot number",
                "type": "integer",
            },
            "status": {"description": "Power supply status", "type": "string"},
            "type": {"description": "Power supply type", "type": "string"},
        },
        "type": "object",
    },
    "health_status": {
        "additionalProperties": False,
        "properties": {
            "fan": {
                "description": "Fan",
                "items": {
                    "additionalProperties": False,
                    "properties": {
                        "serialNumber": {"type": "string"},
                        "slotNumber": {
                            "description": "Fan " "slot " "number",
                            "type": "integer",
                        },
                        "status": {"description": "Fan " "status", "type": "string"},
                        "type": {"description": "Fan " "type", "type": "string"},
                    },
                    "type": "object",
                },
                "type": "array",
            },
            "flaggedCount": {
                "description": "Flagged status " "count",
                "type": "integer",
            },
            "offlineCount": {
                "description": "Offline status " "count",
                "type": "integer",
            },
            "onlineCount": {"description": "Online status count", "type": "integer"},
            "powerHealthStatus": {
                "description": "Health status "
                "for ICX/Stack "
                "that contains "
                "power supply, "
                "temperature "
                "and fan",
                "items": {
                    "additionalProperties": False,
                    "properties": {
                        "fan": {
                            "items": {"$ref": "#/definitions/health_fan"},
                            "type": "array",
                        },
                        "powerSupply": {
                            "items": {"$ref": "#/definitions/health_powerSupply"},
                            "type": "array",
                        },
                        "serialNumber": {"type": "string"},
                        "temperature": {
                            "items": {"$ref": "#/definitions/health_temperature"},
                            "type": "array",
                        },
                    },
                    "type": "object",
                },
                "type": "array",
            },
            "powerSupply": {
                "description": "Powersupply",
                "items": {
                    "additionalProperties": False,
                    "properties": {
                        "serialNumber": {"type": "string"},
                        "slotNumber": {
                            "description": "Power " "supply " "slot " "number",
                            "type": "integer",
                        },
                        "status": {
                            "description": "Power " "supply " "status",
                            "type": "string",
                        },
                        "type": {
                            "description": "Power " "supply " "type",
                            "type": "string",
                        },
                    },
                    "type": "object",
                },
                "type": "array",
            },
            "temperature": {
                "description": "Temperature",
                "items": {
                    "additionalProperties": False,
                    "properties": {
                        "serialNumber": {"type": "string"},
                        "slotNumber": {
                            "description": "Solt " "number",
                            "type": "integer",
                        },
                        "temperatureValue": {
                            "description": "Slot " "temperature",
                            "type": "number",
                        },
                    },
                    "type": "object",
                },
                "type": "array",
            },
        },
        "type": "object",
    },
    "health_temperature": {
        "additionalProperties": False,
        "properties": {
            "serialNumber": {"type": "string"},
            "slotNumber": {"description": "Solt number", "type": "integer"},
            "temperatureValue": {
                "description": "Slot " "temperature",
                "type": "number",
            },
        },
        "type": "object",
    },
    "ipConfig_create": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "Alto Id", "type": "string"},
            "dhcpRelayAgent": {
                "description": "DHCP Relay IP " "Address",
                "type": "string",
            },
            "groupId": {"description": "Switch Group Id", "type": "string"},
            "inAclConfigUUID": {
                "description": "Ingress ACL " "Config UUID",
                "type": "string",
            },
            "ipAddress": {"description": "IP Address", "type": "string"},
            "ipRouterId": {"description": "IP Router ID", "type": "string"},
            "ospfArea": {"description": "OSPF IP Address", "type": "string"},
            "outAclConfigUUID": {
                "description": "Egress ACL " "Config UUID",
                "type": "string",
            },
            "port": {"description": "Switch Port", "type": "string"},
            "portName": {"description": "Switch Port Name", "type": "string"},
            "subnetMask": {"description": "Subnet mask", "type": "string"},
            "switchId": {"description": "Switch Id", "type": "string"},
        },
        "type": "object",
    },
    "ipConfig_createResult": {
        "properties": {"id": {"description": "The ID of Setting", "type": "string"}}
    },
    "ipConfig_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "ipConfig_ipConfig": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "Alto Id", "type": "string"},
            "createdTime": {
                "description": "Config Created " "Time",
                "format": "int64",
                "type": "integer",
            },
            "dhcpRelayAgent": {
                "description": "DHCP Replay " "IP Address",
                "type": "string",
            },
            "groupId": {"description": "Switch Group ID", "type": "string"},
            "id": {"description": "Config ID", "type": "string"},
            "inAclConfigName": {
                "description": "Ingress ACL " "Config Name",
                "type": "string",
            },
            "inAclConfigUUID": {
                "description": "Ingress ACL " "Config UUID",
                "type": "string",
            },
            "ipAddress": {"description": "IP Address", "type": "string"},
            "ipRouterId": {"description": "IP Router ID", "type": "string"},
            "ospfArea": {"description": "OSPF IP Address", "type": "string"},
            "outAclConfigName": {
                "description": "Egress ACL " "Config Name",
                "type": "string",
            },
            "outAclConfigUUID": {
                "description": "Egress ACL " "Config UUID",
                "type": "string",
            },
            "port": {"description": "Switch Port", "type": "string"},
            "portName": {"description": "Switch Port Name", "type": "string"},
            "subnetMask": {"description": "Subnet mask", "type": "string"},
            "switchId": {"description": "Switch ID", "type": "string"},
            "switchName": {"description": "Switch Name", "type": "string"},
            "switchStatus": {"description": "Switch Status", "type": "string"},
            "updatedTime": {
                "description": "Config Updated " "Time",
                "format": "int64",
                "type": "integer",
            },
            "vsixEgressAclConfigName": {
                "description": "IPv6 " "Egress " "ACL " "Config " "Name",
                "type": "string",
            },
            "vsixIngressAclConfigName": {
                "description": "IPv6 " "Ingress " "ACL " "Config " "Name",
                "type": "string",
            },
        },
        "type": "object",
    },
    "ipConfig_list": {
        "additionalProperties": False,
        "properties": {
            "firstIndex": {
                "description": "Index of the first "
                "config returned out "
                "of the complete list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator of whether "
                "there are more configs "
                "after the current "
                "displayed list",
                "type": "boolean",
            },
            "list": {
                "description": "The list of configs in this " "response",
                "items": {"$ref": "#/definitions/ipConfig_ipConfig"},
                "type": "array",
            },
            "totalCount": {
                "description": "Total configs count " "in this response",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "ipConfig_modify": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "Alto Id", "type": "string"},
            "dhcpRelayAgent": {
                "description": "DHCP Relay IP " "Address",
                "type": "string",
            },
            "inAclConfigUUID": {
                "description": "Ingress ACL " "Config UUID",
                "type": "string",
            },
            "ipAddress": {"description": "IP Address", "type": "string"},
            "ipRouterId": {"description": "IP Router ID", "type": "string"},
            "ospfArea": {"description": "OSPF IP Address", "type": "string"},
            "outAclConfigUUID": {
                "description": "Egress ACL " "Config UUID",
                "type": "string",
            },
            "port": {"description": "Switch Port", "type": "string"},
            "portName": {"description": "Switch Port Name", "type": "string"},
            "subnetMask": {"description": "Subnet mask", "type": "string"},
        },
        "type": "object",
    },
    "job_errorObject": {
        "additionalProperties": False,
        "properties": {
            "list": {"items": {"type": "string"}, "type": "array"},
            "message": {"type": "string"},
            "msgKey": {"type": "string"},
        },
        "type": "object",
    },
    "job_job": {
        "additionalProperties": False,
        "properties": {
            "action": {"description": "Action of the job", "type": "string"},
            "createdTimestamp": {
                "description": "Created timestamp of " "the job",
                "format": "int64",
                "type": "integer",
            },
            "csvDataMap": {
                "additionalProperties": {"type": "string"},
                "properties": {},
                "type": "object",
            },
            "domainId": {
                "description": "Identifier of the management "
                "domain to which the job "
                "belong",
                "type": "string",
            },
            "failureReason": {
                "description": "Failure reason of the " "job",
                "type": "string",
            },
            "id": {"description": "Identifier of the job", "type": "string"},
            "modifiedTimestamp": {
                "description": "Modified timestamp " "of the job",
                "format": "int64",
                "type": "integer",
            },
            "scheduleId": {"description": "Schedule Id of the job", "type": "string"},
            "status": {"description": "Status of the job", "type": "string"},
            "stickyNodeId": {
                "description": "Sticky node Id of the job",
                "type": "string",
            },
            "switchGroupLevelOneId": {
                "description": "Switch group " "level one Id of " "the job",
                "type": "string",
            },
            "switchGroupLevelTwoId": {
                "description": "Switch group " "level two Id of " "the job",
                "type": "string",
            },
            "switchId": {"description": "Switch Id of the job", "type": "string"},
            "tenantId": {"description": "Tenant Id of the job", "type": "string"},
            "type": {"description": "Type of the job", "type": "string"},
        },
        "type": "object",
    },
    "job_jobSchedule": {
        "additionalProperties": False,
        "properties": {
            "createdTimestamp": {
                "description": "Created " "timestamp of " "job schedule",
                "type": "integer",
            },
            "jobId": {
                "description": "Job Id of job schedule",
                "items": {"type": "string"},
                "type": "array",
            },
            "triggerValue": {
                "description": "Trigger value of " "job schedule",
                "type": "string",
            },
        },
        "type": "object",
    },
    "job_jobScheduleResponse": {
        "additionalProperties": False,
        "properties": {
            "data": {"$ref": "#/definitions/job_jobSchedule"},
            "error": {"$ref": "#/definitions/job_errorObject"},
            "extra": {
                "description": "Extra response " "of job schedule",
                "type": "object",
            },
            "metaData": {
                "description": "metaData of " "job schedule",
                "type": "object",
            },
            "success": {
                "description": "Success " "response of " "job schedule",
                "type": "boolean",
            },
        },
        "type": "object",
    },
    "job_list": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra information for job list",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index of the first job "
                "returned out of the "
                "complete job list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicates if there are more "
                "jobs after the currently "
                "displayed list",
                "type": "boolean",
            },
            "list": {"items": {"$ref": "#/definitions/job_job"}, "type": "array"},
            "rawDataTotalCount": {"description": "List count", "type": "integer"},
            "totalCount": {"description": "Total list count", "type": "integer"},
        },
        "type": "object",
    },
    "lagConfig_create": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "Alto Id", "type": "string"},
            "groupId": {"description": "Switch Group Id", "type": "string"},
            "name": {"description": "The Name of LAG Config", "type": "string"},
            "ports": {
                "description": "The Switch ports would " "like to join together",
                "items": {"type": "string"},
                "type": "array",
            },
            "switchId": {"description": "Switch Id", "type": "string"},
            "taggedVlans": {
                "description": "The LAG's Tagged " "Vlans",
                "type": "string",
            },
            "type": {
                "description": "The LAG Types in STATIC " "or DYNAMIC",
                "enum": ["STATIC", "DYNAMIC"],
                "type": "string",
            },
            "untaggedVlans": {
                "description": "The LAG's " "Untagged Vlans",
                "type": "string",
            },
        },
        "type": "object",
    },
    "lagConfig_createResult": {
        "properties": {"id": {"description": "The ID of LAG Config", "type": "string"}}
    },
    "lagConfig_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "lagConfig_lagConfig": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "The Alto Id of LAG " "Config", "type": "string"},
            "createdTime": {
                "description": "The LAG Types " "in STATIC or " "DYNAMIC",
                "format": "int64",
                "type": "integer",
            },
            "groupId": {"description": "The ID of  Switch " "Group", "type": "string"},
            "id": {"description": "The ID of LAG Config", "type": "string"},
            "lagId": {"description": "The LAG Id of LAG " "Config", "type": "integer"},
            "name": {"description": "The Name of LAG " "Config", "type": "string"},
            "ports": {
                "description": "The Switch ports " "would like to join " "together",
                "items": {"type": "string"},
                "type": "array",
            },
            "switchId": {"description": "The ID of Switch", "type": "string"},
            "taggedVlans": {
                "description": "The Tagged " "Vlans of LAG " "Config",
                "type": "string",
            },
            "type": {
                "description": "The LAG Types in " "STATIC or DYNAMIC",
                "enum": ["STATIC", "DYNAMIC"],
                "type": "string",
            },
            "untaggedVlans": {
                "description": "The Untagged " "Vlans of LAG " "Config",
                "type": "string",
            },
            "updatedTime": {
                "description": "The LAG Types " "in STATIC or " "DYNAMIC",
                "format": "int64",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "lagConfig_list": {
        "additionalProperties": False,
        "properties": {
            "firstIndex": {
                "description": "Index of the first "
                "config returned out "
                "of the complete list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator of whether "
                "there are more configs "
                "after the current "
                "displayed list",
                "type": "boolean",
            },
            "list": {
                "description": "The list of configs in " "this response",
                "items": {"$ref": "#/definitions/lagConfig_lagConfig"},
                "type": "array",
            },
            "totalCount": {
                "description": "Total configs count " "in this response",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "lagConfig_modify": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "Alto Id", "type": "string"},
            "name": {"description": "The Name of LAG Config", "type": "string"},
            "ports": {
                "description": "The Switch ports would " "like to join together",
                "items": {"type": "string"},
                "type": "array",
            },
            "taggedVlans": {
                "description": "The LAG's Tagged " "Vlans",
                "type": "string",
            },
            "untaggedVlans": {
                "description": "The LAG's " "Untagged Vlans",
                "type": "string",
            },
        },
        "type": "object",
    },
    "portCapacity_capacities": {
        "additionalProperties": False,
        "properties": {
            "capacity": {"description": "Port Speed " "Capacity", "type": "string"}
        },
        "type": "object",
    },
    "portCapacity_result": {
        "additionalProperties": False,
        "properties": {
            "extra": {"description": "Extra field", "type": "object"},
            "firstIndex": {
                "description": "The first data " "index for " "current reulst",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator of " "remaining data",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/portCapacity_capacities"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "Data " "Count",
                "type": "integer",
            },
            "totalCount": {"description": "Total Data " "Count", "type": "integer"},
        },
        "type": "object",
    },
    "portMacSecurity_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "portMacSecurity_portMacSecurity": {
        "additionalProperties": False,
        "properties": {
            "age": {"description": "Port MAC " "Security " "age", "type": "integer"},
            "autoSave": {
                "description": "Port "
                "MAC "
                "Security "
                "auto "
                "save "
                "in "
                "minute",
                "type": "integer",
            },
            "id": {"description": "Port MAC " "Security ID", "type": "string"},
            "maximum": {
                "description": "Maximum " "port " "MAC " "security " "number",
                "type": "integer",
            },
            "portMacSecurityEnable": {
                "description": "Port " "MAC " "Security " "Option",
                "type": "boolean",
            },
            "switchId": {
                "description": "Port " "MAC " "Security " "Switch " "ID",
                "type": "string",
            },
            "violation": {
                "description": "Port " "MAC " "Security " "violation " "action",
                "enum": ["PROTECT", "RESTRICT", "SHUTDOWN"],
                "type": "string",
            },
            "violationMinute": {
                "description": "Port " "MAC " "Security " "violation " "time",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "portMacSecurity_secureMac": {
        "additionalProperties": False,
        "properties": {
            "id": {"description": "Secure MAC ID", "type": "string"},
            "mac": {"description": "Secure MAC " "address", "type": "string"},
            "vlan": {"description": "Secure MAC VLAN", "type": "integer"},
        },
        "type": "object",
    },
    "portMacSecurity_secureMacs": {
        "additionalProperties": False,
        "properties": {
            "secureMac": {
                "items": {"$ref": "#/definitions/portMacSecurity_secureMac"},
                "type": "array",
            }
        },
        "type": "object",
    },
    "portProfiles_applyPortProfile": {
        "additionalProperties": False,
        "properties": {
            "portTemplateConfigId": {
                "description": "Port " "Template " "config " "ID",
                "type": "string",
            },
            "pushTime": {
                "description": "Push " "time",
                "format": "int64",
                "type": "integer",
            },
            "pushTimeType": {
                "description": "Push " "time " "type",
                "enum": ["NOW", "SCHEDULE"],
                "type": "string",
            },
            "targetPorts": {
                "description": "Port " "Template " "target " "ports",
                "items": {"$ref": "#/definitions/portProfiles_targetPorts"},
                "type": "array",
            },
        },
        "type": "object",
    },
    "portProfiles_createPortProfile": {
        "additionalProperties": False,
        "properties": {
            "cli": {"description": "Port " "Template's " "CLI", "type": "string"},
            "groupId": {
                "description": "Port " "Template " "group " "ID",
                "type": "string",
            },
            "name": {"description": "Port " "Template " "name", "type": "string"},
            "taggedVlans": {
                "description": "Port " "Template " "tag " "VLAN " "values",
                "items": {"type": "string"},
                "type": "array",
            },
            "untaggedVlan": {
                "description": "Port " "Template " "untag " "VLAN " "value",
                "type": "string",
            },
            "variables": {
                "description": "Port " "Template " "CLI's " "variable",
                "items": {"$ref": "#/definitions/portProfiles_variable"},
                "type": "array",
            },
        },
        "type": "object",
    },
    "portProfiles_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "portProfiles_portProfileConfig": {
        "additionalProperties": False,
        "properties": {
            "cli": {"description": "Port " "Template " "CLI", "type": "string"},
            "groupId": {
                "description": "Port " "Template " "group " "ID",
                "type": "string",
            },
            "id": {"description": "Port " "Template " "config ID", "type": "string"},
            "name": {"description": "Port " "Template " "name", "type": "string"},
            "pushTime": {
                "description": "Push " "time",
                "format": "int64",
                "type": "integer",
            },
            "pushTimeType": {
                "description": "Push " "time " "type",
                "enum": ["NOW", "SCHEDULE"],
                "type": "string",
            },
            "taggedVlans": {
                "description": "Port " "Template " "tag " "VLAN " "values",
                "items": {"type": "string"},
                "type": "array",
            },
            "targetPorts": {
                "description": "Port " "Template " "target " "ports",
                "items": {
                    "$ref": "#/definitions/portProfiles_targetPortsWithSwitchName"
                },
                "type": "array",
            },
            "untaggedVlan": {
                "description": "Port " "Template " "untag " "VLAN " "value",
                "type": "string",
            },
            "variables": {
                "items": {"$ref": "#/definitions/portProfiles_variable"},
                "type": "array",
            },
        },
        "type": "object",
    },
    "portProfiles_portProfileQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {"description": "Extra", "type": "object"},
            "firstIndex": {"description": "First " "index", "type": "integer"},
            "hasMore": {"description": "Has " "more", "type": "boolean"},
            "list": {
                "items": {"$ref": "#/definitions/portProfiles_portProfiles"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Raw " "data " "total " "count",
                "type": "integer",
            },
            "totalCount": {"description": "Total " "count", "type": "integer"},
        },
        "type": "object",
    },
    "portProfiles_portProfileSampleQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {"description": "Extra", "type": "object"},
            "firstIndex": {"description": "First " "index", "type": "integer"},
            "hasMore": {"description": "Has " "more", "type": "boolean"},
            "list": {
                "items": {"$ref": "#/definitions/portProfiles_sampleResult"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Raw " "data " "total " "count",
                "type": "integer",
            },
            "totalCount": {"description": "Total " "count", "type": "integer"},
        },
        "type": "object",
    },
    "portProfiles_portProfiles": {
        "additionalProperties": False,
        "properties": {
            "id": {"description": "Port Template ID", "type": "string"},
            "name": {"description": "Port Template " "name", "type": "string"},
            "portTemplateConfigId": {
                "description": "Port " "Template " "config " "ID",
                "type": "string",
            },
            "scheduledPortTemplateConfigs": {
                "description": "Schedule " "Port " "Template " "config",
                "items": {
                    "$ref": "#/definitions/portProfiles_simpleSchedulePortProfileConfig"
                },
                "type": "array",
            },
        },
        "type": "object",
    },
    "portProfiles_sampleResult": {
        "additionalProperties": False,
        "properties": {
            "cli": {"description": "Port Template " "example CLI", "type": "string"},
            "id": {"description": "Port Template " "example ID", "type": "string"},
            "name": {"description": "Port Template " "example name", "type": "string"},
            "version": {
                "description": "Port " "Template " "example " "version",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "portProfiles_simpleSchedulePortProfileConfig": {
        "additionalProperties": False,
        "properties": {
            "id": {
                "description": "Schedule " "Port " "Template " "config " "ID",
                "type": "string",
            },
            "name": {
                "description": "Schedule " "Port " "Template " "config " "name",
                "type": "string",
            },
            "pushTime": {
                "description": "Schedule " "Port " "Template " "config " "push " "time",
                "format": "int64",
                "type": "integer",
            },
            "targetPorts": {
                "description": "Schedule "
                "Port "
                "Template "
                "config "
                "target "
                "ports",
                "items": {"$ref": "#/definitions/portProfiles_targetPorts"},
                "type": "array",
            },
        },
        "type": "object",
    },
    "portProfiles_targetPorts": {
        "additionalProperties": False,
        "properties": {
            "port": {
                "description": "Port for apply " "Port Template",
                "type": "string",
            },
            "switchId": {
                "description": "Port " "Template " "target " "ports' " "switch ID",
                "type": "string",
            },
        },
        "type": "object",
    },
    "portProfiles_targetPortsWithSwitchName": {
        "additionalProperties": False,
        "properties": {
            "port": {
                "description": "Port " "for " "apply " "Port " "Template",
                "type": "string",
            },
            "switchId": {
                "description": "Port " "Template " "target " "ports' " "switch " "ID",
                "type": "string",
            },
            "switchName": {
                "description": "Port " "Template " "target " "ports' " "switch " "name",
                "type": "string",
            },
        },
        "type": "object",
    },
    "portProfiles_variable": {
        "additionalProperties": False,
        "properties": {
            "name": {"description": "Port Template " "variable name", "type": "string"},
            "type": {
                "description": "Port Template "
                "variable type, "
                "should be one of "
                "[STRING, RANGE, "
                "IP_ADDRESS]",
                "type": "string",
            },
            "value": {
                "description": "Port Template " "variable variable " "value",
                "type": "string",
            },
        },
        "type": "object",
    },
    "portSettings_LldpQos": {
        "additionalProperties": False,
        "properties": {
            "applicationType": {
                "description": "Port " "Application " "Type",
                "enum": [
                    "GUEST_VOICE",
                    "GUEST_VOICE_SIGNALING",
                    "SOFTPHONE_VOICE",
                    "STREAMING_VIDEO",
                    "VIDEO_CONFERENCING",
                    "VIDEO_SIGNALING",
                    "VOICE",
                    "VOICE_SIGNALING",
                ],
                "type": "string",
            },
            "dscp": {"description": "Port DSCP", "type": "integer"},
            "priority": {"description": "Port Priority", "type": "integer"},
            "qosVlanType": {
                "description": "Port Qos Vlan " "Type",
                "enum": ["PRIORITY_TAGGED", "TAGGED", "UNTAGGED"],
                "type": "string",
            },
            "vlanId": {"description": "Port Vlan Id", "type": "integer"},
        },
        "type": "object",
    },
    "portSettings_PortSettings": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "Alto Id", "type": "string"},
            "arpInspectionEnabled": {
                "description": "ARP " "Inspection " "Enabled",
                "type": "boolean",
            },
            "authDefaultVlan": {
                "description": "Auth " "Default " "Vlan",
                "type": "integer",
                "x-isnullable": True,
            },
            "authFailAction": {
                "description": "Auth " "Fail " "Action",
                "type": "string",
            },
            "authTimeoutAction": {
                "description": "Auth " "Timeout " "Action",
                "type": "string",
            },
            "authenticationType": {
                "description": "Authentication " "Type",
                "type": "string",
            },
            "broadcastLimitKbps": {
                "description": "Broadcast " "Limit " "Kbps",
                "type": "integer",
            },
            "broadcastLimitPkts": {
                "description": "Broadcast " "Limit " "Pkts",
                "type": "integer",
            },
            "changeAuthOrder": {
                "description": "Change " "Auth " "Order",
                "type": "boolean",
            },
            "createdTime": {
                "description": "The " "create " "time of " "the Port " "Settings",
                "format": "int64",
                "type": "integer",
            },
            "criticalVlan": {
                "description": "Critical " "Vlan",
                "type": "integer",
                "x-isnullable": True,
            },
            "customize": {"description": "Port " "Customize", "type": "boolean"},
            "dhcpSnoopingTrustPortEnabled": {
                "description": "DHCP " "Snooping " "Trust " "Port " "Enabled",
                "type": "boolean",
            },
            "dot1XPortControl": {
                "description": "Dot1 " "XPort " "Control",
                "type": "string",
                "x-isnullable": True,
            },
            "dscpTrustEnabled": {
                "description": "DSCP " "Trust " "Enabled",
                "type": "boolean",
            },
            "flexibleAuthenticationEnabled": {
                "description": "Flexible " "Authentication " "Enabled",
                "type": "boolean",
            },
            "fromLag": {
                "description": "Form LAG or " "not, null " "for " "meaningless",
                "type": "boolean",
            },
            "groupId": {"description": "Group Id", "type": "string"},
            "id": {"description": "Id", "type": "string"},
            "inAclConfigName": {
                "description": "Ingress " "ACL " "Config " "Name",
                "type": "string",
            },
            "inAclConfigUUID": {
                "description": "Ingress " "ACL " "Config " "UUID",
                "type": "string",
            },
            "ipsgEnabled": {"description": "IPSG " "Enabled", "type": "boolean"},
            "isStormControlUnitKbps": {
                "description": "Is " "Storm " "Control " "Unit " "kbps",
                "type": "boolean",
            },
            "lldpEnabled": {"description": "LLDP " "Enabled", "type": "boolean"},
            "lldpQosList": {
                "items": {"$ref": "#/definitions/portSettings_LldpQos"},
                "type": "array",
            },
            "multicastLimitKbps": {
                "description": "Multicast " "Limit " "Kbps",
                "type": "integer",
            },
            "multicastLimitPkts": {
                "description": "Multicast " "Limit " "Pkts",
                "type": "integer",
            },
            "outAclConfigName": {
                "description": "Egress " "ACL " "Config " "Name",
                "type": "string",
            },
            "outAclConfigUUID": {
                "description": "Egress " "ACL " "Config " "UUID",
                "type": "string",
            },
            "poeBudget": {"description": "PoE Budget", "type": "integer"},
            "poeCapability": {"description": "PoE " "Capability", "type": "boolean"},
            "poeClass": {
                "description": "PoE Class",
                "enum": ["0", "1", "2", "3", "4", "5", "6", "7", "8"],
                "type": "string",
            },
            "poeEnabled": {"description": "PoE " "Enabled", "type": "boolean"},
            "poePriority": {"description": "PoE " "Priority", "type": "integer"},
            "port": {"description": "Port", "type": "string"},
            "portDhcpSnooping": {"$ref": "#/definitions/portSettings_portDhcpSnooping"},
            "portEnabled": {"description": "Port " "Enabled", "type": "boolean"},
            "portName": {"description": "Port Name", "type": "string"},
            "portProtected": {"description": "Port " "Protected", "type": "boolean"},
            "portSpeed": {
                "description": "Port Speed",
                "enum": [
                    "NONE",
                    "1G",
                    "10G",
                    "AUTO",
                    "10-HALF",
                    "10-FULL",
                    "100-HALF",
                    "100-FULL",
                    "1000-FULL",
                    "1000-FULL-MASTER",
                    "1000-FULL-SLAVE",
                    "2500-FULL",
                    "2500-FULL-MASTER",
                    "2500-FULL-SLAVE",
                    "5G-FULL",
                    "5G-FULL-MASTER",
                    "5G-FULL-SLAVE",
                    "10G-FULL",
                    "10G-FULL-MASTER",
                    "10G-FULL-SLAVE",
                    "25G-FULL",
                    "40G-FULL",
                    "100G-FULL",
                    "OPTIC",
                ],
                "type": "string",
            },
            "pppoeIa": {"$ref": "#/definitions/portSettings_pppoeIaObject"},
            "restrictedVlan": {
                "description": "Restricted " "Vlan",
                "type": "integer",
                "x-isnullable": True,
            },
            "rstpAdminEdgePortEnabled": {
                "description": "RSTP " "Admin " "Edge " "Port " "Enabled",
                "type": "boolean",
            },
            "shouldAlertAaaAndRadiusNotApply": {
                "description": "Should " "Alert " "And " "Radius " "Not " "Apply",
                "type": "boolean",
                "x-isnullable": True,
            },
            "stpBpduGuardEnabled": {
                "description": "STP " "BPDU " "GUARD " "Enabled",
                "type": "boolean",
            },
            "stpRootGuardEnabled": {
                "description": "STP " "Root " "Guard  " "Enabled",
                "type": "boolean",
            },
            "switchId": {"description": "Switch Id", "type": "string"},
            "switchLevelAuthDefaultVlan": {
                "description": "Switch " "Level " "Auth " "Default " "Vlan",
                "type": "integer",
                "x-isnullable": True,
            },
            "taggedVlans": {"description": "Tagged " "Vlans", "type": "string"},
            "unknownUnicastLimitKbps": {
                "description": "Unknown " "Unicast " "Limit " "Kbps",
                "type": "integer",
            },
            "unknownUnicastLimitPkts": {
                "description": "Unknown " "Unicast " "Limit " "Pkts",
                "type": "integer",
            },
            "untaggedVlans": {"description": "Untagged " "Vlans", "type": "string"},
            "updatedTime": {
                "description": "The " "modify " "time of " "the Port " "Settings",
                "format": "int64",
                "type": "integer",
            },
            "v6NdInspectionEnabled": {
                "description": "IPv6 " "ND " "Inspection " "Enabled",
                "type": "boolean",
            },
            "voiceVlanId": {"description": "Voice " "Vlan Id", "type": "integer"},
            "vsixEgressAclConfigName": {
                "description": "IPv6 " "Egress " "ACL " "Config " "Name",
                "type": "string",
            },
            "vsixIngressAclConfigName": {
                "description": "IPv6 " "Ingress " "ACL " "Config " "Name",
                "type": "string",
            },
        },
        "type": "object",
    },
    "portSettings_PortSettingsQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "Port "
                "Settings "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "Port "
                "Settings "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "Port "
                "Settings "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/portSettings_PortSettings"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "Port " "Settings " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total "
                "Port "
                "Settings "
                "count "
                "in "
                "this "
                "response",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "portSettings_UpdatePortSettings": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "Alto Id", "type": "string"},
            "arpInspectionEnabled": {
                "description": "ARP " "Inspection " "Enabled",
                "type": "boolean",
            },
            "authDefaultVlan": {
                "description": "Auth " "Default " "Vlan",
                "type": "integer",
                "x-isnullable": True,
            },
            "authFailAction": {
                "description": "Auth " "Fail " "Action",
                "type": "string",
            },
            "authTimeoutAction": {
                "description": "Auth " "Timeout " "Action",
                "type": "string",
            },
            "authenticationType": {
                "description": "Authentication " "Type",
                "type": "string",
            },
            "broadcastLimitKbps": {
                "description": "Broadcast " "Limit " "Kbps",
                "type": "integer",
            },
            "broadcastLimitPkts": {
                "description": "Broadcast " "Limit " "Pkts",
                "type": "integer",
            },
            "changeAuthOrder": {
                "description": "Change " "Auth " "Order",
                "type": "boolean",
            },
            "criticalVlan": {
                "description": "Critical " "Vlan",
                "type": "integer",
                "x-isnullable": True,
            },
            "customize": {"description": "Port " "Customize", "type": "boolean"},
            "dhcpSnoopingTrustPortEnabled": {
                "description": "DHCP " "Snooping " "Trust " "Port " "Enabled",
                "type": "boolean",
            },
            "dot1XPortControl": {
                "description": "Dot1 " "XPort " "Control",
                "type": "string",
                "x-isnullable": True,
            },
            "dscpTrustEnabled": {
                "description": "DSCP " "Trust " "Enabled",
                "type": "boolean",
            },
            "flexibleAuthenticationEnabled": {
                "description": "Flexible " "Authentication " "Enabled",
                "type": "boolean",
            },
            "inAclConfigName": {
                "description": "Ingress " "ACL " "Config " "Name",
                "type": "string",
            },
            "inAclConfigUUID": {
                "description": "Ingress " "ACL " "Config " "UUID",
                "type": "string",
            },
            "ipsgEnabled": {"description": "IPSG " "Enabled", "type": "boolean"},
            "isStormControlUnitKbps": {
                "description": "Is " "Storm " "Control " "Unit " "kbps",
                "type": "boolean",
            },
            "lldpEnabled": {"description": "LLDP " "Enabled", "type": "boolean"},
            "lldpQosList": {
                "items": {"$ref": "#/definitions/portSettings_LldpQos"},
                "type": "array",
            },
            "multicastLimitKbps": {
                "description": "Multicast " "Limit " "Kbps",
                "type": "integer",
            },
            "multicastLimitPkts": {
                "description": "Multicast " "Limit " "Pkts",
                "type": "integer",
            },
            "outAclConfigName": {
                "description": "Egress " "ACL " "Config " "Name",
                "type": "string",
            },
            "outAclConfigUUID": {
                "description": "Egress " "ACL " "Config " "UUID",
                "type": "string",
            },
            "poeBudget": {"description": "PoE " "Budget", "type": "integer"},
            "poeClass": {
                "description": "PoE " "Class",
                "enum": ["0", "1", "2", "3", "4", "5", "6", "7", "8"],
                "type": "string",
            },
            "poeEnabled": {"description": "PoE " "Enabled", "type": "boolean"},
            "poePriority": {"description": "PoE " "Priority", "type": "integer"},
            "portDhcpSnooping": {"$ref": "#/definitions/portSettings_portDhcpSnooping"},
            "portEnabled": {"description": "Port " "Enabled", "type": "boolean"},
            "portName": {"description": "Port " "Name", "type": "string"},
            "portProtected": {"description": "Port " "Protected", "type": "boolean"},
            "portSpeed": {
                "description": "Port " "Speed",
                "enum": [
                    "NONE",
                    "1G",
                    "10G",
                    "AUTO",
                    "10-HALF",
                    "10-FULL",
                    "100-HALF",
                    "100-FULL",
                    "1000-FULL",
                    "1000-FULL-MASTER",
                    "1000-FULL-SLAVE",
                    "2500-FULL",
                    "2500-FULL-MASTER",
                    "2500-FULL-SLAVE",
                    "5G-FULL",
                    "5G-FULL-MASTER",
                    "5G-FULL-SLAVE",
                    "10G-FULL",
                    "10G-FULL-MASTER",
                    "10G-FULL-SLAVE",
                    "25G-FULL",
                    "40G-FULL",
                    "100G-FULL",
                    "OPTIC",
                ],
                "type": "string",
            },
            "pppoeIa": {"$ref": "#/definitions/portSettings_pppoeIaObject"},
            "restrictedVlan": {
                "description": "Restricted " "Vlan",
                "type": "integer",
                "x-isnullable": True,
            },
            "revert": {"description": "Port " "Revert", "type": "boolean"},
            "rstpAdminEdgePortEnabled": {
                "description": "RSTP " "Admin " "Edge " "Port " "Enabled",
                "type": "boolean",
            },
            "shouldAlertAaaAndRadiusNotApply": {
                "description": "Should " "Alert " "And " "Radius " "Not " "Apply",
                "type": "boolean",
                "x-isnullable": True,
            },
            "stpBpduGuardEnabled": {
                "description": "STP " "BPDU " "GUARD " "Enabled",
                "type": "boolean",
            },
            "stpRootGuardEnabled": {
                "description": "STP " "Root " "Guard  " "Enabled",
                "type": "boolean",
            },
            "switchLevelAuthDefaultVlan": {
                "description": "Switch " "Level " "Auth " "Default " "Vlan",
                "type": "integer",
                "x-isnullable": True,
            },
            "taggedVlans": {"description": "Tagged " "Vlans", "type": "string"},
            "unknownUnicastLimitKbps": {
                "description": "Unknown " "Unicast " "Limit " "Kbps",
                "type": "integer",
            },
            "unknownUnicastLimitPkts": {
                "description": "Unknown " "Unicast " "Limit " "Pkts",
                "type": "integer",
            },
            "untaggedVlans": {"description": "Untagged " "vlans", "type": "string"},
            "v6NdInspectionEnabled": {
                "description": "IPv6 " "ND " "Inspection " "Enabled",
                "type": "boolean",
            },
            "voiceVlanId": {"description": "Voice " "Vlan " "Id", "type": "integer"},
        },
        "type": "object",
    },
    "portSettings_createBulk": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "Alto Id", "type": "string"},
            "arpInspectionEnabled": {
                "description": "ARP " "Inspection " "Enabled",
                "type": "boolean",
            },
            "authDefaultVlan": {
                "description": "Auth " "Default " "Vlan",
                "type": "integer",
                "x-isnullable": True,
            },
            "authFailAction": {
                "description": "Auth " "Fail " "Action",
                "type": "string",
            },
            "authTimeoutAction": {
                "description": "Auth " "Timeout " "Action",
                "type": "string",
            },
            "authenticationType": {
                "description": "Authentication " "Type",
                "type": "string",
            },
            "broadcastLimitKbps": {
                "description": "Broadcast " "Limit " "Kbps",
                "type": "integer",
            },
            "broadcastLimitPkts": {
                "description": "Broadcast " "Limit " "Pkts",
                "type": "integer",
            },
            "changeAuthOrder": {
                "description": "Change " "Auth " "Order",
                "type": "boolean",
            },
            "criticalVlan": {
                "description": "Critical " "Vlan",
                "type": "integer",
                "x-isnullable": True,
            },
            "customize": {"description": "Port " "Customize", "type": "boolean"},
            "dhcpSnoopingTrustPortEnabled": {
                "description": "DHCP " "Snooping " "Trust " "Port " "Enabled",
                "type": "boolean",
            },
            "dot1XPortControl": {
                "description": "Dot1 " "XPort " "Control",
                "type": "string",
                "x-isnullable": True,
            },
            "dscpTrustEnabled": {
                "description": "DSCP " "Trust " "Enabled",
                "type": "boolean",
            },
            "flexibleAuthenticationEnabled": {
                "description": "Flexible " "Authentication " "Enabled",
                "type": "boolean",
            },
            "groupId": {"description": "Group Id", "type": "string"},
            "idList": {"$ref": "#/definitions/common_idList"},
            "ignoreList": {
                "description": "attributes " "not to " "overwrite",
                "items": {"type": "string"},
                "type": "array",
            },
            "inAclConfigName": {
                "description": "Ingress " "ACL " "Config " "Name",
                "type": "string",
            },
            "inAclConfigUUID": {
                "description": "Ingress " "ACL " "Config " "UUID",
                "type": "string",
            },
            "ipsgEnabled": {"description": "IPSG " "Enabled", "type": "boolean"},
            "isStormControlUnitKbps": {
                "description": "Is " "Storm " "Control " "Unit " "kbps",
                "type": "boolean",
            },
            "lldpEnabled": {"description": "LLDP " "Enabled", "type": "boolean"},
            "lldpQosList": {
                "items": {"$ref": "#/definitions/portSettings_LldpQos"},
                "type": "array",
            },
            "multicastLimitKbps": {
                "description": "Multicast " "Limit " "Kbps",
                "type": "integer",
            },
            "multicastLimitPkts": {
                "description": "Multicast " "Limit " "Pkts",
                "type": "integer",
            },
            "outAclConfigName": {
                "description": "Egress " "ACL " "Config " "Name",
                "type": "string",
            },
            "outAclConfigUUID": {
                "description": "Egress " "ACL " "Config " "UUID",
                "type": "string",
            },
            "poeBudget": {"description": "PoE Budget", "type": "integer"},
            "poeClass": {
                "description": "PoE Class",
                "enum": ["0", "1", "2", "3", "4", "5", "6", "7", "8"],
                "type": "string",
            },
            "poeEnabled": {"description": "PoE Enabled", "type": "boolean"},
            "poePriority": {"description": "PoE " "Priority", "type": "integer"},
            "port": {"description": "Port", "type": "string"},
            "portDhcpSnooping": {"$ref": "#/definitions/portSettings_portDhcpSnooping"},
            "portEnabled": {"description": "Port " "Enabled", "type": "boolean"},
            "portName": {"description": "Port Name", "type": "string"},
            "portProtected": {"description": "Port " "Protected", "type": "boolean"},
            "portSpeed": {
                "description": "Port Speed",
                "enum": [
                    "NONE",
                    "1G",
                    "10G",
                    "AUTO",
                    "10-HALF",
                    "10-FULL",
                    "100-HALF",
                    "100-FULL",
                    "1000-FULL",
                    "1000-FULL-MASTER",
                    "1000-FULL-SLAVE",
                    "2500-FULL",
                    "2500-FULL-MASTER",
                    "2500-FULL-SLAVE",
                    "5G-FULL",
                    "5G-FULL-MASTER",
                    "5G-FULL-SLAVE",
                    "10G-FULL",
                    "10G-FULL-MASTER",
                    "10G-FULL-SLAVE",
                    "25G-FULL",
                    "40G-FULL",
                    "100G-FULL",
                    "OPTIC",
                ],
                "type": "string",
            },
            "pppoeIa": {"$ref": "#/definitions/portSettings_pppoeIaObject"},
            "restrictedVlan": {
                "description": "Restricted " "Vlan",
                "type": "integer",
                "x-isnullable": True,
            },
            "revert": {"description": "Port Revert", "type": "boolean"},
            "rstpAdminEdgePortEnabled": {
                "description": "RSTP " "Admin " "Edge " "Port " "Enabled",
                "type": "boolean",
            },
            "stpBpduGuardEnabled": {
                "description": "STP " "BPDU " "GUARD " "Enabled",
                "type": "boolean",
            },
            "stpRootGuardEnabled": {
                "description": "STP " "Root " "Guard  " "Enabled",
                "type": "boolean",
            },
            "switchId": {"description": "Switch Id", "type": "string"},
            "taggedVlans": {"description": "Tagged " "Vlans", "type": "string"},
            "unknownUnicastLimitKbps": {
                "description": "Unknown " "Unicast " "Limit " "Kbps",
                "type": "integer",
            },
            "unknownUnicastLimitPkts": {
                "description": "Unknown " "Unicast " "Limit " "Pkts",
                "type": "integer",
            },
            "untaggedVlans": {"description": "Untagged " "vlans", "type": "string"},
            "v6NdInspectionEnabled": {
                "description": "IPv6 " "ND " "Inspection " "Enabled",
                "type": "boolean",
            },
            "voiceVlanId": {"description": "Voice Vlan " "Id", "type": "integer"},
        },
        "type": "object",
    },
    "portSettings_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "portSettings_portDhcpSnooping": {
        "additionalProperties": False,
        "properties": {
            "circuitId": {
                "description": "Port " "DHCP " "Snooping " "Circuit " "ID",
                "type": "string",
            },
            "ipv4": {
                "description": "Port DHCP " "Snooping " "IPv4 " "Enabled",
                "type": "boolean",
            },
            "ipv6": {
                "description": "Port DSCP " "Snooping " "IPv6 " "Enabled",
                "type": "boolean",
            },
            "remoteId": {
                "description": "Port " "DHCP " "Snooping " "Remote " "ID",
                "type": "string",
            },
            "v6RemoteId": {
                "description": "Port " "DHCP " "Snooping " "IPv6 " "Remote " "ID",
                "type": "string",
            },
        },
        "type": "object",
    },
    "portSettings_pppoeIaObject": {
        "additionalProperties": False,
        "properties": {
            "circuitId": {"description": "PPPoE IA " "Circuit " "Id", "type": "string"},
            "pppoeIaType": {
                "description": "PPPoE " "IA",
                "enum": ["NONE", "SERVER", "CLIENT"],
                "type": "string",
            },
            "remoteId": {"description": "PPPoE IA " "Remote Id", "type": "string"},
            "vendorTagPolicy": {
                "description": "PPPoE " "IA " "Vendor " "Tag " "Policy",
                "enum": ["NONE", "STRIP"],
                "type": "string",
            },
        },
        "type": "object",
    },
    "registration_clientObjectID": {
        "additionalProperties": False,
        "properties": {
            "extraValues": {
                "description": "Extra " "values " "of the " "client",
                "type": "object",
            },
            "id": {"description": "Identifier of " "the client", "type": "string"},
            "label": {"description": "Label of the " "client", "type": "string"},
            "type": {"description": "Type of the " "client", "type": "string"},
        },
        "type": "object",
    },
    "registration_createResult": {
        "additionalProperties": False,
        "properties": {
            "data": {"$ref": "#/definitions/registration_clientObjectID"},
            "error": {"$ref": "#/definitions/registration_errorObject"},
            "extra": {"description": "Any additional " "response", "type": "object"},
            "metaData": {
                "description": "Matadata of " "Rule create " "result",
                "type": "object",
            },
            "success": {
                "description": "Create " "result " "success or " "not",
                "type": "boolean",
            },
        },
        "type": "object",
    },
    "registration_deleteMultipleResult": {
        "additionalProperties": False,
        "properties": {
            "data": {"$ref": "#/definitions/registration_list"},
            "error": {"$ref": "#/definitions/registration_errorObject"},
            "extra": {"description": "Any " "additional " "response", "type": "object"},
            "metaData": {
                "description": "Matadata "
                "of "
                "delete "
                "multiple "
                "rules "
                "result",
                "type": "object",
            },
            "success": {
                "description": "Delete " "multiple " "result " "success " "or " "not",
                "type": "boolean",
            },
        },
        "type": "object",
    },
    "registration_deleteResult": {
        "additionalProperties": False,
        "properties": {
            "data": {"$ref": "#/definitions/registration_clientObjectID"},
            "error": {"$ref": "#/definitions/registration_errorObject"},
            "extra": {"description": "Any additional " "response", "type": "object"},
            "metaData": {
                "description": "Matadata of " "Rule delete " "result",
                "type": "object",
            },
            "success": {
                "description": "Delete " "result " "success or " "not",
                "type": "boolean",
            },
        },
        "type": "object",
    },
    "registration_errorObject": {
        "additionalProperties": False,
        "properties": {
            "list": {"items": {"type": "string"}, "type": "array"},
            "message": {"type": "string"},
            "msgKey": {"type": "string"},
        },
        "type": "object",
    },
    "registration_list": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any additional " "response data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index of the "
                "first "
                "registration rule "
                "returned out of "
                "the complete "
                "registration rule "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator of whether "
                "there are more "
                "registration rule "
                "after the current "
                "displayed list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/registration_registrationRule"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Registration " "rule list " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "Registration rule " "list count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "registration_modifyResult": {
        "additionalProperties": False,
        "properties": {
            "data": {"$ref": "#/definitions/registration_clientObjectID"},
            "error": {"$ref": "#/definitions/registration_errorObject"},
            "extra": {"description": "Any additional " "response", "type": "object"},
            "metaData": {
                "description": "Matadata of " "rule modify " "result",
                "type": "object",
            },
            "success": {
                "description": "Modify " "result " "success or " "not",
                "type": "boolean",
            },
        },
        "type": "object",
    },
    "registration_registrationRule": {
        "additionalProperties": False,
        "properties": {
            "createDatetime": {
                "description": "Create "
                "datetime "
                "of "
                "the "
                "registration "
                "rule",
                "format": "int64",
                "type": "integer",
            },
            "creatorId": {
                "description": "Creator " "Id of " "the " "registration " "rule",
                "type": "string",
            },
            "creatorName": {
                "description": "Creator " "name " "of " "the " "registration " "rule",
                "type": "string",
            },
            "description": {
                "description": "Description " "of " "the " "registration " "rule",
                "type": "string",
            },
            "groupName": {
                "description": "Switch "
                "group "
                "name "
                "of the "
                "registration "
                "rule",
                "type": "string",
            },
            "id": {
                "description": "Identifier of " "the " "registration " "rule",
                "type": "string",
            },
            "ipFrom": {
                "description": "Start IP " "range of " "the " "registration " "rule",
                "type": "string",
            },
            "ipRange": {
                "description": "IP range " "of the " "registration " "rule",
                "type": "string",
            },
            "ipTo": {
                "description": "End IP " "range of " "the " "registration " "rule",
                "type": "string",
            },
            "label": {
                "description": "Lable of " "the " "registration " "rule",
                "type": "string",
            },
            "modelNumber": {
                "description": "Switch "
                "Model "
                "number "
                "of "
                "the "
                "registration "
                "rule",
                "type": "string",
            },
            "network": {
                "description": "Network " "of the " "registration " "rule",
                "type": "string",
            },
            "rank": {
                "description": "Rank of the " "registration " "rule",
                "type": "integer",
            },
            "subnetMask": {
                "description": "Subnet " "mask " "of " "the " "registration " "rule",
                "type": "string",
            },
            "switchGroupId": {
                "description": "Switch "
                "group "
                "Id "
                "of "
                "the "
                "registration "
                "rule",
                "type": "string",
            },
            "type": {
                "description": "Type of the " "registration " "rule",
                "enum": ["IP_RANGE", "SUBNET", "MODEL_NUMBER"],
                "type": "string",
            },
        },
        "type": "object",
    },
    "registration_ruleQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "data": {"$ref": "#/definitions/registration_list"},
            "error": {"$ref": "#/definitions/registration_errorObject"},
            "extra": {"description": "Any " "additional " "response", "type": "object"},
            "metaData": {
                "description": "Matadata " "of " "Rule " "query " "result",
                "type": "object",
            },
            "success": {
                "description": "Rule " "query " "result " "success " "or " "not",
                "type": "boolean",
            },
        },
        "type": "object",
    },
    "registration_ruleUUIDs": {
        "items": {"description": "registration rule UUID id", "type": "string"},
        "type": "array",
    },
    "selectiveQinq_createSelectiveQinq": {
        "additionalProperties": False,
        "properties": {
            "cvlan": {
                "description": "Customer "
                "vlan(cVlan). "
                "It "
                "could "
                "be "
                "range "
                "of "
                "value, "
                "single "
                "value, "
                "or "
                "empty "
                "string "
                "for "
                "untagged. "
                "such "
                "like "
                "2,3,5-10",
                "type": "string",
            },
            "newCvlan": {
                "description": "Replacement " "CVLAN(newCVlan)",
                "type": "string",
            },
            "port": {"description": "Selective " "QinQ " "Port", "type": "string"},
            "svlan": {"description": "Service " "vlan(sVlan)", "type": "string"},
            "switchId": {"description": "Switch " "Id", "type": "string"},
        },
        "type": "object",
    },
    "selectiveQinq_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "selectiveQinq_selectiveQinq": {
        "additionalProperties": False,
        "properties": {
            "cvlan": {"type": "string"},
            "id": {"type": "string"},
            "newCvlan": {"type": "string"},
            "port": {"type": "string"},
            "svlan": {"type": "string"},
            "switchId": {"type": "string"},
        },
        "type": "object",
    },
    "selectiveQinq_selectiveQinqQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "Selective "
                "QinQ "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "Selective "
                "QinQ "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "Selective "
                "QinQ "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/selectiveQinq_selectiveQinq"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "Selective " "QinQ " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total "
                "Selective "
                "QinQ "
                "count "
                "in "
                "this "
                "response",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "selectiveQinq_updateSelectiveQinq": {
        "additionalProperties": False,
        "properties": {
            "cvlan": {
                "description": "Customer "
                "vlan(cVlan). "
                "Only "
                "accepts "
                "one "
                "vlan "
                "Id or "
                "empty "
                "for "
                "untagged",
                "type": "string",
            },
            "newCvlan": {
                "description": "Replacement " "CVLAN(newCVlan)",
                "type": "string",
            },
            "port": {"description": "Selective " "QinQ " "Port", "type": "string"},
            "svlan": {"description": "Service " "vlan(sVlan)", "type": "string"},
            "switchId": {"description": "Switch " "Id", "type": "string"},
        },
        "type": "object",
    },
    "selfGenerateTraffic_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "selfGenerateTraffic_saveSelfGenerateTraffic": {
        "additionalProperties": False,
        "properties": {
            "dscpMarking": {"description": "DSCP " "Marking", "type": "string"},
            "priorityMarking": {"description": "Priority " "Marking", "type": "string"},
            "sgtType": {
                "description": "Self " "Generate " "Traffic " "Type",
                "enum": [
                    "DNS",
                    "ICMP",
                    "NTP",
                    "RADIUS",
                    "SNMP",
                    "SNMP_TRAP",
                    "SSH",
                    "SYSLOG",
                    "TELNET",
                    "TFTP",
                ],
                "type": "string",
            },
            "switchId": {"description": "Switch " "Id", "type": "string"},
        },
        "type": "object",
    },
    "selfGenerateTraffic_selfGenerateTraffic": {
        "additionalProperties": False,
        "properties": {
            "dscpMarking": {"description": "DSCP " "Marking", "type": "string"},
            "id": {
                "description": "Self " "Generate " "Traffic " "Id",
                "type": "string",
            },
            "priorityMarking": {"description": "Priority " "Marking", "type": "string"},
            "sgtType": {
                "description": "Self " "Generate " "Traffic " "Type",
                "enum": [
                    "DNS",
                    "ICMP",
                    "NTP",
                    "RADIUS",
                    "SNMP",
                    "SNMP_TRAP",
                    "SSH",
                    "SYSLOG",
                    "TELNET",
                    "TFTP",
                ],
                "type": "string",
            },
            "switchId": {"description": "Switch " "Id", "type": "string"},
        },
        "type": "object",
    },
    "selfGenerateTraffic_selfGenerateTrafficQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {"type": "object"},
            "firstIndex": {"type": "integer"},
            "hasMore": {"type": "boolean"},
            "list": {
                "items": {
                    "$ref": "#/definitions/selfGenerateTraffic_selfGenerateTraffic"
                },
                "type": "array",
            },
            "rawDataTotalCount": {"type": "integer"},
            "totalCount": {"type": "integer"},
        },
        "type": "object",
    },
    "specificSettings_DHCPOption": {
        "additionalProperties": False,
        "properties": {
            "seq": {"description": "Seq of Option", "type": "integer"},
            "type": {"description": "Type of " "Option", "type": "string"},
            "value": {"description": "Value of " "Option", "type": "string"},
        },
        "type": "object",
    },
    "specificSettings_DHCPServer": {
        "additionalProperties": False,
        "properties": {
            "defaultRouterIp": {
                "description": "Default " "Router " "Ip",
                "type": "string",
            },
            "dhcpOptions": {
                "items": {"$ref": "#/definitions/specificSettings_DHCPOption"},
                "type": "array",
            },
            "excludedEnd": {
                "description": "Excluded " "range " "end",
                "type": "string",
            },
            "excludedStart": {
                "description": "Excluded " "range " "start",
                "type": "string",
            },
            "leaseDays": {"description": "Lease " "Days", "type": "integer"},
            "leaseHrs": {"description": "Lease " "Hours", "type": "integer"},
            "leaseMins": {"description": "Lease " "Mins", "type": "integer"},
            "network": {"description": "Network/Mask", "type": "string"},
            "poolName": {"description": "Pool Name", "type": "string"},
        },
        "type": "object",
    },
    "specificSettings_SpecificSettings": {
        "additionalProperties": False,
        "properties": {
            "aclOnCpu": {"description": "ACL " "on " "CPU", "type": "string"},
            "altoId": {"description": "Alto " "Id", "type": "string"},
            "bootFlash": {
                "description": "Boot " "Flash",
                "enum": ["DEFAULT", "PRIMARY", "SECONDARY"],
                "type": "string",
            },
            "createdTime": {
                "description": "The "
                "create "
                "time "
                "of "
                "the "
                "Specific "
                "Settings",
                "type": "integer",
            },
            "defaultGateway": {"description": "DefaultGateway", "type": "string"},
            "dhcpServerEnabled": {
                "description": "DHCP " "server " "enabled",
                "type": "boolean",
            },
            "dhcpServers": {
                "items": {"$ref": "#/definitions/specificSettings_DHCPServer"},
                "type": "array",
            },
            "hostname": {"description": "Hostname", "type": "string"},
            "id": {"description": "Id", "type": "string"},
            "igmpSnooping": {"description": "IGMP " "snopping", "type": "string"},
            "ipAddress": {"description": "IP " "Address", "type": "string"},
            "ipAddressType": {
                "description": "IP " "Address " "Type",
                "enum": ["STATIC", "DYNAMIC"],
                "type": "string",
            },
            "jumboMode": {"description": "JumboMode", "type": "boolean"},
            "subnetMask": {"description": "SubnetMask", "type": "string"},
            "updatedTime": {
                "description": "The "
                "modify "
                "time "
                "of "
                "the "
                "Specific "
                "Settings",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "specificSettings_UpdateSpecificSettings": {
        "additionalProperties": False,
        "properties": {
            "aclOnCpu": {"description": "ACL " "on " "CPU", "type": "string"},
            "altoId": {"description": "Alto " "Id", "type": "string"},
            "arpInspectionTrustPort": {
                "description": "ARP " "Inspection " "Trust " "Port",
                "type": "string",
            },
            "bootFlash": {
                "description": "Boot " "flash",
                "enum": ["DEFAULT", "PRIMARY", "SECONDARY"],
                "type": "string",
            },
            "defaultGateway": {"description": "DefaultGateway", "type": "string"},
            "dhcpServerEnabled": {
                "description": "DHCP " "server " "enabled",
                "type": "boolean",
            },
            "dhcpServers": {
                "items": {"$ref": "#/definitions/specificSettings_DHCPServer"},
                "type": "array",
            },
            "hostname": {"description": "Hostname", "type": "string"},
            "igmpSnooping": {"description": "IGMP " "snopping", "type": "string"},
            "ipAddress": {"description": "IP " "Address", "type": "string"},
            "ipAddressType": {
                "description": "IP " "Address " "Type",
                "enum": ["STATIC", "DYNAMIC"],
                "type": "string",
            },
            "ipv4DhcpSnoopingTrustPort": {
                "description": "DHCP " "Snooping " "Trust " "Port",
                "type": "string",
            },
            "jumboMode": {"description": "JumboMode", "type": "boolean"},
            "subnetMask": {"description": "SubnetMask", "type": "string"},
        },
        "type": "object",
    },
    "specificSettings_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "specificSettings_idList": {
        "additionalProperties": False,
        "properties": {
            "hostname": {"description": "Hostname", "type": "string"},
            "id": {"description": "Id", "type": "string"},
        },
        "type": "object",
    },
    "specificSettings_specificSettingsAllResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "Specific "
                "Settings "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "Specific "
                "Settings "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "Specific "
                "Settings "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/specificSettings_idList"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "Specific " "Settings " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total "
                "Specific "
                "Settings "
                "count "
                "in "
                "this "
                "response",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "stack_auditIdList": {
        "additionalProperties": False,
        "properties": {
            "extra": {"type": "object"},
            "firstIndex": {"type": "integer"},
            "hasMore": {"type": "boolean"},
            "list": {
                "items": {"$ref": "#/definitions/switch_auditId"},
                "type": "array",
            },
            "rawDataTotalCount": {"type": "integer"},
            "totalCount": {"type": "integer"},
        },
        "type": "object",
    },
    "stack_list": {
        "additionalProperties": False,
        "properties": {
            "firstIndex": {
                "description": "Index of the first stack "
                "returned out of the "
                "complete stack list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator of whether there "
                "are more stack after the "
                "current displayed list",
                "type": "boolean",
            },
            "list": {
                "description": "List of stack",
                "items": {"$ref": "#/definitions/stack_member"},
                "type": "array",
            },
            "rawDataTotalCount": {"description": "Stack count", "type": "integer"},
            "totalCount": {"description": "Total Stack count", "type": "integer"},
        },
        "type": "object",
    },
    "stack_member": {
        "additionalProperties": False,
        "properties": {
            "activeMode": {"description": "Role of stack", "type": "string"},
            "model": {"description": "Switch model of stack", "type": "string"},
            "poe": {
                "additionalProperties": False,
                "description": "Information of PoE",
                "properties": {
                    "free": {
                        "description": "Free "
                        "power "
                        "capacity "
                        "of a "
                        "switch "
                        "unit "
                        "in "
                        "stack",
                        "type": "integer",
                    },
                    "percent": {
                        "description": "Percentage "
                        "of "
                        "power "
                        "usage "
                        "for "
                        "a "
                        "switch "
                        "unit "
                        "in "
                        "stack",
                        "type": "number",
                    },
                    "total": {
                        "description": "Total "
                        "power "
                        "capacity "
                        "of a "
                        "switch "
                        "unit "
                        "in "
                        "stack",
                        "type": "integer",
                    },
                },
                "type": "object",
            },
            "portStatus": {
                "additionalProperties": False,
                "description": "Port status " "Information",
                "properties": {
                    "adminDown": {
                        "description": "Count "
                        "for "
                        "port "
                        "status "
                        "is "
                        "admin "
                        "down "
                        "of "
                        "stack",
                        "type": "integer",
                    },
                    "down": {
                        "description": "Count "
                        "for "
                        "port "
                        "status "
                        "is "
                        "down "
                        "of "
                        "stack",
                        "type": "integer",
                    },
                    "speed": {
                        "description": "Port " "speed " "of " "stack",
                        "type": "string",
                    },
                    "total": {
                        "description": "Total " "port " "count " "of " "stack",
                        "type": "integer",
                    },
                    "up": {
                        "description": "Count "
                        "for "
                        "port "
                        "status "
                        "is "
                        "up "
                        "of "
                        "stack",
                        "type": "integer",
                    },
                    "warning": {
                        "description": "Count "
                        "for "
                        "port "
                        "status "
                        "is "
                        "warring "
                        "of "
                        "stack",
                        "type": "integer",
                    },
                },
                "type": "object",
            },
            "ports": {"description": "Port count  of stack", "type": "integer"},
            "serialNumber": {
                "description": "Serial number of " "stack",
                "type": "string",
            },
            "switchModule": {
                "description": "Switch module of " "stack",
                "type": "string",
            },
            "switchName": {"description": "Switch name of stack", "type": "string"},
            "switchPorts": {
                "description": "Switch port " "information of stack",
                "items": {
                    "additionalProperties": False,
                    "properties": {
                        "adminStatus": {
                            "description": "Admin " "Status " "of " "switch " "port",
                            "type": "string",
                        },
                        "connectedDevice": {
                            "additionalProperties": False,
                            "description": "Connected " "device " "information",
                            "properties": {
                                "domainId": {
                                    "description": "Identifier "
                                    "of "
                                    "the "
                                    "management "
                                    "domain "
                                    "to "
                                    "which "
                                    "the "
                                    "connected "
                                    "device "
                                    "belong",
                                    "type": "string",
                                },
                                "id": {
                                    "description": "Identifier "
                                    "of "
                                    "switch "
                                    "port "
                                    "connected "
                                    "device",
                                    "type": "string",
                                },
                                "isRuckusAP": {
                                    "description": "Connected "
                                    "devices "
                                    "is "
                                    "RuckusAP,True "
                                    "or "
                                    "False",
                                    "type": "string",
                                },
                                "localPort": {
                                    "description": "Local "
                                    "port "
                                    "description "
                                    "of "
                                    "connected "
                                    "device",
                                    "type": "string",
                                },
                                "localPortIfaceName": {
                                    "description": "Local " "port " "interface " "name",
                                    "type": "string",
                                },
                                "localPortMac": {
                                    "description": "Local "
                                    "port "
                                    "mac "
                                    "address "
                                    "of "
                                    "connected "
                                    "device",
                                    "type": "string",
                                },
                                "remoteDeviceName": {
                                    "description": "Remote "
                                    "device "
                                    "name "
                                    "of "
                                    "connected "
                                    "device",
                                    "type": "string",
                                },
                                "remotePort": {
                                    "description": "Remote "
                                    "port "
                                    "number "
                                    "of "
                                    "connected "
                                    "device",
                                    "type": "string",
                                },
                                "remotePortDesc": {
                                    "description": "Remote "
                                    "port "
                                    "description "
                                    "of "
                                    "connected "
                                    "device",
                                    "type": "string",
                                },
                                "remotePortMac": {
                                    "description": "Remote "
                                    "port "
                                    "mac "
                                    "address "
                                    "of "
                                    "connected "
                                    "device",
                                    "type": "string",
                                },
                                "remotePortType": {
                                    "description": "Remote "
                                    "port "
                                    "type "
                                    "of "
                                    "connected "
                                    "device",
                                    "type": "string",
                                },
                                "switchGroup": {
                                    "description": "Switch " "group",
                                    "type": "string",
                                },
                                "switchGroupLevelOneId": {
                                    "description": "Switch "
                                    "group "
                                    "level "
                                    "one "
                                    "Id",
                                    "type": "string",
                                },
                                "switchGroupLevelTwoId": {
                                    "description": "Switch "
                                    "group "
                                    "level "
                                    "two "
                                    "Id",
                                    "type": "string",
                                },
                                "switchId": {
                                    "description": "Switch " "Id",
                                    "type": "string",
                                },
                                "switchName": {
                                    "description": "Switch " "name",
                                    "type": "string",
                                },
                                "tenantId": {
                                    "description": "Tenant " "Id " "of " "stack",
                                    "type": "string",
                                },
                                "unitId": {
                                    "description": "Unit " "Id",
                                    "type": "string",
                                },
                            },
                            "type": "object",
                        },
                        "id": {
                            "description": "Identifier " "of " "switch " "port",
                            "type": "string",
                        },
                        "inUtilization": {
                            "description": "In " "utilization " "of " "switch " "port",
                            "type": "number",
                        },
                        "lagName": {
                            "description": "LAG " "name " "of " "switch " "port",
                            "type": "string",
                        },
                        "mac": {
                            "description": "Mac " "address " "of " "switch " "port",
                            "type": "string",
                        },
                        "name": {
                            "description": "Name " "of " "switch " "port",
                            "type": "string",
                        },
                        "neighborName": {
                            "description": "Neighbor " "name " "of " "switch " "port",
                            "type": "string",
                        },
                        "opticsType": {
                            "description": "Optics " "type " "of " "switch " "port",
                            "type": "string",
                        },
                        "outUtilization": {
                            "description": "Out " "utilization " "of " "switch " "port",
                            "type": "number",
                        },
                        "poe": {
                            "additionalProperties": False,
                            "description": "PoE " "information " "of " "switch " "port",
                            "properties": {
                                "free": {
                                    "description": "Free "
                                    "power "
                                    "capacity "
                                    "of "
                                    "switch "
                                    "port",
                                    "type": "integer",
                                },
                                "percent": {
                                    "description": "Power "
                                    "used "
                                    "percentage "
                                    "of "
                                    "switch "
                                    "port",
                                    "type": "number",
                                },
                                "total": {
                                    "description": "Total "
                                    "power "
                                    "capacity "
                                    "of "
                                    "switch "
                                    "port",
                                    "type": "integer",
                                },
                            },
                            "type": "object",
                        },
                        "poeEnabled": {
                            "description": "PoE " "Enabled, " "True " "or " "False",
                            "type": "boolean",
                        },
                        "portIdentifier": {
                            "description": "Port " "Identifier " "of " "switch " "port",
                            "type": "string",
                        },
                        "portSpeed": {
                            "description": "Port " "speed " "of " "switch " "port",
                            "type": "string",
                        },
                        "sampledInstant": {
                            "description": "Sampled " "instant " "of " "switch " "port",
                            "type": "string",
                        },
                        "status": {
                            "description": "Status " "of " "switch " "port",
                            "type": "string",
                        },
                        "stpState": {
                            "description": "STP " "state " "of " "switch " "port",
                            "type": "integer",
                        },
                        "switchGroup": {
                            "description": "Switch " "group " "of " "switch " "port",
                            "type": "string",
                        },
                        "switchName": {
                            "description": "Switch " "name " "of " "stack",
                            "type": "string",
                        },
                        "trafficUsage": {
                            "additionalProperties": False,
                            "description": "Traffic " "usage " "information",
                            "properties": {
                                "rx": {
                                    "description": "Rx "
                                    "traffic "
                                    "usage "
                                    "of "
                                    "switch "
                                    "port",
                                    "type": "integer",
                                },
                                "tx": {
                                    "description": "Tx "
                                    "traffic "
                                    "usage "
                                    "of "
                                    "switch "
                                    "port",
                                    "type": "integer",
                                },
                            },
                            "type": "object",
                        },
                        "type": {
                            "description": "Type " "of " "switch " "port",
                            "type": "string",
                        },
                        "unTaggedVlan": {
                            "description": "Untagged " "vlan " "of " "switch " "port",
                            "type": "string",
                        },
                        "usedInFormingStack": {
                            "description": "Used "
                            "in "
                            "forming "
                            "stack, "
                            "True "
                            "or "
                            "False",
                            "type": "boolean",
                        },
                        "vlans": {
                            "description": "Switch " "port " "include " "vlans",
                            "type": "string",
                        },
                    },
                    "type": "object",
                },
                "type": "array",
            },
            "switchUnit": {"description": "Switch unit of stack", "type": "string"},
            "switchUnitState": {
                "description": "Switch unit state " "of stack",
                "type": "string",
            },
        },
        "type": "object",
    },
    "stack_stackConfig": {
        "additionalProperties": False,
        "properties": {
            "activeSwitchId": {
                "description": "Switch Id of " "Active Unit",
                "type": "string",
            },
            "isActiveRole": {
                "description": "Switch role is "
                "Active, True "
                "(Active) or "
                "False (Standby "
                "or Member)",
                "type": "boolean",
            },
            "suggestedId": {
                "description": "Suggested switch " "unit Id in " "stack, 1 ~ 12",
                "type": "integer",
            },
            "switchId": {"description": "Switch Id", "type": "string"},
        },
        "type": "object",
    },
    "stack_stackConfigList": {
        "items": {"$ref": "#/definitions/stack_stackConfig"},
        "type": "array",
    },
    "staticRoute_createStaticRoute": {
        "additionalProperties": False,
        "properties": {
            "adminDistance": {"description": "Admin " "Distance", "type": "integer"},
            "altoId": {"description": "Audit Id", "type": "string"},
            "destinationIp": {"description": "Destination " "IP", "type": "string"},
            "familyId": {"description": "Family " "Id", "type": "string"},
            "groupId": {"description": "Switch " "Group Id", "type": "string"},
            "nextHop": {"description": "Next Hop", "type": "string"},
            "pushTime": {
                "description": "Puch " "Schedule " "Time",
                "format": "int64",
                "type": "integer",
            },
            "pushTimeType": {
                "description": "Puch " "Config " "Type",
                "enum": ["NOW", "SCHEDULE"],
                "type": "string",
            },
            "switchId": {"description": "Switch " "Id", "type": "string"},
        },
        "type": "object",
    },
    "staticRoute_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "staticRoute_staticRoute": {
        "additionalProperties": False,
        "properties": {
            "adminDistance": {"description": "Admin " "Distance", "type": "string"},
            "altoId": {"description": "Audit Id", "type": "string"},
            "createdTime": {
                "description": "The create " "time of " "the Static " "Route",
                "format": "int64",
                "type": "integer",
            },
            "destinationIp": {"description": "Destination " "IP", "type": "string"},
            "familyId": {"description": "Family Id", "type": "string"},
            "groupId": {"description": "Switch Group " "Id", "type": "string"},
            "id": {"description": "Static Route Id", "type": "string"},
            "nextHop": {"description": "Next Hop", "type": "string"},
            "pushTime": {
                "description": "Puch Schedule " "Time",
                "format": "int64",
                "type": "integer",
            },
            "pushTimeType": {
                "description": "Puch " "Config " "Type",
                "enum": ["NOW", "SCHEDULE"],
                "type": "string",
            },
            "switchId": {"description": "Switch Id", "type": "string"},
            "updatedTime": {
                "description": "The modify " "time of " "the Static " "Route",
                "format": "int64",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "staticRoute_staticRoutesQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "Static "
                "Route "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "Static "
                "Route "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "Static "
                "Routes "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/staticRoute_staticRoute"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "Static " "Route " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total "
                "Static "
                "Route "
                "Servers "
                "count "
                "in "
                "this "
                "response",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "staticRoute_updateStaticRoute": {
        "additionalProperties": False,
        "properties": {
            "adminDistance": {"description": "Admin " "Distance", "type": "integer"},
            "altoId": {"description": "Audit Id", "type": "string"},
            "destinationIp": {"description": "Destination " "IP", "type": "string"},
            "nextHop": {"description": "Next Hop", "type": "string"},
            "pushTime": {
                "description": "Puch " "Schedule " "Time",
                "format": "int64",
                "type": "integer",
            },
            "pushTimeType": {
                "description": "Puch " "Config " "Type",
                "enum": ["NOW", "SCHEDULE"],
                "type": "string",
            },
        },
        "type": "object",
    },
    "switchClientVisibility_client": {
        "additionalProperties": False,
        "properties": {
            "clientAuthType": {"type": "string"},
            "clientDesc": {"type": "string"},
            "clientIpv4Addr": {"type": "string"},
            "clientIpv6Addr": {"type": "string"},
            "clientMac": {"type": "string"},
            "clientStatus": {"type": "string"},
            "clientType": {"type": "string"},
            "clientUserName": {"type": "string"},
            "clientVlan": {"type": "string"},
            "clientVni": {"type": "string"},
            "dot1XIpv4Addr": {"type": "string"},
            "dot1XIpv6Addr": {"type": "string"},
            "pastAuthHistory": {"type": "string"},
            "switchName": {"type": "string"},
            "switchPort": {"type": "string"},
            "updatedTime": {"type": "string"},
        },
        "type": "object",
    },
    "switchClientVisibility_list": {
        "additionalProperties": False,
        "properties": {
            "firstIndex": {"type": "integer"},
            "hasMore": {"type": "boolean"},
            "list": {
                "items": {"$ref": "#/definitions/switchClientVisibility_client"},
                "type": "array",
            },
            "rawDataTotalCount": {"type": "integer"},
            "totalCount": {"type": "integer"},
        },
        "type": "object",
    },
    "switchClientVisibility_status": {
        "additionalProperties": False,
        "properties": {
            "flaggedCount": {
                "description": "Flagged " "status " "count",
                "type": "integer",
            },
            "offlineCount": {
                "description": "Offline " "status " "count",
                "type": "integer",
            },
            "onlineCount": {
                "description": "Online " "status " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "switchModel_modelList": {
        "additionalProperties": False,
        "properties": {"model": {"description": "Switch Model", "type": "string"}},
        "type": "object",
    },
    "switchModel_result": {
        "additionalProperties": False,
        "properties": {
            "extra": {"description": "Extra field", "type": "object"},
            "firstIndex": {
                "description": "The first data " "index for " "current reulst",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator of " "remaining data",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/switchModel_modelList"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "Data " "Count",
                "type": "integer",
            },
            "totalCount": {"description": "Total Data Count", "type": "integer"},
        },
        "type": "object",
    },
    "switch_auditId": {
        "additionalProperties": False,
        "properties": {
            "id": {"description": "Audit Id", "type": "string"},
            "name": {"description": "Audit name", "type": "string"},
        },
        "type": "object",
    },
    "switch_barChart": {
        "additionalProperties": False,
        "properties": {
            "id": {"description": "Identifier of the barchart", "type": "string"},
            "key": {"description": "Key of the barchart", "type": "string"},
            "value": {"description": "Metrics of the barchart", "type": "number"},
        },
        "type": "object",
    },
    "switch_batchPreProvision": {
        "additionalProperties": False,
        "properties": {
            "domainId": {
                "description": "The id of "
                "the domain "
                "for batch "
                "preprovisioning "
                "the "
                "NetworkSwitch",
                "type": "string",
            }
        },
        "type": "object",
    },
    "switch_connectedAPsQueryList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of the "
                "first "
                "switch "
                "connected "
                "AP "
                "returned "
                "out of "
                "the "
                "complete "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there are "
                "more "
                "switch "
                "connected "
                "AP after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/switch_connectedDevice"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Connected " "AP " "list " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "connected " "AP " "list " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "switch_connectedDevice": {
        "additionalProperties": False,
        "properties": {
            "domainId": {
                "description": "Identifier of "
                "the management "
                "domain to "
                "which the "
                "connected "
                "device belong",
                "type": "string",
            },
            "id": {
                "description": "Identifier of " "connected device",
                "type": "string",
            },
            "isRuckusAP": {
                "description": "Remote "
                "connected "
                "device is "
                "Ruckus AP, "
                "True or "
                "False.",
                "type": "string",
            },
            "localPort": {
                "description": "Local port " "which connect " "to remote " "device",
                "type": "string",
            },
            "localPortIfaceName": {
                "description": "Local " "port " "interface " "name",
                "type": "string",
            },
            "localPortMac": {
                "description": "Local port " "mac " "address",
                "type": "string",
            },
            "remoteDeviceMac": {"type": "string"},
            "remoteDeviceName": {
                "description": "Remote " "connected " "device " "name",
                "type": "string",
            },
            "remotePort": {
                "description": "Remote "
                "device port "
                "which "
                "connected to "
                "local device",
                "type": "string",
            },
            "remotePortDesc": {
                "description": "Remote " "connected " "device " "port " "description",
                "type": "string",
            },
            "remotePortMac": {
                "description": "Remote " "connected " "device " "port mac " "address",
                "type": "string",
            },
            "remotePortType": {
                "description": "Remote " "connected " "device " "port " "type",
                "type": "string",
            },
            "sampledInstant": {"description": "Sampled " "instant", "type": "object"},
            "switchGroup": {"description": "Switch " "group", "type": "string"},
            "switchGroupLevelOneId": {
                "description": "Switch " "group " "level " "one " "Id",
                "type": "string",
            },
            "switchGroupLevelTwoId": {
                "description": "Switch " "group " "level " "two " "Id",
                "type": "string",
            },
            "switchId": {"description": "Switch Id", "type": "string"},
            "switchName": {"description": "Switch name", "type": "string"},
            "tenantId": {"description": "Tenant Id", "type": "string"},
            "unitId": {"description": "Unit Id", "type": "string"},
        },
        "type": "object",
    },
    "switch_connectedDevicesQueryList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "switch "
                "connected "
                "devices "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "switch "
                "connected "
                "devices "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/switch_connectedDevice"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Connected " "devices " "list " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "connected " "devices " "list " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "switch_deleteSwitchesResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "delete "
                "switches "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "delete "
                "switches "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/switch_auditId"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Delete " "switches " "list " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "delete " "switches " "list " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "switch_firmware": {
        "additionalProperties": False,
        "properties": {
            "fromVersion": {
                "description": "Original fireware " "version before " "firmware update",
                "type": "string",
            },
            "timestamp": {
                "description": "Timestamp of " "fireware update",
                "type": "number",
            },
            "toVersion": {
                "description": "Firmware version " "after firmware " "update",
                "type": "string",
            },
        },
        "type": "object",
    },
    "switch_firmwareHistoryQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "firmware "
                "history "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "query "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "firmware "
                "history "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/switch_firmware"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Firmware " "history " "list " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "firmware " "history " "list " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "switch_networkSwitch": {
        "additionalProperties": False,
        "properties": {
            "alarm": {"description": "Count of switch " "alarm", "type": "integer"},
            "backupDiffWithMaster": {
                "description": "Indicate "
                "there "
                "is a "
                "config "
                "backup "
                "different "
                "from "
                "the "
                "master "
                "backup",
                "type": "boolean",
            },
            "bgpEvpnRole": {
                "description": "Switch BGP " "eVPN role",
                "enum": ["BGP_EVPN_SERVER", "BGP_EVPN_CLIENT"],
                "type": "string",
            },
            "defaultGateway": {
                "description": "Default " "gateway of " "switch",
                "type": "string",
            },
            "domainId": {
                "description": "Identifier of "
                "the management "
                "domain to which "
                "the switch "
                "belong",
                "type": "string",
            },
            "family": {"description": "Switch Model " "Family", "type": "string"},
            "firmwareUpdate": {
                "additionalProperties": False,
                "description": "Information " "of " "firmware " "update",
                "properties": {
                    "modifiedTime": {
                        "description": "Modified "
                        "time "
                        "of "
                        "the "
                        "firmware "
                        "update "
                        "scheduled",
                        "type": "string",
                    },
                    "scheduleId": {
                        "description": "Schedule " "Id " "of " "firmware " "update",
                        "type": "string",
                    },
                    "scheduledTime": {
                        "description": "Scheduled " "time " "of " "firmware " "update",
                        "type": "string",
                    },
                    "status": {
                        "description": "Status " "of " "firmware " "update",
                        "type": "string",
                    },
                    "toVersion": {
                        "description": "Update " "to " "which " "firmware " "version",
                        "type": "string",
                    },
                },
                "type": "object",
            },
            "firmwareVersion": {
                "description": "Switch " "firmware " "version",
                "type": "string",
            },
            "groupConfigMode": {
                "description": "Config " "mode of " "switch " "group",
                "type": "string",
            },
            "groupFirmware": {
                "description": "Firmware of " "switch " "group",
                "type": "string",
            },
            "groupId": {
                "description": "Identifier of " "switch group",
                "type": "string",
            },
            "groupName": {"description": "Name of switch " "group", "type": "string"},
            "id": {"description": "Identifier of switch", "type": "string"},
            "ipAddress": {"description": "switch IP " "address", "type": "string"},
            "ipAddressType": {"description": "IP address " "type", "type": "string"},
            "isInNetworkSegmentation": {
                "description": "Indicate "
                "the "
                "switch "
                "is "
                "used "
                "for "
                "Network "
                "Segmentation",
                "type": "boolean",
            },
            "lastBackupStatus": {
                "description": "Last " "config " "backup " "status " "of " "switch",
                "enum": ["STARTED", "SUCCESS", "FAILED"],
                "type": "string",
            },
            "lastBackupTime": {
                "description": "Last " "config " "backup " "time of " "switch",
                "format": "int64",
                "type": "integer",
            },
            "lastRestoreStatus": {
                "description": "Last " "config " "restore " "status " "of " "switch",
                "enum": ["STARTED", "SUCCESS", "FAILED"],
                "type": "string",
            },
            "lastRestoreTime": {
                "description": "Last " "config " "restore " "time of " "switch",
                "format": "int64",
                "type": "integer",
            },
            "localsyncStatus": {
                "description": "Status of " "LocalSync",
                "enum": ["LOCAL_SYNC_NONE", "LOCAL_SYNCING"],
                "type": "string",
            },
            "macAddress": {"description": "Switch mac " "address", "type": "string"},
            "model": {"description": "Switch model", "type": "string"},
            "modules": {"description": "Stack or Switch", "type": "string"},
            "numOfUnits": {"description": "Count of " "switch unit", "type": "integer"},
            "parentGroupId": {
                "description": "Identifier " "of parent " "switch " "group",
                "type": "string",
            },
            "poe": {
                "additionalProperties": False,
                "description": "Information of PoE",
                "properties": {
                    "free": {
                        "description": "Free " "power " "capacity " "of " "a " "switch",
                        "type": "integer",
                    },
                    "percent": {
                        "description": "Percentage "
                        "of "
                        "power "
                        "usage "
                        "for "
                        "a "
                        "switch",
                        "type": "number",
                    },
                    "total": {
                        "description": "Total "
                        "power "
                        "capacity "
                        "of "
                        "a "
                        "switch",
                        "type": "integer",
                    },
                },
                "type": "object",
            },
            "portStatus": {
                "additionalProperties": False,
                "description": "Information of " "port status",
                "properties": {
                    "adminDown": {
                        "description": "Count "
                        "for "
                        "port "
                        "status "
                        "is "
                        "admin "
                        "down "
                        "of "
                        "switch",
                        "type": "integer",
                    },
                    "down": {
                        "description": "Count "
                        "for "
                        "port "
                        "status "
                        "is "
                        "down "
                        "of "
                        "switch",
                        "type": "integer",
                    },
                    "speed": {
                        "description": "Port " "speed " "of " "switch",
                        "type": "string",
                    },
                    "speedInt": {
                        "description": "Switch " "port " "fully " "speed",
                        "type": "integer",
                    },
                    "total": {
                        "description": "Total "
                        "count "
                        "for "
                        "port "
                        "status "
                        "of "
                        "switch",
                        "type": "integer",
                    },
                    "up": {
                        "description": "Count "
                        "for "
                        "port "
                        "status "
                        "is "
                        "up "
                        "of "
                        "switch",
                        "type": "integer",
                    },
                    "warning": {
                        "description": "Count "
                        "for "
                        "port "
                        "status "
                        "is "
                        "warring "
                        "of "
                        "switch",
                        "type": "integer",
                    },
                },
                "type": "object",
            },
            "ports": {"description": "Total port count", "type": "integer"},
            "registrationStatus": {
                "description": "Status " "for " "switch " "registater " "to " "ICX-M",
                "type": "string",
            },
            "serialNumber": {
                "description": "Switch " "serial " "number",
                "type": "string",
            },
            "siteActive": {
                "description": "Data Plane Ip, " "for Network " "Segmentation",
                "type": "string",
            },
            "siteConnection": {
                "description": "Data Plane "
                "Connection "
                "status, "
                "for "
                "Network "
                "Segmentation",
                "type": "string",
            },
            "stackId": {"description": "Stack Id", "type": "string"},
            "status": {
                "description": "Status of switch, " "Ex: ONLINE, " "OFFLINE",
                "type": "string",
            },
            "supportedCsl": {
                "description": "Supported " "CSL of " "switch",
                "format": "int32",
                "type": "integer",
            },
            "switchName": {"description": "Switch name", "type": "string"},
            "upTime": {"description": "SWitch uptime", "type": "string"},
        },
        "type": "object",
    },
    "switch_portDetails": {
        "additionalProperties": False,
        "properties": {
            "adminStatus": {
                "description": "Admin status of " "switch port, UP " "or DOWN",
                "type": "string",
            },
            "connectedDevice": {
                "additionalProperties": False,
                "description": "Connected " "device " "information",
                "properties": {
                    "domainId": {
                        "description": "Identifier "
                        "of "
                        "the "
                        "management "
                        "domain "
                        "to "
                        "which "
                        "the "
                        "connected "
                        "device "
                        "belong",
                        "type": "string",
                    },
                    "id": {
                        "description": "Identifier " "of " "connected " "device",
                        "type": "string",
                    },
                    "isRuckusAP": {
                        "description": "Connected "
                        "devices "
                        "is "
                        "RuckusAP,True "
                        "or "
                        "False",
                        "type": "string",
                    },
                    "localPort": {
                        "description": "Local "
                        "port "
                        "description "
                        "to "
                        "connected "
                        "device",
                        "type": "string",
                    },
                    "localPortIfaceName": {
                        "description": "Local " "port " "interface " "name",
                        "type": "string",
                    },
                    "localPortMac": {
                        "description": "Local "
                        "port "
                        "mac "
                        "address "
                        "to "
                        "connected "
                        "device",
                        "type": "string",
                    },
                    "remoteDeviceMac": {"type": "string"},
                    "remoteDeviceName": {
                        "description": "Remote " "connected " "device " "name",
                        "type": "string",
                    },
                    "remotePort": {
                        "description": "Remote "
                        "port "
                        "number "
                        "of "
                        "connected "
                        "device",
                        "type": "string",
                    },
                    "remotePortDesc": {
                        "description": "Remote "
                        "port "
                        "description "
                        "of "
                        "connected "
                        "device",
                        "type": "string",
                    },
                    "remotePortMac": {
                        "description": "Remote "
                        "port "
                        "mac "
                        "address "
                        "of "
                        "local "
                        "device",
                        "type": "string",
                    },
                    "remotePortType": {
                        "description": "Remote "
                        "port "
                        "type "
                        "of "
                        "connected "
                        "device",
                        "type": "string",
                    },
                    "switchGroup": {"description": "Switch " "group", "type": "string"},
                    "switchGroupLevelOneId": {
                        "description": "Switch " "group " "level " "one " "Id",
                        "type": "string",
                    },
                    "switchGroupLevelTwoId": {
                        "description": "Switch " "group " "level " "two " "Id",
                        "type": "string",
                    },
                    "switchId": {"description": "Switch " "Id", "type": "string"},
                    "switchName": {"description": "Switch " "name", "type": "string"},
                    "tenantId": {"description": "Tenant " "Id", "type": "string"},
                    "unitId": {"description": "Unit " "Id", "type": "string"},
                },
                "type": "object",
            },
            "defaultVlanId": {"description": "Default VLAN " "ID", "type": "integer"},
            "id": {"description": "Identifier of switch " "port", "type": "string"},
            "inUtilization": {
                "description": "Switch port " "traffic in " "utilization",
                "type": "number",
            },
            "lagConfig": {
                "additionalProperties": False,
                "description": "Lag config of " "switch port",
                "properties": {
                    "lagAdminStatus": {
                        "description": "Lag " "admin " "status " "of " "switch " "port",
                        "type": "string",
                    },
                    "lagId": {
                        "description": "Lag " "id " "of " "switch " "port",
                        "type": "integer",
                    },
                    "lagName": {
                        "description": "Lag " "name " "of " "switch " "port",
                        "type": "string",
                    },
                    "lagStatus": {
                        "description": "Lag " "status " "of " "switch " "port",
                        "type": "string",
                    },
                },
                "type": "object",
            },
            "mac": {"description": "Mac address of switch " "port", "type": "string"},
            "name": {"description": "Name of switch port", "type": "string"},
            "neighborName": {
                "description": "Switch port " "connected " "neighbor name",
                "type": "string",
            },
            "opticsType": {
                "description": "Switch port " "optics type",
                "type": "string",
            },
            "outUtilization": {
                "description": "Switch port " "traffic out " "utilization",
                "type": "number",
            },
            "packets": {
                "additionalProperties": False,
                "description": "Port packet " "transmit " "information",
                "properties": {
                    "broadcastIn": {
                        "description": "Switch "
                        "port "
                        "broadcast "
                        "in "
                        "packet "
                        "count",
                        "type": "integer",
                    },
                    "broadcastOut": {
                        "description": "Switch "
                        "port "
                        "broadcast "
                        "out "
                        "packet "
                        "count",
                        "type": "integer",
                    },
                    "multicastIn": {
                        "description": "Switch "
                        "port "
                        "multicast "
                        "in "
                        "packet "
                        "count",
                        "type": "integer",
                    },
                    "multicastOut": {
                        "description": "Switch "
                        "port "
                        "multicast "
                        "out "
                        "packet "
                        "count",
                        "type": "integer",
                    },
                },
                "type": "object",
            },
            "poe": {
                "additionalProperties": False,
                "description": "PoE information of " "switch port",
                "properties": {
                    "free": {
                        "description": "Free "
                        "power "
                        "capacity "
                        "of "
                        "switch "
                        "port",
                        "type": "integer",
                    },
                    "percent": {
                        "description": "Power "
                        "used "
                        "percentage "
                        "of "
                        "switch "
                        "port",
                        "type": "number",
                    },
                    "total": {
                        "description": "Total "
                        "power "
                        "capacity "
                        "of "
                        "switch "
                        "port",
                        "type": "integer",
                    },
                },
                "type": "object",
            },
            "poeEnabled": {
                "description": "PoE Enabled, " "True or False",
                "type": "boolean",
            },
            "poeType": {"description": "PoE type", "type": "string"},
            "portError": {
                "additionalProperties": False,
                "description": "Port error " "Information",
                "properties": {
                    "crcError": {
                        "description": "Switch " "port " "CRC " "error " "count",
                        "type": "integer",
                    },
                    "inDiscard": {
                        "description": "Switch "
                        "port "
                        "traffic "
                        "in "
                        "discard "
                        "count",
                        "type": "integer",
                    },
                    "inError": {
                        "description": "Switch "
                        "port "
                        "traffic "
                        "in "
                        "error "
                        "count",
                        "type": "integer",
                    },
                    "outError": {
                        "description": "Switch "
                        "port "
                        "traffic "
                        "out "
                        "error "
                        "count",
                        "type": "integer",
                    },
                },
                "type": "object",
            },
            "portIdentifier": {
                "description": "Port " "Identifier " "of switch " "port",
                "type": "string",
            },
            "portSettingId": {"type": "string"},
            "portSpeed": {"description": "Switch port speed", "type": "string"},
            "sampledInstant": {
                "description": "Sampled " "instant of " "switch port",
                "type": "string",
            },
            "status": {
                "description": "Status of switch " "port, UP or DOWN",
                "type": "string",
            },
            "stpState": {"description": "Switch port STP " "state", "type": "integer"},
            "switchFamily": {
                "description": "Switch family " "of switch port",
                "type": "string",
            },
            "switchFirmwareVersion": {
                "description": "Switch " "firmware " "of " "switch " "port",
                "type": "string",
            },
            "switchGroup": {
                "description": "Switch group of " "switch port",
                "type": "string",
            },
            "switchId": {
                "description": "Switch id of " "switch port",
                "type": "string",
            },
            "switchModel": {
                "description": "Switch model of " "switch port",
                "type": "string",
            },
            "switchName": {
                "description": "Switch Name of " "switch port",
                "type": "string",
            },
            "trafficUsage": {
                "additionalProperties": False,
                "description": "Traffic usage " "information",
                "properties": {
                    "rx": {
                        "description": "Rx " "traffic " "usage " "of " "switch " "port",
                        "type": "integer",
                    },
                    "tx": {
                        "description": "Tx " "traffic " "usage " "of " "switch " "port",
                        "type": "integer",
                    },
                },
                "type": "object",
            },
            "type": {"description": "Type of switch port", "type": "string"},
            "unTaggedVlan": {
                "description": "Untagged vlan " "of switch port",
                "type": "string",
            },
            "usedInFormingStack": {
                "description": "Used in " "forming " "stack, " "True or " "False",
                "type": "boolean",
            },
            "vlans": {"description": "Switch port include " "vlans", "type": "string"},
        },
        "type": "object",
    },
    "switch_portDetailsQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "switch "
                "port "
                "detail "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "switch "
                "port "
                "detail "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/switch_portDetails"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Switch " "port " "detail " "list " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "switch " "port " "detail " "list " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "switch_portStatus": {
        "additionalProperties": False,
        "description": "$",
        "properties": {
            "adminDown": {"description": "Admin down port " "count", "type": "integer"},
            "down": {"description": "Down port count", "type": "integer"},
            "speed": {"description": "Switch port speed", "type": "string"},
            "speedInt": {
                "description": "Switch port fully " "speed",
                "type": "integer",
            },
            "total": {"description": "Total port count", "type": "integer"},
            "up": {"description": "Up port count", "type": "integer"},
            "warning": {"description": "Warring port count", "type": "integer"},
        },
        "type": "object",
    },
    "switch_stackMember": {
        "additionalProperties": False,
        "properties": {
            "activeMode": {"description": "Role of stack", "type": "string"},
            "model": {"description": "Switch model of stack", "type": "string"},
            "portStatus": {"$ref": "#/definitions/switch_portStatus"},
            "ports": {"description": "Port count of stack", "type": "integer"},
            "serialNumber": {
                "description": "Serial number " "of stack",
                "type": "string",
            },
            "switchModule": {
                "description": "Switch module " "of stack",
                "type": "string",
            },
            "switchName": {"description": "Switch name of " "stack", "type": "string"},
            "switchPorts": {"$ref": "#/definitions/switch_portDetails"},
            "switchUnit": {"description": "Switch unit of " "stack", "type": "string"},
        },
        "type": "object",
    },
    "switch_stackMemberQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra " "information " "for stack " "member " "list",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "stack "
                "member "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "stack "
                "member "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are more "
                "stack "
                "member "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/switch_stackMember"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "stack " "member " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Current " "stack " "member " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "switch_switchIdList": {
        "description": "$",
        "items": {"type": "string"},
        "type": "array",
    },
    "switch_switchPortsSummaryQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "switch "
                "ports "
                "summary "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "switch "
                "ports "
                "summary "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/switch_portStatus"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Switch " "ports " "summary " "list " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "switch " "ports " "summary " "list " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "switch_switchQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {"$ref": "#/definitions/common_rbacMetadata"},
            "firstIndex": {
                "description": "Index "
                "of the "
                "first "
                "registration "
                "rule "
                "returned "
                "out of "
                "the "
                "complete "
                "registration "
                "rule "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there are "
                "more  "
                "after the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/switch_networkSwitch"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Switch " "query " "result " "list " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "switch " "query " "result " "list " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "switch_topSwitchesByFirmwareQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "top "
                "switches "
                "by "
                "firmware "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "top "
                "switches "
                "by "
                "firmware "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/switch_barChart"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Top " "switches " "by " "firmware " "list " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total "
                "top "
                "switches "
                "by "
                "firmware "
                "list "
                "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "switch_topSwitchesByModelQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "top "
                "switches "
                "by "
                "model "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "top "
                "switches "
                "by "
                "model "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/switch_barChart"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Top " "switches " "by " "model " "list " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total "
                "top "
                "switches "
                "by "
                "model "
                "list "
                "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "syslogServers_createSyslogServerConfig": {
        "additionalProperties": False,
        "properties": {
            "ip": {
                "description": "Syslog " "server " "IP " "address",
                "type": "string",
            },
            "udpPort": {
                "description": "Syslog " "server " "UDP " "port",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "syslogServers_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "syslogServers_syslogServer": {
        "additionalProperties": False,
        "properties": {
            "createdTime": {"description": "Created " "Time", "type": "integer"},
            "creatorId": {
                "description": "Syslog " "server " "creator " "ID",
                "type": "string",
            },
            "creatorUsername": {
                "description": "Syslog " "server " "creator " "name",
                "type": "string",
            },
            "groupId": {"description": "Switch " "Group ID", "type": "string"},
            "id": {"description": "ID", "type": "string"},
            "ip": {"description": "Syslog server IP " "address", "type": "string"},
            "udpPort": {
                "description": "Syslog " "server UDP " "port",
                "type": "integer",
            },
            "updatedTime": {"description": "Updated " "Time", "type": "integer"},
            "updaterId": {
                "description": "Syslog " "server " "updater " "ID",
                "type": "string",
            },
            "updaterUsername": {
                "description": "Syslog " "server " "updater " "name",
                "type": "string",
            },
        },
        "type": "object",
    },
    "syslogServers_syslogServersQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {"description": "Extra " "information", "type": "object"},
            "firstIndex": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "configs "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "configs "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/syslogServers_syslogServer"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total "
                "raw "
                "data "
                "count "
                "in "
                "this "
                "response",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "records " "count " "in " "this " "response",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "trafficPolicy_createTrafficPolicy": {
        "additionalProperties": False,
        "properties": {
            "cbs": {
                "description": "Committed " "Burst " "Size " "(CBS)",
                "type": "string",
            },
            "cir": {
                "description": "Committed " "Information " "Rate(CIR)",
                "type": "string",
            },
            "exceedAction": {
                "description": "Traffic " "Policy " "Exceed " "action " "type",
                "enum": ["DROP", "PERMIT_AT_LOW_PRI"],
                "type": "string",
            },
            "meteringType": {
                "description": "Traffic " "Policy " "Metering " "type",
                "enum": ["BYTE", "PACKET"],
                "type": "string",
            },
            "name": {"description": "Traffic " "Policy " "Name", "type": "string"},
            "pbs": {"description": "Peak " "Burst " "Size " "(PBS)", "type": "string"},
            "pir": {
                "description": "Peak " "Information " "Rate " "(PIR)",
                "type": "string",
            },
            "rateLimitType": {
                "description": "Traffic " "Policy " "Rate " "Limiting " "type",
                "enum": ["FIXED", "ADAPTIVE"],
                "type": "string",
            },
            "switchId": {"description": "Switch " "Id", "type": "string"},
        },
        "type": "object",
    },
    "trafficPolicy_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "trafficPolicy_trafficPolicy": {
        "additionalProperties": False,
        "properties": {
            "aclNames": {
                "description": "ACL Names "
                "which "
                "applied "
                "the "
                "current "
                "traffic "
                "policy",
                "type": "string",
            },
            "cbs": {
                "description": "Committed " "Burst Size " "(CBS)",
                "type": "string",
            },
            "cir": {
                "description": "Committed " "Information " "Rate(CIR)",
                "type": "string",
            },
            "exceedAction": {
                "description": "Traffic " "Policy " "Exceed " "action " "type",
                "enum": ["DROP", "PERMIT_AT_LOW_PRI"],
                "type": "string",
            },
            "id": {"description": "Traffic Policy " "Id", "type": "string"},
            "meteringType": {
                "description": "Traffic " "Policy " "Metering " "type",
                "enum": ["BYTE", "PACKET"],
                "type": "string",
            },
            "name": {"description": "Traffic " "Policy Name", "type": "string"},
            "pbs": {"description": "Peak Burst " "Size (PBS)", "type": "string"},
            "pir": {
                "description": "Peak " "Information " "Rate (PIR)",
                "type": "string",
            },
            "rateLimitType": {
                "description": "Traffic " "Policy " "Rate " "Limiting " "type",
                "enum": ["FIXED", "ADAPTIVE"],
                "type": "string",
            },
            "switchId": {"description": "Switch Id", "type": "string"},
        },
        "type": "object",
    },
    "trafficPolicy_trafficPolicyQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "Traffic "
                "Policy "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "Traffic "
                "Policy "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "Traffic "
                "Policy "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/trafficPolicy_trafficPolicy"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "Traffic " "Policy " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total "
                "Traffic "
                "Policy "
                "count "
                "in "
                "this "
                "response",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "trafficPolicy_updateTrafficPolicy": {
        "additionalProperties": False,
        "properties": {
            "cbs": {
                "description": "Committed " "Burst " "Size " "(CBS)",
                "type": "string",
            },
            "cir": {
                "description": "Committed " "Information " "Rate(CIR)",
                "type": "string",
            },
            "exceedAction": {
                "description": "Traffic " "Policy " "Exceed " "action " "type",
                "enum": ["DROP", "PERMIT_AT_LOW_PRI"],
                "type": "string",
            },
            "meteringType": {
                "description": "Traffic " "Policy " "Metering " "type",
                "enum": ["BYTE", "PACKET"],
                "type": "string",
            },
            "name": {"description": "Traffic " "Policy " "Name", "type": "string"},
            "pbs": {"description": "Peak " "Burst " "Size " "(PBS)", "type": "string"},
            "pir": {
                "description": "Peak " "Information " "Rate " "(PIR)",
                "type": "string",
            },
            "rateLimitType": {
                "description": "Traffic " "Policy " "Rate " "Limiting " "type",
                "enum": ["FIXED", "ADAPTIVE"],
                "type": "string",
            },
            "switchId": {"description": "Switch " "Id", "type": "string"},
        },
        "type": "object",
    },
    "traffic_broadcast": {
        "additionalProperties": False,
        "properties": {
            "broadcastIn": {
                "description": "The broadcast in " "of the switch " "traffic",
                "type": "string",
            },
            "broadcastOut": {
                "description": "The broadcast " "out of the " "switch traffic",
                "type": "string",
            },
            "timestamp": {
                "description": "The broadcast " "timestamp of the " "switch traffic",
                "type": "string",
            },
            "total": {
                "description": "The total broadcast of " "the switch traffic",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "traffic_broadcastQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra "
                "information "
                "for "
                "broadcast "
                "traffic "
                "list",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "broadcast "
                "traffic "
                "list "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "broadcast "
                "traffic "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicates "
                "if "
                "there "
                "are "
                "more "
                "broadcast "
                "traffic "
                "list "
                "after "
                "the "
                "currently "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/traffic_broadcast"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "broadcast " "traffic " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "broadcast " "traffic " "list " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "traffic_multicast": {
        "additionalProperties": False,
        "properties": {
            "multicastIn": {
                "description": "The multicast in " "of the switch " "traffic",
                "type": "string",
            },
            "multicastOut": {
                "description": "The multicast " "out of the " "switch traffic",
                "type": "string",
            },
            "timestamp": {
                "description": "The multicast " "timestamp of the " "switch traffic",
                "type": "string",
            },
            "total": {
                "description": "The total multicast of " "the switch traffic",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "traffic_multicastQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra "
                "information "
                "for "
                "multicast "
                "traffic "
                "list",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "multicast "
                "traffic "
                "list "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "multicast "
                "traffic "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicates "
                "if "
                "there "
                "are "
                "more "
                "multicast "
                "traffic "
                "list "
                "after "
                "the "
                "currently "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/traffic_multicast"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "multicast " "traffic " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "multicast " "traffic " "list " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "traffic_portError": {
        "additionalProperties": False,
        "properties": {
            "crcErr": {
                "description": "the port crc error of " "the switch traffic",
                "type": "string",
            },
            "inErr": {
                "description": "the port in error of " "the switch traffic",
                "type": "string",
            },
            "outErr": {
                "description": "the port out error of " "the switch traffic",
                "type": "string",
            },
            "timestamp": {
                "description": "Timestamp of the " "switch traffic " "port error",
                "type": "string",
            },
            "total": {
                "description": "Total port error of " "the switch traffic",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "traffic_portErrorQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra "
                "information "
                "for "
                "port "
                "error "
                "traffic "
                "list",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "port "
                "error "
                "traffic "
                "list "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "port "
                "error "
                "traffic "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicates "
                "if "
                "there "
                "are "
                "more "
                "port "
                "error "
                "traffic "
                "list "
                "after "
                "the "
                "currently "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/traffic_portError"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "port " "error " "traffic " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total "
                "port "
                "error "
                "of "
                "traffic "
                "list "
                "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "traffic_queryCriteria": {
        "additionalProperties": False,
        "properties": {
            "extraFilters": {
                "items": {
                    "additionalProperties": False,
                    "properties": {
                        "operator": {"$ref": "#/definitions/common_filterOperator"},
                        "type": {
                            "enum": ["SWITCH", "SWITCH_GROUP", "PORT"],
                            "type": "string",
                        },
                        "value": {"type": "string"},
                    },
                    "type": "object",
                },
                "type": "array",
            },
            "extraTimeRange": {"$ref": "#/definitions/common_timeRange"},
            "filters": {
                "items": {
                    "additionalProperties": False,
                    "properties": {
                        "operator": {"$ref": "#/definitions/common_filterOperator"},
                        "type": {"enum": ["DOMAIN", "SWITCH_GROUP"], "type": "string"},
                        "value": {"type": "string"},
                    },
                    "type": "object",
                },
                "type": "array",
            },
        },
        "required": ["filters", "extraTimeRange"],
        "type": "object",
    },
    "traffic_topPortErrorQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra " "information " "for " "top " "port " "error",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "top "
                "port "
                "error "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicates "
                "if "
                "there "
                "are "
                "more "
                "top "
                "port "
                "error "
                "after "
                "the "
                "currently "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/traffic_trafficUsage"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Top " "port " "error " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "of " "top " "port " "error " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "traffic_topPortTrafficUsageQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra "
                "information "
                "for "
                "top "
                "port "
                "traffic "
                "usage",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "top "
                "port "
                "traffic "
                "usage "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicates "
                "if "
                "there "
                "are "
                "more "
                "top "
                "port "
                "traffic "
                "usage "
                "after "
                "the "
                "currently "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/traffic_trafficUsage"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Top " "port " "traffic " "usage " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total "
                "of "
                "top "
                "port "
                "traffic "
                "usage "
                "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "traffic_topSwitchPoEUtilizationQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra "
                "information "
                "for "
                "top "
                "PoE "
                "utilization",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "top "
                "PoE "
                "usage "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicates "
                "if "
                "there "
                "are "
                "more "
                "top "
                "PoE "
                "usage "
                "after "
                "the "
                "currently "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/traffic_trafficUsage"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "PoE " "utilization " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "PoE " "utilization " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "traffic_topTrafficUsageQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra " "information " "for " "top " "traffic " "usage",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "top "
                "traffic "
                "usage "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicates "
                "if "
                "there "
                "are "
                "more "
                "top "
                "traffic "
                "usage "
                "after "
                "the "
                "currently "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/traffic_trafficUsage"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Top " "traffic " "usage " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "of " "top " "traffic " "usage " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "traffic_traffic": {
        "additionalProperties": False,
        "properties": {
            "rx": {"description": "RX traffic of the switch", "type": "string"},
            "timestamp": {
                "description": "Timestamp of the " "switch traffic",
                "type": "string",
            },
            "total": {
                "description": "Total traffic of the " "switch",
                "type": "integer",
            },
            "tx": {"description": "TX traffic of the switch", "type": "string"},
        },
        "type": "object",
    },
    "traffic_trafficQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra " "information " "for " "traffic " "list",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "traffic "
                "list "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "traffic "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicates "
                "if "
                "there "
                "are "
                "more "
                "traffic "
                "list "
                "after "
                "the "
                "currently "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/traffic_traffic"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "traffic " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "of " "traffic " "list " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "traffic_trafficUsage": {
        "additionalProperties": False,
        "properties": {
            "id": {
                "description": "Identifier of the " "Traffic Usage",
                "type": "string",
            },
            "key": {
                "description": "Interface of the " "Traffic Usage",
                "type": "string",
            },
            "value": {
                "description": "Total Tx and Rx of " "Traffic Usage",
                "type": "number",
            },
        },
        "type": "object",
    },
    "traffic_unicast": {
        "additionalProperties": False,
        "properties": {
            "timestamp": {
                "description": "The unicast " "timestamp of the " "switch traffic",
                "type": "string",
            },
            "total": {
                "description": "The total unicast of the " "switch traffic",
                "type": "integer",
            },
            "unicastIn": {
                "description": "The unicast in of " "the switch traffic",
                "type": "string",
            },
            "unicastOut": {
                "description": "The unicast out of " "the switch traffic",
                "type": "string",
            },
        },
        "type": "object",
    },
    "traffic_unicastQueryResultList": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Extra "
                "information "
                "for "
                "unicast "
                "traffic "
                "list",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "unicast "
                "traffic "
                "list "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "unicast "
                "traffic "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicates "
                "if "
                "there "
                "are "
                "more "
                "unicast "
                "traffic "
                "list "
                "after "
                "the "
                "currently "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/traffic_unicast"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "unicast " "traffic " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total " "unicast " "traffic " "list " "count",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "troubleShooting_commonResult": {
        "additionalProperties": False,
        "properties": {
            "data": {"type": "string"},
            "error": {"$ref": "#/definitions/troubleShooting_errorObject"},
            "extra": {"type": "object"},
            "metaData": {"type": "object"},
            "success": {"type": "boolean"},
        },
        "type": "object",
    },
    "troubleShooting_errorObject": {
        "additionalProperties": False,
        "properties": {
            "list": {"items": {"type": "string"}, "type": "array"},
            "message": {"type": "string"},
            "msgKey": {"type": "string"},
        },
        "type": "object",
    },
    "troubleShooting_supportLogStatus": {
        "additionalProperties": False,
        "properties": {
            "createdTime": {
                "description": "Created " "Time " "of " "this " "SupportLog " "Request",
                "type": "string",
            },
            "downloadStatus": {
                "description": "SupportLog "
                "Download "
                "Status "
                "(DOWNLOADING, "
                "DONE, "
                "FAILED)",
                "enum": ["DOWNLOADING", "DONE", "TIMEOUT", "FAILED"],
                "type": "string",
            },
            "serialNumber": {
                "description": "Switch " "Serial " "Number",
                "type": "string",
            },
            "switchId": {"description": "Switch " "MAC " "Address", "type": "string"},
        },
        "type": "object",
    },
    "veConfig_create": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "Alto Id", "type": "string"},
            "dhcpRelayAgent": {
                "description": "DHCP Replay IP " "Address",
                "type": "string",
            },
            "groupId": {"description": "Switch Group ID", "type": "string"},
            "inAclConfigName": {
                "description": "Ingress ACL " "Config Name",
                "type": "string",
            },
            "inAclConfigUUID": {
                "description": "Ingress ACL " "Config UUID",
                "type": "string",
            },
            "ipAddress": {"description": "IP Address", "type": "string"},
            "ipRouterId": {"description": "IP Router ID", "type": "string"},
            "name": {"description": "name", "type": "string"},
            "ospfArea": {"description": "OSPF IP Address", "type": "string"},
            "outAclConfigName": {
                "description": "Egress ACL " "Config Name",
                "type": "string",
            },
            "outAclConfigUUID": {
                "description": "Egress ACL " "Config UUID",
                "type": "string",
            },
            "subnetMask": {"description": "Subnet Mask", "type": "string"},
            "switchId": {"description": "Switch ID", "type": "string"},
            "veId": {"description": "VE Id", "type": "integer"},
            "vlanId": {"description": "VLAN ID", "type": "integer"},
        },
        "type": "object",
    },
    "veConfig_createResult": {
        "properties": {"id": {"description": "The ID of Setting", "type": "string"}}
    },
    "veConfig_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "veConfig_list": {
        "additionalProperties": False,
        "properties": {
            "firstIndex": {
                "description": "Index of the first "
                "config returned out "
                "of the complete list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator of whether "
                "there are more configs "
                "after the current "
                "displayed list",
                "type": "boolean",
            },
            "list": {
                "description": "The list of configs in this " "response",
                "items": {"$ref": "#/definitions/veConfig_veConfig"},
                "type": "array",
            },
            "totalCount": {
                "description": "Total configs count " "in this response",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "veConfig_modify": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "Alto Id", "type": "string"},
            "dhcpRelayAgent": {
                "description": "DHCP Replay IP " "Address",
                "type": "string",
            },
            "inAclConfigName": {
                "description": "Ingress ACL " "Config Name",
                "type": "string",
            },
            "inAclConfigUUID": {
                "description": "Ingress ACL " "Config UUID",
                "type": "string",
            },
            "ipAddress": {"description": "IP Address", "type": "string"},
            "ipRouterId": {"description": "IP Router ID", "type": "string"},
            "name": {"description": "name", "type": "string"},
            "ospfArea": {"description": "OSPF IP Address", "type": "string"},
            "outAclConfigName": {
                "description": "Egress ACL " "Config Name",
                "type": "string",
            },
            "outAclConfigUUID": {
                "description": "Egress ACL " "Config UUID",
                "type": "string",
            },
            "subnetMask": {"description": "Subnet Mask", "type": "string"},
            "switchId": {"description": "Switch ID", "type": "string"},
            "vlanId": {"description": "VLAN ID", "type": "integer"},
        },
        "type": "object",
    },
    "veConfig_veConfig": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "Alto Id", "type": "string"},
            "createdTime": {
                "description": "Created Time",
                "format": "int64",
                "type": "integer",
            },
            "dhcpRelayAgent": {
                "description": "DHCP Replay " "IP Address",
                "type": "string",
            },
            "groupId": {"description": "Switch Group ID", "type": "string"},
            "id": {"description": "ID", "type": "string"},
            "inAclConfigName": {
                "description": "Ingress ACL " "Config Name",
                "type": "string",
            },
            "inAclConfigUUID": {
                "description": "Ingress ACL " "Config UUID",
                "type": "string",
            },
            "ipAddress": {"description": "IP Address", "type": "string"},
            "ipRouterId": {"description": "IP Router ID", "type": "string"},
            "name": {"description": "name", "type": "string"},
            "ospfArea": {"description": "OSPF IP Address", "type": "string"},
            "outAclConfigName": {
                "description": "Egress ACL " "Config Name",
                "type": "string",
            },
            "outAclConfigUUID": {
                "description": "Egress ACL " "Config UUID",
                "type": "string",
            },
            "subnetMask": {"description": "Subnet Mask", "type": "string"},
            "switchId": {"description": "Switch ID", "type": "string"},
            "switchName": {"description": "Switch Name", "type": "string"},
            "switchStatus": {"description": "Switch Status", "type": "string"},
            "updatedTime": {
                "description": "Updated Time",
                "format": "int64",
                "type": "integer",
            },
            "veId": {"description": "VE Id", "type": "integer"},
            "vlanId": {"description": "VLAN ID", "type": "integer"},
            "vsixEgressAclConfigName": {
                "description": "IPv6 " "Egress " "ACL " "Config " "Name",
                "type": "string",
            },
            "vsixIngressAclConfigName": {
                "description": "IPv6 " "Ingress " "ACL " "Config " "Name",
                "type": "string",
            },
        },
        "type": "object",
    },
    "vlanConfig_VlanConfig": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "Alto Id", "type": "string"},
            "arpInspectionTrustPort": {
                "description": "ARP " "Inspection " "Trust " "Port",
                "type": "string",
            },
            "arpInspections": {
                "items": {"$ref": "#/definitions/vlanConfig_vlanArpInspections"},
                "type": "array",
            },
            "createdTime": {
                "description": "The create " "time of the " "Vlan Config",
                "format": "int64",
                "type": "integer",
            },
            "enableArpInspection": {
                "description": "ARP " "Inspection " "Enabled",
                "type": "boolean",
            },
            "enableAsDefaultVlan": {"type": "boolean"},
            "enableIpv4DhcpSnooping": {
                "description": "IPv4 " "DHCP " "Snooping " "Enabled",
                "type": "boolean",
            },
            "enableManagementVlan": {"type": "boolean"},
            "familyId": {"description": "Family Id", "type": "string"},
            "groupId": {"description": "Group Id", "type": "string"},
            "id": {"description": "Id", "type": "string"},
            "igmpSnooping": {"description": "IGMP " "Snooping", "type": "string"},
            "ipv4DhcpSnoopingTrustPort": {
                "description": "IPv4 " "DHCP " "Snooping " "Trust " "Port",
                "type": "string",
            },
            "multicastVersion": {
                "description": "Mutilcast " "Version",
                "type": "integer",
            },
            "name": {"description": "Vlan Name", "type": "string"},
            "ports": {
                "items": {"$ref": "#/definitions/vlanConfig_VlanPorts"},
                "type": "array",
            },
            "pushTime": {
                "description": "Puch Schedule " "Time",
                "format": "int64",
                "type": "integer",
            },
            "pushTimeType": {
                "description": "Puch Config " "Type",
                "enum": ["NOW", "SCHEDULE"],
                "type": "string",
            },
            "rootBridgeFamilyId": {"type": "string"},
            "spanningTree": {
                "description": "Spanning " "Tree",
                "enum": ["STT_NONE", "STP", "RSTP"],
                "type": "string",
            },
            "spanningTreePriority": {
                "description": "Spanning " "Tree " "Priority",
                "type": "integer",
            },
            "switchId": {"description": "Switch Id", "type": "string"},
            "updatedTime": {
                "description": "The update " "time of the " "Vlan Config",
                "format": "int64",
                "type": "integer",
            },
            "vlanId": {"description": "Vlan Id", "type": "integer"},
        },
        "type": "object",
    },
    "vlanConfig_VlanPorts": {
        "additionalProperties": False,
        "properties": {
            "switchModel": {
                "description": "The Switch " "Model of " "Ports",
                "type": "string",
            },
            "taggedPorts": {
                "description": "The Tagged " "Ports of " "Ports",
                "type": "string",
            },
            "untaggedPorts": {
                "description": "The " "Untagged " "Ports of " "Ports",
                "type": "string",
            },
        },
        "type": "object",
    },
    "vlanConfig_createVlanConfig": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "Alto Id", "type": "string"},
            "arpInspectionTrustPort": {
                "description": "ARP " "Inspection " "Trust " "Port",
                "type": "string",
            },
            "arpInspections": {
                "items": {"$ref": "#/definitions/vlanConfig_vlanArpInspections"},
                "type": "array",
            },
            "enableArpInspection": {
                "description": "ARP " "Inspection " "Enabled",
                "type": "boolean",
            },
            "enableAsDefaultVlan": {"type": "boolean"},
            "enableIpv4DhcpSnooping": {
                "description": "IPv4 " "DHCP " "Snooping " "Enabled",
                "type": "boolean",
            },
            "enableManagementVlan": {"type": "boolean"},
            "familyId": {"description": "Family Id", "type": "string"},
            "groupId": {"description": "Group Id", "type": "string"},
            "igmpSnooping": {
                "description": "IGMP " "Snooping",
                "enum": ["IST_NONE", "ACTIVE", "PASSIVE"],
                "type": "string",
            },
            "ipv4DhcpSnoopingTrustPort": {
                "description": "IPv4 " "DHCP " "Snooping " "Trust " "Port",
                "type": "string",
            },
            "multicastVersion": {
                "description": "Mutilcast " "Version",
                "type": "integer",
            },
            "name": {"description": "Vlan Name", "type": "string"},
            "ports": {
                "items": {"$ref": "#/definitions/vlanConfig_VlanPorts"},
                "type": "array",
            },
            "pushTime": {
                "description": "Puch " "Schedule " "Time",
                "format": "int64",
                "type": "integer",
            },
            "pushTimeType": {
                "description": "Puch " "Config " "Type",
                "enum": ["NOW", "SCHEDULE"],
                "type": "string",
            },
            "rootBridgeFamilyId": {"type": "string"},
            "spanningTree": {
                "description": "Spanning " "Tree",
                "enum": ["STT_NONE", "STP", "RSTP"],
                "type": "string",
            },
            "spanningTreePriority": {
                "description": "Spanning " "Tree " "Priority",
                "type": "integer",
            },
            "switchId": {"description": "Switch Id", "type": "string"},
            "vlanId": {"description": "Vlan Id", "type": "integer"},
        },
        "type": "object",
    },
    "vlanConfig_emptyResult": {
        "additionalProperties": False,
        "properties": {},
        "type": "object",
    },
    "vlanConfig_updateVlanConfig": {
        "additionalProperties": False,
        "properties": {
            "altoId": {"description": "Alto Id", "type": "string"},
            "arpInspectionTrustPort": {
                "description": "ARP " "Inspection " "Trust " "Port",
                "type": "string",
            },
            "arpInspections": {
                "items": {"$ref": "#/definitions/vlanConfig_vlanArpInspections"},
                "type": "array",
            },
            "enableArpInspection": {
                "description": "ARP " "Inspection " "Enabled",
                "type": "boolean",
            },
            "enableIpv4DhcpSnooping": {
                "description": "IPv4 " "DHCP " "Snooping " "Enabled",
                "type": "boolean",
            },
            "enableManagementVlan": {"type": "boolean"},
            "igmpSnooping": {
                "description": "IGMP " "Snooping",
                "enum": ["IST_NONE", "ACTIVE", "PASSIVE"],
                "type": "string",
            },
            "ipv4DhcpSnoopingTrustPort": {
                "description": "IPv4 " "DHCP " "Snooping " "Trust " "Port",
                "type": "string",
            },
            "multicastVersion": {
                "description": "Mutilcast " "Version",
                "type": "integer",
            },
            "name": {"description": "Vlan Name", "type": "string"},
            "ports": {
                "items": {"$ref": "#/definitions/vlanConfig_VlanPorts"},
                "type": "array",
            },
            "pushTime": {
                "description": "Puch " "Schedule " "Time",
                "format": "int64",
                "type": "integer",
            },
            "pushTimeType": {
                "description": "Puch " "Config " "Type",
                "enum": ["NOW", "SCHEDULE"],
                "type": "string",
            },
            "rootBridgeFamilyId": {"type": "string"},
            "spanningTree": {
                "description": "Spanning " "Tree",
                "enum": ["STT_NONE", "STP", "RSTP"],
                "type": "string",
            },
            "spanningTreePriority": {
                "description": "Spanning " "Tree " "Priority",
                "type": "integer",
            },
        },
        "type": "object",
    },
    "vlanConfig_vlanArpInspections": {
        "additionalProperties": False,
        "properties": {
            "ip": {"description": "The IP of " "ArpInspections", "type": "string"},
            "mac": {"description": "The MAC of " "ArpInspections", "type": "string"},
        },
        "type": "object",
    },
    "vlanConfig_vlanConfigQueryResult": {
        "additionalProperties": False,
        "properties": {
            "extra": {
                "description": "Any " "additional " "response " "data",
                "type": "object",
            },
            "firstIndex": {
                "description": "Index "
                "of "
                "the "
                "first "
                "Vlan "
                "Configs "
                "returned "
                "out "
                "of "
                "the "
                "complete "
                "Vlan "
                "Configs "
                "list",
                "type": "integer",
            },
            "hasMore": {
                "description": "Indicator "
                "of "
                "whether "
                "there "
                "are "
                "more "
                "Vlan "
                "Configs "
                "after "
                "the "
                "current "
                "displayed "
                "list",
                "type": "boolean",
            },
            "list": {
                "items": {"$ref": "#/definitions/vlanConfig_VlanConfig"},
                "type": "array",
            },
            "rawDataTotalCount": {
                "description": "Total " "Vlan " "Configs " "count",
                "type": "integer",
            },
            "totalCount": {
                "description": "Total "
                "Vlan "
                "Configs "
                "count "
                "in "
                "this "
                "response",
                "type": "integer",
            },
        },
        "type": "object",
    },
}
