from commands.custom_command import CustomCommand
import tkinter as tk
import threading

class OnScreenCommand(CustomCommand):
    
    def get_command(self):
        return "onscreen"

    def get_description(self):
        return "Shows given text on screen using a window."

    def get_author(self):
        return "Dariusz Gulbicki"

    def get_version(self):
        return "1.0.0"

    def _create_window(self, args):
        root = tk.Tk()
        root.title("Assistant")
        root.geometry("300x300")
        root.resizable(False, False)
        root.configure(bg="black")
        label = tk.Label(root, text=args, bg="black", fg="white", font=("Arial", 20))
        label.pack()
        root.mainloop()

    def execute(self, args):
        threading.Thread(target=self._create_window, args=(args,)).start()
        return False