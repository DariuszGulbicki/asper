from config import config_manager as configs
from personality import personality_manager as personas
from logging_system import logger
from cli import cli
from utils.initializer import init_asper

if __name__ == '__main__':
    init_asper()
    cli.cli(obj={})