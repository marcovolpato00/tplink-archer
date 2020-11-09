from tplink_archer import WifiFreq


def test_queries(connection, test_server):
    with test_server.run('127.0.0.1', 5000):
        connection.get_dhcp_leases()
        connection.get_external_ip()
        connection.get_stats()
        connection.get_dhcp_clients()
        connection.get_wifi_clients(WifiFreq.WIFI_2G)
        connection.get_wifi_clients(WifiFreq.WIFI_5G)
        connection.get_port_forwarding_rules()


def test_downloads(connection, test_server):
    with test_server.run('127.0.0.1', 5000):
        connection.download_config_backup('/tmp')
        with open('/tmp/conf.bin', 'r') as f:
            content = f.read()
            assert content == 'conf'

