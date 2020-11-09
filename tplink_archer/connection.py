import os
import base64
import requests
from typing import List

from .exceptions import AuthError, RequestError
from .constants import *
from .models import Stack, DHCPLease, PortForwardingRule, WifiFreq


class ArcherConnection(object):
    """Object that provides an interface with TP-Link Archer routers
    """

    def __init__(self, router_url: str):
        """Init ArcherConnection object

        :param router_url: URL or IP address of the router
        """

        self.router_url = router_url
        self.is_authenticated = False
        self.headers = None

    def __repr__(self):
        return f'<ArcherConnection(router_url={self.router_url},is_authenticated={str(self.is_authenticated)})>'

    def authenticate(self, username: str, password: str):
        """Authenticate to the router using your username and password

        :param username:
        :param password:
        """

        credentials = base64.b64encode(
            bytes('{}:{}'.format(username, password), 'UTF-8')).decode('UTF-8')
        self.authenticate_basicauth(credentials)
  
    def authenticate_basicauth(self, credentials: str):
        """Authenticate using your username and password encoded in base64

        :param credentials: base64 encoded 'username:password'
        """

        self.headers = {
            'Referer': f'http://{self.router_url}/',
            'Cookie': 'Authorization=Basic ' + credentials
        }

        attempts = 1
        while attempts <= 2 and not self.is_authenticated:      # sometimes 2 attempts are necessary
            r = self.__get_request(AUTHENTICATION_URL)
            self.is_authenticated = True
            if r.status_code != 200:
                self.is_authenticated = False
            attempts += 1
        if not self.is_authenticated:
            raise AuthError

    def __get_request(self, request_url: str) -> requests.Response:
        """Performs a GET request

        :param request_url:
        :rtype: requests.Response
        """
        r = requests.get(
            f'http://{self.router_url}/{request_url}',
            headers=self.headers,
        )
        return r

    def __post_request(self, request_url: str, data: dict) -> requests.Response:
        """Performs a POST request

        :param request_url:
        :param data: data to send
        :rtype: requests.Response
        """
        r = requests.post(
            f'http://{self.router_url}/{request_url}',
            headers=self.headers,
            data=data
        )
        return r

    def api_request(self, request_type: str, url: str, data: dict = None) -> requests.Response:
        """Performs an HTTP request to the device

        :param request_type: either 'get' or 'post'
        :param url: request URL
        :param data: data to send in a POST request, ignored if GET
        :rtype: requests.Response
        """

        if not self.is_authenticated:
            raise AuthError

        if request_type == 'get':
            r = self.__get_request(url)
        elif request_type == 'post':
            r = self.__post_request(url, data)
        else:
            raise ValueError('Invalid request type')

        if r.status_code != 200:
            raise RequestError('Response status code not 200')

        return r

    def get_stats(self) -> dict:
        """Get router statistics about connection speed

        :rtype: dict
        """

        data = STATS_QUERY
        r = self.api_request('post', STATS_URL, data)

        stack = Stack(r.text)
        values = stack.sections[0].values

        return {
            'current_up_rate': values.get('upstreamCurrRate'),
            'current_down_rate': values.get('downstreamCurrRate'),
            'max_up_rate': values.get('upstreamMaxRate'),
            'max_down_rate': values.get('downstreamMaxRate'),
        }

    def get_external_ip(self) -> str:
        """Get router external IP address

        :rtype: str
        """

        data = EXTERNAL_IP_QUERY
        r = self.api_request('post', EXTERNAL_IP_URL, data)

        stack = Stack(r.text)
        section = stack.get_section('[1,1,1,0,0,0]7')
        external_ip = section.values.get('externalIPAddress')
        return external_ip

    def get_dhcp_clients(self) -> List[dict]:
        """Get all (almost) router DHCP clients

        :rtype: list
        """

        data = DHCP_CLIENTS_QUERY
        r = self.api_request('post', DHCP_CLIENTS_URL, data)

        stack = Stack(r.text)

        clients = []
        for c in stack.sections:
            values = c.values
            if c.identifier != '[error]0':
                clients.append({
                    'ip_address': values.get('IPAddress'),
                    'mac_address': values.get('MACAddress'),
                    'hostname': values.get('hostName')
                })
        return clients

    def get_wifi_clients(self, wifi_freq: WifiFreq) -> List[str]:
        """Get list of MAC addresses connected to specified WiFi frequency

        :param wifi_freq: WiFi frequency
        :rtype: list
        """

        data = WIFI_2G_CLIENTS_QUERY
        if wifi_freq == WifiFreq.WIFI_5G:
            data = WIFI_5G_CLIENTS_QUERY

        r = self.api_request('post', WIFI_CLIENTS_URL, data)

        stack = Stack(r.text)

        clients = []
        for c in stack.sections:
            if c.identifier != '[error]0':
                clients.append(c.values.get('associatedDeviceMACAddress'))
        return clients

    def get_dhcp_leases(self) -> List[DHCPLease]:
        """Get list of all static DHCP leases

        :return: list of DHCP leases objects
        :rtype: List[DHCPLease]
        """

        data = DHCP_LEASES_QUERY
        r = self.api_request('post', DHCP_LEASES_URL, data)

        stack = Stack(r.text)

        leases = []
        for section in stack.sections:
            identifier = section.identifier
            if identifier != '[error]0':
                values = section.values
                l = DHCPLease(
                    identifier=identifier,
                    ip_address=values.get('yiaddr'),
                    mac_address=values.get('chaddr'),
                    is_enabled=values.get('enable') == '1'
                )
                leases.append(l)

        return leases

    def create_dhcp_lease(self, ip_address: str, mac_address: str, is_enabled: bool) -> DHCPLease:
        """Create DHCP lease

        :param ip_address: lease IP address
        :param mac_address: lease MAC address
        :param is_enabled: lease is enabled
        :return: newly created DHCP lease
        :rtype: DHCPLease
        """
        enabled = '1' if is_enabled else '0'
        data = CREATE_DHCP_LEASE_COMMAND.format(
            mac_address=mac_address,
            ip_address=ip_address,
            enabled=enabled
        )
        self.api_request('post', DHCP_LEASES_CREATE_URL, data)
        leases = self.get_dhcp_leases()
        new_lease = [l for l in leases if l.ip_address == ip_address][0]
        return new_lease

    def delete_dhcp_lease(self, dhcp_lease: DHCPLease):
        """Deletes DHCP lease

        :param dhcp_lease: DHCPLease to delete
        """
        data = DELETE_DHCP_LEASE_COMMAND.format(raw_identifier=dhcp_lease.raw_identifier)
        self.api_request('post', DHCP_LEASES_DELETE_URL, data)

    def toggle_dhcp_lease(self, dhcp_lease: DHCPLease, enable: bool):
        """Toggle DHCP lease enable

        :param dhcp_lease: DHCPLease object to toggle
        :param enable: whether enable or not
        """
        enabled = '1' if enable else '0'
        data = TOGGLE_DHCP_LEASE_COMMAND.format(raw_identifier=dhcp_lease.raw_identifier, enabled=enabled)
        self.api_request('post', DHCP_LEASES_TOGGLE_URL, data)
        dhcp_lease.is_enabled = enable

    def enable_dhcp_lease(self, dhcp_lease: DHCPLease):
        """Enables DHCP lease

        :param dhcp_lease:
        """
        self.toggle_dhcp_lease(dhcp_lease, enable=True)

    def disable_dhcp_lease(self, dhcp_lease: DHCPLease):
        """Disables DHCP lease

        :param dhcp_lease:
        """
        self.toggle_dhcp_lease(dhcp_lease, enable=False)

    def get_port_forwarding_rules(self) -> List[PortForwardingRule]:
        """Get list of all port forwarding rules

        :return: list of port forwaring rules
        :rtype: List[PortForwardingRule]
        """

        data = PORT_FORWARDING_RULES_QUERY
        r = self.api_request('post', PORT_FORWARDING_RULES_URL, data)

        stack = Stack(r.text)

        rules = []
        for section in stack.sections:
            identifier = section.identifier
            if identifier != '[error]0':
                values = section.values
                r = PortForwardingRule(
                    identifier=identifier,
                    client_ip_address=values.get('internalClient'),
                    internal_port=values.get('internalPort'),
                    external_port=values.get('externalPort'),
                    internal_port_end=values.get('X_TP_InternalPortEnd'),
                    external_port_end=values.get('X_TP_ExternalPortEnd'),
                    is_enabled=values.get('portMappingEnabled') == '1',
                    protocol=values.get('portMappingProtocol')
                )
                rules.append(r)

        return rules

    def download_config_backup(self, download_path: str = None):
        """Downloads router configuration

        :param download_path: path where to save file
        """
        file_name = 'conf.bin'
        if not download_path:
            download_path = os.path.join(file_name)
        else:
            download_path = os.path.join(download_path, file_name)

        r = self.api_request('get', CONFIG_DOWNLOAD_URL)
        with open(download_path, 'wb') as f:
            f.write(r.content)
