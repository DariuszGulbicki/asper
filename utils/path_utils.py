import os
import sys
import platform

def get_installation_path():
    if getattr(sys, 'frozen', False):
        # The application is frozen
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        application_path = os.path.dirname(__file__)

    if 'pip' in application_path:
        # The program was installed via pip
        path = sys._MEIPASS
    else:
        # The program was cloned via git
        path = application_path
    # Thats stupid but will suffice for now
    return path.replace("/utils", "")

def get_installed_path(path):
    return os.path.join(get_installation_path(), path)

def get_default_app_folder():
    sysname = platform.system()
    if sysname == "Windows":
        return os.path.join(os.getenv("APPDATA"), "asper")
    elif sysname == "Linux":
        return os.path.join(os.getenv("HOME"), ".asper")