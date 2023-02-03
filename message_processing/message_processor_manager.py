from importlib import import_module
from importlib.machinery import SourceFileLoader
import os

from logging_system import logger
from message_processing.message_processor import MessageProcessor
from utils import printer
from config import config_manager as configs
from utils import path_utils as paths

processors = []
selected_processor = None

processor_config = {}

# Load all processors from given directory
# Use library importlib to import all modules in directory
# Each module must have a class that extends the base class "message_processor"
# Instantiate each class and add it to the list of processors
def load_processors_from_directory(dir):
    logger.debug("Loading processors from directory: " + dir, "Message processor manager")
    for file in os.listdir(dir):
        if file.endswith(".py"):
            logger.debug("Loading processor from file " + file, "Message processor manager")
            module = SourceFileLoader(file[:-3], os.path.join(dir, file)).load_module()
            for name, obj in module.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, MessageProcessor):
                    processors.append(obj())


def _load_default_processors():
    logger.debug("Loading default processors", "Message processor manager")
    load_processors_from_directory(paths.get_installed_path("message_processing/default/"))

def _load_user_processors():
    logger.debug("Loading user processors", "Message processor manager")
    try:
        load_processors_from_directory(paths.get_default_app_folder() + "/processors/")
    except FileNotFoundError:
        logger.warn("Asper user message processor directory not found.", "Message processor manager")

def load_processors():
    logger.debug("Loading processors", "Message processor manager")
    global processors
    processors = []
    _load_default_processors()
    _load_user_processors()

def get_processors():
    table = []
    for processor in processors:
        table.append([processor.get_processor_id(), processor.get_processor_name(), processor.get_processor_description(), processor.get_processor_author()])
    return table

def pretty_print_processors():
    table = []
    for processor in processors:
        table.append([processor.get_processor_id(), processor.get_processor_name(), processor.get_processor_description(), processor.get_processor_author(), processor.get_processor_version()])
    printer.pretty_print_table(table, ["ID", "Name", "Description", "Author", "Version"])

def initialize_processor():
    logger.debug("Initializing processor", "Message processor manager")
    if selected_processor == None:
        logger.error("No processor selected.", "Message processor manager")
        return
    selected_processor.initialize(processor_config)

def process_message(message):
    if selected_processor == None:
        logger.error("No processor selected.", "Message processor manager")
        return
    return selected_processor.process_message(message)

def select_processor(id):
    global selected_processor
    for processor in processors:
        if processor.get_processor_id() == id:
            selected_processor = processor
            return
    logger.error("Processor with ID " + id + " not found.", "Message processor manager")

def get_selected_processor():
    return selected_processor

def _get_selected_processor_parameters():
    return [selected_processor.get_processor_id(), selected_processor.get_processor_name(), selected_processor.get_processor_description(), selected_processor.get_processor_author(), selected_processor.get_processor_version()]

def pretty_print_selected_processor():
    return printer.pretty_print_table([_get_selected_processor_parameters()], ["ID", "Name", "Description", "Author", "Version"])