from commands.custom_command import CustomCommand

class ExecuteCommand(CustomCommand):
    
    def get_command(self):
        return "execute"

    def get_description(self):
        return "Executes python script."

    def get_author(self):
        return "Dariusz Gulbicki"

    def get_version(self):
        return "1.0.0"

    def execute(self, args):
        exec(args)
        return False