from commands.custom_command import CustomCommand
import os

class TerminalCommand(CustomCommand):
    
    def get_command(self):
        return "terminal"

    def get_description(self):
        return "Executes a command via system shell."

    def get_author(self):
        return "Dariusz Gulbicki"

    def get_version(self):
        return "1.0.0"

    def execute(self, args):
        os.system(args)
        return False