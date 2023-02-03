from commands.custom_command import CustomCommand
import pyautogui

class KeyInputCommand(CustomCommand):
    
    def get_command(self):
        return "keyinput"

    def get_description(self):
        return "Inputs given text using keyboard."

    def get_author(self):
        return "Dariusz Gulbicki"

    def get_version(self):
        return "1.0.0"

    def execute(self, args):
        pyautogui.typewrite(args)
        return False