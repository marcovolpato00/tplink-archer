import json
import click
import pprint
from pathlib import Path
from typing import Optional
from functools import wraps

from tplink_archer import ArcherConnection, AuthError, WifiFreq


CONFIG_FILE_PATH = Path.home().joinpath('.config', 'tplink-archer', 'config.json')

connection: Optional[ArcherConnection] = None
pp = pprint.PrettyPrinter(indent=4)


def save_config(config: dict):
    if not CONFIG_FILE_PATH.parent.exists():
        CONFIG_FILE_PATH.parent.mkdir(parents=True)

    with open(CONFIG_FILE_PATH, 'w+') as f:
        json.dump(config, f)


def load_config() -> Optional[dict]:
    if not CONFIG_FILE_PATH.exists():
        return None

    with open(CONFIG_FILE_PATH) as f:
        config = json.load(f)

    return config


def authentication_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global connection
        config = load_config()
        if config:
            connection = authenticate(load_config())
            if connection:
                return func(*args, **kwargs)
        click.echo('You should authenticate first')
    return wrapper


def pretty_print(stuff):
    pp.pprint(stuff)

########################################################################################################################


def authenticate(config: dict) -> Optional[ArcherConnection]:
    archer_connection = ArcherConnection(config['router_url'])
    try:
        archer_connection.authenticate(config['username'], config['password'])
    except AuthError:
        return None
    return archer_connection


@click.group()
def cli():
    pass


@click.command()
@click.option('--url', prompt=True)
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def auth(url, username, password):
    config = {
        'router_url': url,
        'username': username,
        'password': password
    }
    if authenticate(config):
        click.echo('Successfully authenticated')
        save_config(config)
    else:
        click.echo('Cannot authenticate')


@click.command()
@authentication_required
def stats():
    pretty_print(connection.get_stats())


@click.command()
@authentication_required
def dhcp_clients():
    pretty_print(connection.get_dhcp_clients())


@click.command()
@authentication_required
def dhcp_leases():
    pretty_print(connection.get_dhcp_leases())


@click.command()
@authentication_required
def external_ip():
    click.echo(connection.get_external_ip())


@click.command()
@click.option('--freq', default='2g', type=click.Choice(['2g', '5g']))
@authentication_required
def wifi_clients(freq: str):
    wifi_freq = WifiFreq.WIFI_2G
    if freq == '5g':
        wifi_freq = WifiFreq.WIFI_5G
    pretty_print(connection.get_wifi_clients(wifi_freq))


@click.command()
@authentication_required
def port_forwarding():
    pretty_print(connection.get_port_forwarding_rules())


cli.add_command(auth)
cli.add_command(stats)
cli.add_command(dhcp_clients)
cli.add_command(dhcp_leases)
cli.add_command(external_ip)
cli.add_command(wifi_clients)
cli.add_command(port_forwarding)


if __name__ == '__main__':
    cli()

