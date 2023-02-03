import utils.command_interpreter as parser

from message_processing import message_processor_manager as proc
from logging_system import logger

class user_command:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def execute(self, args):
        self.function(args)

_user_commands = []
_assistant_commands = []

def _array_of_command_names(commands):
    names = []
    for command in commands:
        names.append(command.name)
    return names

def _check_for_user_command(text):
    logger.debug("Checking for user commands", "Responder")
    parsed_commands = parser.parse_user_text(text, _array_of_command_names(_user_commands))
    if parsed_commands != None:
        for command in _user_commands:
            if command.name == parsed_commands[0]:
                logger.info("Executing user command: " + command.name, "Responder")
                return command.execute(parsed_commands[1])
    else:
        return True

def _handle_assistant_commands(text, default_function):
    logger.debug("Checking for assistant commands", "Responder")
    parsed_commands = parser.parse_commands(text)
    for command in parsed_commands:
        if isinstance(command, parser.Command):
            for assistant_command in _assistant_commands:
                if command.get_name() == assistant_command.name:
                    if command.get_args() != None:
                        logger.info("Executing assistant command: " + assistant_command.name + " with args: " + command.get_args(), "Responder")
                        pros = assistant_command.execute(command.get_args())
                        if isinstance(pros, str) and default_function != None:
                            logger.debug("Executing default function with: " + pros + " from assistant command: " + assistant_command.name + " with args: " + command.get_args(), "Responder")
                            default_function(pros)
                    else:
                        logger.info("Executing assistant command: " + assistant_command.name + " with no args", "Responder")
                        pros = assistant_command.execute(None)
                        if isinstance(pros, str) and default_function != None:
                            logger.debug("Adding default function with: " + pros + " from assistant command: " + assistant_command.name, "Responder")
                            default_function(pros)
        else:
            if default_function != None and command != "" and command != " ":
                logger.debug("Executing default function with: " + command, "Responder")
                default_function(command)

def respond(text, default_function):
    if _check_for_user_command(text):
        _handle_assistant_commands(proc.process_message(text), default_function)

def init():
    proc.initialize_processor()

def register_user_command(name, function):
    _user_commands.append(user_command(name, function))
    logger.debug("Registering user command: " + name, "Responder")

def register_assistant_command(name, function):
    _assistant_commands.append(user_command(name, function))
    logger.debug("Registering assistant command: " + name, "Responder")

def clear_registered_commands():
    _user_commands.clear()
    _assistant_commands.clear()