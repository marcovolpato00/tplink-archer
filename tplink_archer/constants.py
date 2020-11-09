# URLs

STATS_URL = 'cgi?1&5'
EXTERNAL_IP_URL = 'cgi?1&1&1&5&5&5&5&5&5&5&5&5&5&5'
DHCP_CLIENTS_URL = 'cgi?5'
WIFI_CLIENTS_URL = 'cgi?6'
DHCP_LEASES_URL = DHCP_CLIENTS_URL
DHCP_LEASES_CREATE_URL = 'cgi?3'
DHCP_LEASES_DELETE_URL = 'cgi?4'
DHCP_LEASES_TOGGLE_URL = 'cgi?2'
PORT_FORWARDING_RULES_URL = 'cgi?5&5&5&5'

CONFIG_DOWNLOAD_URL = 'cgi/conf.bin?'
AUTHENTICATION_URL = 'main/status.htm'


########################################################################################################################
# Queries

DHCP_LEASES_QUERY = '[LAN_DHCP_STATIC_ADDR#0,0,0,0,0,0#0,0,0,0,0,0]0,3\r\nenable\r\nchaddr\r\nyiaddr\r\n'

STATS_QUERY = ('[WAN_DSL_INTF_CFG#1,0,0,0,0,0#0,0,0,0,0,0]0,12\r\nstatus\r\n'
               'modulationType\r\nX_TP_AdslModulationCfg\r\nupstreamCurrRate\r\n'
               'downstreamCurrRate\r\nX_TP_AnnexType\r\nupstreamMaxRate\r\ndownstreamMaxRate\r\n'
               'upstreamNoiseMargin\r\ndownstreamNoiseMargin\r\nupstreamAttenuation\r\n'
               'downstreamAttenuation\r\n[WAN_DSL_INTF_STATS_TOTAL#1,0,0,0,0,0#0,0,0,0,0,0]1,8\r\n'
               'ATUCCRCErrors\r\nCRCErrors\r\nATUCFECErrors\r\nFECErrors\r\nSeverelyErroredSecs\r\n'
               'X_TP_US_SeverelyErroredSecs\r\nerroredSecs\r\nX_TP_US_ErroredSecs\r\n')

EXTERNAL_IP_QUERY = ('[SYS_MODE#0,0,0,0,0,0#0,0,0,0,0,0]0,1\r\nmode\r\n[IGD#0,0,0,0,0,0#0,0,0,0,0,0]1,1\r\n'
                     'LANDeviceNumberOfEntries\r\n[IGD_DEV_INFO#0,0,0,0,0,0#0,0,0,0,0,0]2,3\r\nsoftwareVersion\r\n'
                     'hardwareVersion\r\nupTime\r\n[WAN_DSL_INTF_CFG#0,0,0,0,0,0#0,0,0,0,0,0]3,1\r\nstatus\r\n'
                     '[WAN_COMMON_INTF_CFG#0,0,0,0,0,0#0,0,0,0,0,0]4,1\r\nWANAccessType\r\n'
                     '[WAN_DSL_LINK_CFG#0,0,0,0,0,0#0,0,0,0,0,0]5,0\r\n'
                     '[WAN_IP_CONN#0,0,0,0,0,0#0,0,0,0,0,0]6,0\r\n[WAN_PPP_CONN#0,0,0,0,0,0#0,0,0,0,0,0]7,'
                     '0\r\n[WAN_L2TP_CONN#0,0,0,0,0,0#0,0,0,0,0,0]8,0\r\n'
                     '[WAN_PPTP_CONN#0,0,0,0,0,0#0,0,0,0,0,0]9,0\r\n[L2_BRIDGING_ENTRY#0,0,0,0,0,0#0,0,0,0,0,0]10,'
                     '1\r\nbridgeName\r\n '
                     '[LAN_WLAN#0,0,0,0,0,0#0,0,0,0,0,0]11,'
                     '12\r\nstatus\r\nSSID\r\nBSSID\r\nchannel\r\nautoChannelEnable\r\nstandard\r\nbeaconType\r\n '
                     'basicEncryptionModes\r\nX_TP_Bandwidth\r\npossibleDataTransmitRates\r\nWPAAuthenticationMode\r'
                     '\nIEEE11iAuthenticationMode\r\n '
                     '[LAN_WLAN_WDSBRIDGE#0,0,0,0,0,0#0,0,0,0,0,0]12,1\r\nBridgeEnable\r\n[LAN_WLAN_TASK_SCHEDULE#0,0,'
                     '0,0,0,0#0,0,0,0,0,0]13,2\r\nenable\r\nisUsrCtrl\r\n')

DHCP_CLIENTS_QUERY = '[LAN_HOST_ENTRY#0,0,0,0,0,0#0,0,0,0,0,0]0,' \
                     '4\r\nleaseTimeRemaining\r\nMACAddress\r\nhostName\r\nIPAddress\r\n '

WIFI_2G_CLIENTS_QUERY = '[LAN_WLAN_ASSOC_DEV#0,0,0,0,0,0#1,1,0,0,0,0]0,' \
                        '4\r\nAssociatedDeviceMACAddress\r\nX_TP_TotalPacketsSent\r\nX_TP_TotalPacketsReceived\r' \
                        '\nX_TP_HostName\r\n '

WIFI_5G_CLIENTS_QUERY = '[LAN_WLAN_ASSOC_DEV#0,0,0,0,0,0#1,2,0,0,0,0]0,' \
                        '4\r\nAssociatedDeviceMACAddress\r\nX_TP_TotalPacketsSent\r\nX_TP_TotalPacketsReceived\r' \
                        '\nX_TP_HostName\r\n '

PORT_FORWARDING_RULES_QUERY = '[WAN_IP_CONN_PORTMAPPING#0,0,0,0,0,0#0,0,0,0,0,0]0,0\r\n[WAN_PPP_CONN_PORTMAPPING#0,0,' \
                              '0,0,0,0#0,0,0,0,0,0]1,0\r\n[WAN_L2TP_CONN_PORTMAPPING#0,0,0,0,0,0#0,0,0,0,0,0]2,' \
                              '0\r\n[WAN_PPTP_CONN_PORTMAPPING#0,0,0,0,0,0#0,0,0,0,0,0]3,0\r\n '

TOGGLE_DHCP_LEASE_COMMAND = '[LAN_DHCP_STATIC_ADDR#{raw_identifier}#0,0,0,0,0,0]0,1\r\nenable={enabled}\r\n'

CREATE_DHCP_LEASE_COMMAND = '[LAN_DHCP_STATIC_ADDR#0,0,0,0,0,0#1,0,0,0,0,0]0,3\r\n' \
                            'chaddr={mac_address}\r\n' \
                            'yiaddr={ip_address}\r\n' \
                            'enable={enabled}\r\n'

DELETE_DHCP_LEASE_COMMAND = '[LAN_DHCP_STATIC_ADDR#{raw_identifier}#0,0,0,0,0,0]0,0\r\n'
