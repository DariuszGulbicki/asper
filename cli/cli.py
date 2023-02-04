import click
from cli.cli_personas import persona as persona
from cli.cli_run import run
from cli.cli_logger import logger
from utils.path_utils import get_default_app_folder
from utils.initializer import init_asper

@click.group("cli")
def cli():
    """Lets you interact with ASPER via the command line."""
    pass

cli.add_command(persona)
cli.add_command(run)
cli.add_command(logger)