import asyncio
import click
from utils.db import db as dbs


@click.group()
def db():
    pass


@db.command()
def seed():
    asyncio.run(dbs.seed())


cli = click.CommandCollection(sources=[db])

if __name__ == '__main__':
    cli()