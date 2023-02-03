import os
import platform
import yaml

from logging_system import logger
from personality.personality import Personality
from message_processing import message_processor_manager as proc
from config import config_manager as configs
from utils import audio_effects as audio
from utils import text_to_speech as tts
from commands import custom_command_loader as commands
from cli import cli_run as crun

from utils import printer


personas = []
selected_personality = "default.asper"
persona = Personality()

def _get_default_app_folder():
    sysname = platform.system()
    if sysname == "Windows":
        return os.path.join(os.getenv("APPDATA"), "asper")
    elif sysname == "Linux":
        return os.path.join(os.getenv("HOME"), ".asper")

def _execute_load_hooks():
    logger.debug("Executing load hooks", "Personality manager")
    logger.debug("executing message processor load hook", "Personality manager")
    # Load the message processors #
    proc.load_processors()
    proc.select_processor(persona.selected_message_processor)
    proc.processor_config = persona.message_processor_config
    logger.debug("executing audio load hook", "Personality manager")
    # Load audio settings #
    audio.play = persona.audio_effects_enabled
    audio.music_pack = persona.audio_effects_pack
    logger.debug("executing tts load hook", "Personality manager")
    # Load TTS settings #
    tts.slow = persona.tts_slow
    tts.lang = persona.tts_language
    tts.welocme_message = persona.welcome_message
    logger.debug("executing commands load hook", "Personality manager")
    # Load disabled commands #
    commands._user_disabled_commands = persona.disabled_user_commands
    commands._assistant_disabled_commands = persona.disabled_assistant_commands
    logger.debug("executing cli load hook", "Personality manager")
    # Load cli settings #
    #crun._hotwords = persona.hotwords
    #crun._hotword_model = persona.hotword_model

def load():
    global persona
    logger.debug("Loading selected personality", "Personality manager")
    def_app_folder = _get_default_app_folder()
    try:
        with open(os.path.join(def_app_folder, "personas", selected_personality), "r") as f:
            persona = yaml.load(f.read(), Loader=yaml.Loader)
    except FileNotFoundError:
        logger.warn("Personality file not found. Creating new one.", "Personality manager")
        persona = Personality()
        save()
    _execute_load_hooks()

def save():
    logger.debug("Saving selected personality", "Personality manager")
    def_app_folder = _get_default_app_folder()
    os.makedirs(os.path.join(def_app_folder, "personas"), exist_ok=True)
    try:
        with open(os.path.join(def_app_folder, "personas", selected_personality), "x") as f:
            f.write(yaml.dump(persona))
            logger.debug("Created new personality file.", "Personality manager")
    except FileExistsError:
        with open(os.path.join(def_app_folder, "personas", selected_personality), "w") as f:
            f.write(yaml.dump(persona))

def _search_personas_dir():
    logger.debug("Searching for personas", "Personality manager")
    global personas
    def_app_folder = _get_default_app_folder()
    temp_personas = []
    temp = None
    for file in os.listdir(os.path.join(def_app_folder, "personas")):
        if file.endswith(".asper") or file.endswith(".yml") or file.endswith(".yaml"):
            logger.debug("Found persona file: " + file, "Personality manager")
            temp = yaml.load(open(os.path.join(def_app_folder, "personas", file), "r").read(), Loader=yaml.Loader)
            temp_personas.append([file, temp.name, temp.description, temp.author])
    personas = temp_personas
    logger.debug("Found " + str(len(personas)) + " personas", "Personality manager")

def refresh_avaiable_personas():
    logger.debug("Refreshing avaiable personas", "Personality manager")
    _search_personas_dir()

def change_personality(file):
    logger.debug("Changing personality to " + file, "Personality manager")
    global selected_personality
    selected_personality = file
    load()

def destroy_personality(per_file):
    global selected_personality
    if per_file is None:
        per_file = selected_personality
    logger.debug("Destroying personality " + per_file, "Personality manager")
    def_app_folder = _get_default_app_folder()
    os.remove(os.path.join(def_app_folder, "personas", per_file))
    selected_personality = "default.asper"
    load()
    return per_file

def pretty_print_personas():
    printer.pretty_print_table(personas, ["File", "Name", "Description", "Author"])

def pretty_print_selected_persona():
    printer.pretty_print_table([[persona.name, persona.description, persona.author]], ["Name", "Description", "Author"], trim=100)