from commands.custom_command import CustomCommand
import pyautogui

class MouseCommand(CustomCommand):
    
    def get_command(self):
        return "mouse"

    def get_description(self):
        return "Moves mouse to given coordinates (\"x,y\")."

    def get_author(self):
        return "Dariusz Gulbicki"

    def get_version(self):
        return "1.0.0"

    def execute(self, args):
        args = args.split(",")
        pyautogui.moveTo(int(args[0]), int(args[1]))
        return False