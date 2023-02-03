from setuptools import setup

setup(
    name='asper',
    version='0.0.1',
    packages=[''],
    install_requires=[
        'SpeechRecognition',
        'pyaudio',
        'pydub',
        'PocketSphinx',
        'Vosk',
        'setuptools',
        'openai-whisper',
        'torch',
        'setuptools-rust',
        'tensorrt',
        'numpy',
        'gtts',
        'playsound',
        'pyautogui',
        'termcolor',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'asper = cli.cli:cli',
            'asper-persona = cli.cli_personas:persona',
            'asper-run = cli.cli_run:run',
            'asper-logger = cli.cli_logger:logger'
        ],
    },
)