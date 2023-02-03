from commands.custom_command import CustomCommand
from utils import audio_effects as audio
import os

class AudioCommand(CustomCommand):
    
    def get_command(self):
        return "audio"

    def get_description(self):
        return "Plays specified audio effect."

    def get_author(self):
        return "Dariusz Gulbicki"

    def get_version(self):
        return "1.0.0"

    def execute(self, args):
        audio.play_effect(args)
        return False