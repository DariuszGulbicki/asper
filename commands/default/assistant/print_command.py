from commands.custom_command import CustomCommand

class PrintCommand(CustomCommand):
    
    def get_command(self):
        return "print"

    def get_description(self):
        return "Prints given text to the terminal."

    def get_author(self):
        return "Dariusz Gulbicki"

    def get_version(self):
        return "1.0.0"

    def execute(self, args):
        print(args)
        return False