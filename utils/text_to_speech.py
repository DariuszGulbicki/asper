import threading
from gtts import gTTS, lang as langs
from playsound import playsound

welocme_message = "System started"

lang = "en-GB"
slow = False
  
def get_available_languages():
    return langs.tts_langs()

def get_available_languages_ids():
    return langs.tts_langs().keys()

def read_text(text):
    myobj = gTTS(text=text, lang=lang, slow=slow)
    myobj.save("cache.mp3")
    playsound("cache.mp3")

def read_welcome_message():
    read_text(welocme_message)