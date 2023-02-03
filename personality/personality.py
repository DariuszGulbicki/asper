from utils.speech_recognition_engines import SpeechRecognitionEngines as Engines
import os

class Personality:

    def __init__(self):
        self.name = "New personality"
        self.description = "This is a new personality personality for your assistant. It could be the start of something great!"
        self.author = os.getlogin()
        self.hotwords = ["computer", "assistant", "jarvis", "hey jarvis", "hey computer", "hey assistant"]
        self.hotword_engine = Engines.WHISPER
        self.hotword_model = "tiny.en"
        self.assistant_engine = Engines.WHISPER
        self.assistant_model = "base.en"
        self.selected_message_processor = "null"
        self.message_processor_config = { }
        self.disabled_user_commands = [ ]
        self.disabled_assistant_commands = [ ]
        self.audio_effects_enabled = True
        self.audio_effects_pack = "scifi"
        self.tts_slow = False
        self.tts_language = "en"
        self.welcome_message = "Hello, world!"