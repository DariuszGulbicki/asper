from config import config_manager as configs
from personality import personality_manager as personas
from logging_system import logger
from cli import cli

if __name__ == '__main__':
    logger.debug("Starting ASPER", "Main")
    configs.load()
    personas.load()
    cli.cli(obj={})