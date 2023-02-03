import os
from playsound import playsound

from logging_system import logger

# 'effects/' + music_pack + '/' + name + '.wav'

music_pack = "scifi"
play = True

def get_available_packs():
    return os.listdir("effects/")

def play_effect(name):
    logger.debug("Playing effect: " + name, "Audio effects")
    try:
        if play:
            playsound('effects/' + music_pack + '/' + name + '.wav')
    except Exception as e:
        logger.error("There was an error when playing file" + name + '.wav', "Audio effects", e)

def play_listening_started():
    play_effect("listening_started")

def play_listening_finished():
    play_effect("listening_finished")

def play_system_started():
    play_effect("system_started")

def play_system_stopped():
    play_effect("system_stopped")