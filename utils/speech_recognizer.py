import speech_recognition as sr
import os
import Errors.RecognitionError as RecognitionError
from enum import Enum
import time
from pydub import AudioSegment
from pydub.silence import split_on_silence
from utils.speech_recognition_engines import SpeechRecognitionEngines
from logging_system import logger

last = False


recognizer = sr.Recognizer()
model = "base.en"
engine = SpeechRecognitionEngines.WHISPER

def recognize_audio(audio, model=model, engine=engine):
    if (engine == SpeechRecognitionEngines.GOOGLE):
        return recognizer.recognize_google(audio, model)
    elif (engine == SpeechRecognitionEngines.SPHINX):
        return recognizer.recognize_sphinx(audio, model)
    elif (engine == SpeechRecognitionEngines.VOSK):
        return recognizer.recognize_vosk(audio, model)
    elif (engine == SpeechRecognitionEngines.IBM):
        return recognizer.recognize_ibm(audio, model)
    elif (engine == SpeechRecognitionEngines.WHISPER):
        return recognizer.recognize_whisper(audio, model)

def audio_file_transcript(path):
    with sr.AudioFile(path) as source:
        audio = recognizer.record(source)
    return recognize_audio(audio)

def large_audio_file_transcription(path):
    sound = AudioSegment.from_wav(path)  
    chunks = split_on_silence(sound,
        min_silence_len = 500,
        silence_thresh = sound.dBFS-14,
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = recognizer.record(source)
            try:
                text = recognize_audio(audio_listened)
            except sr.UnknownValueError as e:
                logger.error(str(e), "Speech recognizer")
            else:
                text = f"{text.capitalize()}. "
                logger.info(chunk_filename, ":", text)
                whole_text += text
    return whole_text

def microphone_recognition(duration=5):
    with sr.Microphone() as source:
        audio_data = recognizer.record(source, duration)
        logger.info("Recognizing speech", "Speech recognizer")
        text = recognize_audio(audio_data)
        return text

def microphone_recognition_continuous():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            logger.info("Listening", "Speech recognizer")
            audio_data = recognizer.listen(source)
            logger.info("Recognizing speech", "Speech recognizer")
            text = recognize_audio(audio_data)
            logger.info(text)

# When any of the hotwords are detected, voice recognition is started and will stop after 3 seconds of silence and run the trigger function with recognized text as argument
def microphone_recognition_hotword(hotwords, trigger, hotword_recognized, hotword_model=model, trigger_model=model, hotword_engine=engine, trigger_engine=engine, detect_frequency=3, hotword_sleep=3):
    global recognizer
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            logger.info("🎙  Listening for hotword", "Speech recognizer")
            audio_data = recognizer.listen(source, phrase_time_limit=detect_frequency)
            logger.info("💠 Recognizing speech for hotword", "Speech recognizer")
            try:
                text = recognize_audio(audio_data, hotword_model, hotword_engine)
                logger.info("🗣  Hotword engine recognized: " + text, "Speech recognizer")
                if any(hotword in (" " + text + " ").lower() for hotword in hotwords):
                    logger.info("🔴 Hotword Detected", "Speech recognizer")
                    hotword_recognized(text)
                    time.sleep(hotword_sleep)
                    audio_data = recognizer.listen(source, timeout=7, phrase_time_limit=7)
                    text = recognize_audio(audio_data, trigger_model, trigger_engine)
                    # Close and reopen the stream to reset the buffer
                    # #Not resetting the buffer causes the recognizer to recognize hotwords in TTS
                    source.stream.close()
                    source.stream = None
                    trigger(text)
                    source.__enter__()
            except sr.UnknownValueError as e:
                logger.error("Google Speech Recognition could not understand audio", "Speech recognizer", e)
            except sr.RequestError as e:
                logger.error("Could not request results from Google Speech Recognition service; {0}".format(e), "Speech recognizer", e)
            except sr.WaitTimeoutError as e:
                logger.error("Timeout", "Speech recognizer", e)