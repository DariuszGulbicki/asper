import re
from bs4 import BeautifulSoup

class Command:

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def get_name(self):
        return self.name

    def get_args(self):
        return self.args

def parse_user_text(text, commands):
    for command in commands:
        text = text.strip()
        if text.lower().startswith(command):
            return [command, text[len(command):].strip()]
    return None

# Make a function in python that parses text into commands (command class) and arguments
# They will be returned as a list of command class and strings and sorted in the order they appear in the text
# Beautiful soup is used to parse the text
# Loose spaces are removed
# THE RETURNED LIST MUST BE SORTED IN THE ORDER THE COMMANDS AND STRINGS APPEAR IN THE TEXT
# Example:
# parse_commands("Hello, <print>this is a test</print> and this is a string")
# returns:
# ["Hello, ",Command("print", "this is a test"), " and this is a string"]
# Example 2:
# parse_commands("Hello, <comm1>this is a test</comm1> and this is a string <comm2>and this is another test</comm2>")
# returns:
# ["Hello, ",Command("comm1", "this is a test"), " and this is a string ",Command("comm2", "and this is another test")]
# Example 3:
# parse_commands(<input>This </input> is a test <audio>system_stopped</audio>)
# returns:
# [Command("input", "This "), " is a test ",Command("audio", "system_stopped")]
def parse_commands(text):
    soup = BeautifulSoup(text, 'html.parser')
    parsed = []
    for element in soup:
        if isinstance(element, str):
            parsed.append(element)
        else:
            parsed.append(Command(element.name, element.text))
    return parsed