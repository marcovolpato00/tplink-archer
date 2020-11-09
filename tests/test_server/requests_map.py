import os
from typing import Optional

from tplink_archer import constants


base_path = os.path.dirname(__file__)


REQUESTS_MAP = [
    {
        'params': '?1&5',
        'query': constants.STATS_QUERY,
        'response_file': 'stats.txt',
        'name': 'STATS_QUERY'
    },
    {
        'params': '?5',
        'query': constants.DHCP_LEASES_QUERY,
        'response_file': 'dhcp_leases.txt',
        'name': 'DHCP_LEASES_QUERY'
    },
    {
        'params': '?1&1&1&5&5&5&5&5&5&5&5&5&5&5',
        'query': constants.EXTERNAL_IP_QUERY,
        'response_file': 'external_ip.txt',
        'name': 'EXTERNAL_IP_QUERY'
    },
    {
        'params': '?5',
        'query': constants.DHCP_CLIENTS_QUERY,
        'response_file': 'dhcp_clients.txt',
        'name': 'DHCP_CLIENTS_QUERY'
    },
    {
        'params': '?6',
        'query': constants.WIFI_2G_CLIENTS_QUERY,
        'response_file': '2g_clients.txt',
        'name': 'WIFI_2G_CLIENTS_QUERY'
    },
    {
        'params': '?6',
        'query': constants.WIFI_5G_CLIENTS_QUERY,
        'response_file': '5g_clients.txt',
        'name': 'WIFI_5G_CLIENTS_QUERY'
    },
    {
        'params': '?5&5&5&5',
        'query': constants.PORT_FORWARDING_RULES_QUERY,
        'response_file': 'port_forwarding_rules.txt',
        'name': 'PORT_FORWARDING_RULES_QUERY'
    },
    {
        'params': '/conf.bin',
        'query': '',
        'response_file': 'conf.txt',
        'name': 'DOWNLOAD_CONF_BACKUP'
    }
]


def get_response(params: str, query: str) -> Optional[dict]:
    request = None
    for r in REQUESTS_MAP:
        if r.get('params') == params and r.get('query') == query:
            request = r
    
    if not request:
        return None

    with open(os.path.join(base_path, 'responses', request.get('response_file')), 'r') as f:
        data = f.read()

    request.update({'data': data})

    return request
