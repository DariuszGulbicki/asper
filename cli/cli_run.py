import click
from termcolor import colored
from utils import audio_effects as audio
from utils import speech_recognizer as sr
from utils import text_to_speech as tts
from utils import responder
from config import config_manager as configs
from personality import personality_manager as personas
from utils import printer
from commands import custom_command_loader as commands
from utils.initializer import init_asper


_render_emojis = True
_render_colors = True

def _render_emoji(emoji):
    if _render_emojis:
        return emoji
    else:
        return ""

def _render_colored(list):
    text = ""
    for item in list:
        if isinstance(item, str):
            text += item + " "
        elif isinstance(item, tuple) and _render_colors:
            text += colored(item[0], item[1]) + " "
        elif isinstance(item, tuple):
            text += item[0] + " "
    return text

def _read_text(text):
    tts.read_text(text)

def _text_said(text):
    responder.respond(text, _read_text)
    audio.play_listening_finished()

def _hotword_detected(text):
    audio.play_listening_started()

@click.command("run")
def run():
    init_asper()
    commands.load_commands()
    """Runs an ASPER persona."""
    printer.print_welcome_screen(configs.config.version)
    audio.play_system_started()
    tts.read_welcome_message()
    responder.init()
    sr.microphone_recognition_hotword(personas.persona.hotwords, _text_said, _hotword_detected, hotword_model=personas.persona.hotword_model, hotword_engine=personas.persona.hotword_engine, trigger_engine=personas.persona.assistant_engine, trigger_model=personas.persona.assistant_model) 