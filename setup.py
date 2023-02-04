from setuptools import setup, find_packages

long_description = open('README.md').read()

setup(
    name='asper',
    version='0.0.2',
    author="Dariusz Gulbicki",
    description="Assistant Personalities. A system to quickly create voice assistants for different tasks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
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