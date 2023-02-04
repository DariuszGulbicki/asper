from config import config_manager as configs
from personality import personality_manager as personas
from logging_system import logger

_initialized = False

def init_asper():
    global _initialized
    if not _initialized:
        _initialized = True
        logger.info("Starting ASPER", "Initializer")
        configs.load()
        personas.load()
    else:
        logger.debug("ASPER is already initialized", "Initializer")