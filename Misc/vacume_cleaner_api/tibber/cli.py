import asyncio

import click
from hypercorn import Config
from hypercorn.asyncio import serve

from tibber.api import app
from tibber.models import first_migration


@click.group
def cli_root():
    pass


@cli_root.command()
def run():
    asyncio.run(serve(app, Config()))


@cli_root.group
def db():
    pass


@db.command()
def migrate():
    asyncio.run(first_migration())
