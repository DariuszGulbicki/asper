import click
from termcolor import colored
from utils.speech_recognition_engines import SpeechRecognitionEngines as Engines
from utils import printer
from config import config_manager as configs
from personality import personality_manager as personas
from message_processing import message_processor_manager as proc
from utils import audio_effects as audio
from utils import text_to_speech as txtts

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

@click.group("persona")
def persona():
    """Lets you manage your personas."""
    pass

@click.command("list")
def list_personas():
    """Lists all your personas."""
    personas.refresh_avaiable_personas()
    personas.pretty_print_personas()

@click.command("selected")
def selected_persona():
    """Shows the currently selected persona."""
    personas.pretty_print_selected_persona()

@click.command("select")
@click.argument("persona_file", required=True, type=str)
def select_persona(persona_file):
    """Selects a persona."""
    if not (persona_file.endswith(".asper") or persona_file.endswith(".yml") or persona_file.endswith(".yaml")):
        persona_file += ".asper"
    configs.config.selected_persona = persona_file
    personas.change_personality(persona_file)
    configs.save()
    click.echo(_render_emoji("🔄 ") + _render_colored([("Selected persona:", "green"), (persona_file, "magenta")]))

@click.command("destroy")
@click.argument("persona_file", required=False, type=str)
def destroy_persona(persona_file):
    """Destroys a persona."""
    if persona_file is not None and (not (persona_file.endswith(".asper") or persona_file.endswith(".yml") or persona_file.endswith(".yaml"))):
        persona_file += ".asper"
    destroyed = personas.destroy_personality(persona_file)
    configs.config.selected_persona = "default.asper"
    configs.save()
    click.echo(_render_emoji("🔥 ") + _render_colored([("Destroyed persona:", "red"), (destroyed, "yellow")]))


@click.command("name")
@click.argument("new_name",required=False, default=None, type=str)
def change_persona_name(new_name):
    """Lists or changes the name of your persona."""
    if new_name == None:
        click.echo(_render_emoji("📝 ") + _render_colored([("Current name:", "green"), (personas.persona.name, "magenta")]))
        return
    personas.persona.name = new_name
    personas.save()
    click.echo(_render_emoji("🔄 ") + _render_colored([("Changed name to:", "green"), (new_name, "magenta")]))

@click.command("description")
@click.argument("new_description",required=False, default=None, type=str)
def change_persona_description(new_description):
    """Lists or changes the description of your persona."""
    if new_description == None:
        click.echo(_render_emoji("📝 ") + _render_colored([("Current description:", "green"), (personas.persona.description, "magenta")]))
        return
    personas.persona.description = new_description
    personas.save()
    click.echo(_render_emoji("🔄 ") + _render_colored([("Changed description to:", "green"), (new_description, "magenta")]))

@click.command("author")
@click.argument("new_author", required=False, default=None, type=str)
def change_persona_author(new_author):
    """Lists or changes the author of your persona."""
    if new_author == None:
        click.echo(_render_emoji("📝 ") + _render_colored([("Current author:", "green"), (personas.persona.author, "magenta")]))
        return
    personas.persona.author = new_author
    personas.save()
    click.echo(_render_emoji("🔄 ") + _render_colored([("Changed author to:", "green"), (new_author, "magenta")]))

@click.command("hotwords")
@click.option("--add", "-a", multiple=True, help="Adds a hotword to your persona.", type=str)
@click.option("--remove", "-r", multiple=True, help="Removes a hotword from your persona.", type=str)
def list_hotwords(add, remove):
    """Lists all hotwords of your persona."""
    for hotword in add:
        personas.persona.hotwords.append(hotword)
        click.echo(_render_emoji("➕ ") + _render_colored([("Added hotword:", "green"), (hotword, "magenta")]))
    for hotword in remove:
        personas.persona.hotwords.remove(hotword)
        click.echo(_render_emoji("➖ ") + _render_colored([("Removed hotword:", "green"), (hotword, "magenta")]))
    printer.pretty_print_list_vertical(personas.persona.hotwords)
    personas.save()

@click.command("hotword-engine")
@click.argument("engine", required=False, default=None, type=str)
def change_hotword_engine(engine):
    """Lists or changes the hotword engine of your persona."""
    if engine == None:
        click.echo(_render_emoji("📝 ") + _render_colored([("Current hotword engine:", "green"), (personas.persona.hotword_engine, "magenta")]))
        return
    enum_engine = None
    if engine == "google":
        enum_engine = Engines.GOOGLE
    elif engine == "sphinx":
        enum_engine = Engines.SPHINX
    elif engine == "ibm":
        enum_engine = Engines.IBM
    elif engine == "whisper":
        enum_engine = Engines.WHISPER
    if enum_engine == None:
        click.echo(_render_emoji("❌ ") + _render_colored([("Invalid engine:", "red"), (engine, "magenta")]))
        return
    personas.persona.hotword_engine = enum_engine
    personas.save()
    click.echo(_render_emoji("🔄 ") + _render_colored([("Changed hotword engine to:", "green"), (engine, "magenta")]))

@click.command("hotword-model")
@click.argument("model", required=False, default=None, type=str)
def change_hotword_model(model):
    """Lists or changes the hotword model of your persona."""
    if model == None:
        click.echo(_render_emoji("📝 ") + _render_colored([("Current hotword model:", "green"), (personas.persona.hotword_model, "magenta")]))
        return
    personas.persona.hotword_model = model
    personas.save()
    click.echo(_render_emoji("🔄 ") + _render_colored([("Changed hotword model to:", "green"), (model, "magenta")]))

@click.command("assistant-engine")
@click.argument("engine", required=False, default=None, type=str)
def change_assistant_engine(engine):
    """Lists or changes the assistant engine of your persona."""
    if engine == None:
        click.echo(_render_emoji("📝 ") + _render_colored([("Current assistant engine:", "green"), (personas.persona.assistant_engine, "magenta")]))
        return
    enum_engine = None
    if engine == "google":
        enum_engine = Engines.GOOGLE
    elif engine == "sphinx":
        enum_engine = Engines.SPHINX
    elif engine == "ibm":
        enum_engine = Engines.IBM
    elif engine == "whisper":
        enum_engine = Engines.WHISPER
    if enum_engine == None:
        click.echo(_render_emoji("❌ ") + _render_colored([("Invalid engine:", "red"), (engine, "magenta")]))
        return
    personas.persona.assistant_engine = enum_engine
    personas.save()
    click.echo(_render_emoji("🔄 ") + _render_colored([("Changed assistant engine to:", "green"), (engine, "magenta")]))

@click.command("assistant-model")
@click.argument("model", required=False, default=None, type=str)
def change_assistant_model(model):
    """Lists or changes the assistant model of your persona."""
    if model == None:
        click.echo(_render_emoji("📝 ") + _render_colored([("Current assistant model:", "green"), (personas.persona.assistant_model, "magenta")]))
        return
    personas.persona.assistant_model = model
    personas.save()
    click.echo(_render_emoji("🔄 ") + _render_colored([("Changed assistant model to:", "green"), (model, "magenta")]))

@click.command("message-processor")
@click.argument("processor", required=False, default=None, type=str)
def change_message_processor(processor):
    """Lists or changes the message processor of your persona."""
    if processor == None:
        click.echo(_render_emoji("📝 ") + _render_colored([("Current message processor:", "green"), (personas.persona.selected_message_processor, "magenta")]))
        return 
    if processor not in [proc[0] for proc in proc.get_processors()]:
        click.echo(_render_emoji("❌ ") + _render_colored([("Invalid processor:", "red"), (processor, "magenta")]))
        return
    personas.persona.selected_message_processor = processor
    personas.save()
    click.echo(_render_emoji("🔄 ") + _render_colored([("Changed message processor to:", "green"), (processor, "magenta")]))

@click.group("message-processor-settings")
def message_processor_settings():
    """Lists or changes the settings of the message processor of your persona."""
    pass

@click.command("list")
def list_message_processor_settings():
    """Lists the settings of the message processor of your persona."""
    click.echo(_render_emoji("📝 ") + _render_colored([("Current message processor settings:", "green")]))
    printer.pretty_print_dict_vertical(personas.persona.message_processor_config)

@click.command("add")
@click.argument("key", required=True, type=str)
@click.argument("value", required=True, type=str)
def add_message_processor_setting(key, value):
    """Adds a setting to the message processor of your persona."""
    personas.persona.message_processor_config[key] = value
    personas.save()
    click.echo(_render_emoji("➕ ") + _render_colored([("Added message processor setting:", "green"), (key, "magenta"), ("with value:", "green"), (value, "magenta")]))
    click.echo(_render_emoji("📝 ") + _render_colored([("Current message processor settings:", "green")]))
    printer.pretty_print_dict_vertical(personas.persona.message_processor_config)

@click.command("remove")
@click.argument("key", required=True, type=str)
def remove_message_processor_setting(key):
    """Removes a setting from the message processor of your persona."""
    if key not in personas.persona.message_processor_config:
        click.echo(_render_emoji("❌ ") + _render_colored([("Invalid key:", "red"), (key, "magenta")]))
        return
    personas.persona.message_processor_config.pop(key)
    personas.save()
    click.echo(_render_emoji("➖ ") + _render_colored([("Removed message processor setting:", "green"), (key, "magenta")]))
    click.echo(_render_emoji("📝 ") + _render_colored([("Current message processor settings:", "green")]))
    printer.pretty_print_dict_vertical(personas.persona.message_processor_config)

@click.command("disabled-user-commands")
@click.option("--add", "-a", required=False, multiple=True, default=None, type=str)
@click.option("--remove", "-r", required=False, multiple=True, default=None, type=str)
def disabled_user_commands(add, remove):
    """Lists or changes the disabled user commands of your persona."""
    if add == None and remove == None:
        click.echo(_render_emoji("📝 ") + _render_colored([("Current disabled user commands:", "green")]))
        printer.pretty_print_list_vertical(personas.persona.disabled_user_commands)
        return
    if add != None:
        for command in add:
            if command not in personas.persona.disabled_user_commands:
                click.echo(_render_emoji("➕ ") + _render_colored([("Added disabled user command:", "green"), (command, "magenta")]))
                personas.persona.disabled_user_commands.append(command)
    if remove != None:
        for command in remove:
            if command in personas.persona.disabled_user_commands:
                click.echo(_render_emoji("➖ ") + _render_colored([("Removed disabled user command:", "green"), (command, "magenta")]))
                personas.persona.disabled_user_commands.remove(command)
    personas.save()
    click.echo(_render_emoji("🔄 ") + _render_colored([("Changed disabled user commands:", "green")]))
    printer.pretty_print_list_vertical(personas.persona.disabled_user_commands)

@click.command("disabled-assistant-commands")
@click.option("--add", "-a", required=False, multiple=True, default=None, type=str)
@click.option("--remove", "-r", required=False, multiple=True, default=None, type=str)
def disabled_assistant_commands(add, remove):
    """Lists or changes the disabled assistant commands of your persona."""
    if add == None and remove == None:
        click.echo(_render_emoji("📝 ") + _render_colored([("Current disabled assistant commands:", "green")]))
        printer.pretty_print_list_vertical(personas.persona.disabled_assistant_commands)
        return
    if add != None:
        for command in add:
            if command not in personas.persona.disabled_assistant_commands:
                click.echo(_render_emoji("➕ ") + _render_colored([("Added disabled assistant command:", "green"), (command, "magenta")]))
                personas.persona.disabled_assistant_commands.append(command)
    if remove != None:
        for command in remove:
            if command in personas.persona.disabled_assistant_commands:
                click.echo(_render_emoji("➖ ") + _render_colored([("Removed disabled assistant command:", "green"), (command, "magenta")]))
                personas.persona.disabled_assistant_commands.remove(command)
    personas.save()
    click.echo(_render_emoji("🔄 ") + _render_colored([("Changed disabled assistant commands:", "green")]))
    printer.pretty_print_list_vertical(personas.persona.disabled_assistant_commands)

@click.group("audio-effects")
def audio_effects():
    """Manages audio effects."""
    pass

@click.command("enable")
def enable_audio_effects():
    """Enables audio effects for your persona."""
    personas.persona.audio_effects_enabled = True
    personas.save()
    click.echo(_render_emoji("🔊 ") + _render_colored([("Enabled audio effects!", "green")]))
    click.echo(_render_emoji("🔊 ") + _render_colored([("Current audio effects pack:", "green"), (personas.persona.audio_effects_pack, "magenta")]))

@click.command("disable")
def disable_audio_effects():
    """Disables audio effects for your persona."""
    personas.persona.audio_effects_enabled = False
    personas.save()
    click.echo(_render_emoji("🔇 ") + _render_colored([("Disabled audio effects!", "green")]))

@click.command("list-packs")
def list_audio_effects_packs():
    """Lists all available audio effects packs."""
    click.echo(_render_emoji("📦 ") + _render_colored([("Available audio effects packs:", "green")]))
    printer.pretty_print_list_vertical(audio.get_available_packs())

@click.command("select-pack")
@click.argument("effects_pack", required=True, type=str)
def select_audio_effects_pack(effects_pack):
    """Selects an audio effects pack for your persona."""
    if effects_pack not in audio.get_available_packs():
        click.echo(_render_emoji("❌ ") + _render_colored([("Invalid audio effects pack:", "red"), (effects_pack, "magenta")]))
        return
    personas.persona.audio_effects_pack = effects_pack
    personas.save()
    click.echo(_render_emoji("🔊 ") + _render_colored([("Selected audio effects pack:", "green"), (effects_pack, "magenta")]))

@click.command("play")
@click.argument("effect", required=True, type=str)
def play_audio_effect(effect):
    """Plays an audio effect."""
    click.echo(_render_emoji("🔊 ") + _render_colored([("Playing audio effect:", "green"), (effect, "magenta"), ("from pack:", "green"), (personas.persona.audio_effects_pack, "magenta")]))
    audio.play_effect(effect)

@click.group("tts")
def tts():
    """Manages the text-to-speech engine of your persona."""
    pass

@click.command("enable-slow")
def enable_slow_tts():
    """Enables slow text-to-speech for your persona."""
    personas.persona.tts_slow = True
    personas.save()
    click.echo(_render_emoji("🗣 ") + _render_colored([("Enabled slow text-to-speech!", "green")]))

@click.command("disable-slow")
def disable_slow_tts():
    """Disables slow text-to-speech for your persona."""
    personas.persona.tts_slow = False
    personas.save()
    click.echo(_render_emoji("🗣 ") + _render_colored([("Disabled slow text-to-speech!", "green")]))

@click.command("list-languages")
@click.argument("language", required=False, type=str)
def list_tts_languages(language):
    """Lists all available text-to-speech languages."""
    click.echo(_render_emoji("💬 ") + _render_colored([("Available text-to-speech languages:", "green")]))
    printer.pretty_print_dict_vertical(txtts.get_available_languages())

@click.command("selected-language")
def selected_tts_language():
    """Lists the selected text-to-speech language."""
    try:
        click.echo(_render_emoji("💬 ") + _render_colored([("Selected text-to-speech language:", "green"), (txtts.get_available_languages()[personas.persona.tts_language], "magenta")]))
    except KeyError:
        click.echo(_render_emoji("❌ ") + _render_colored([("Invalid text-to-speech language:", "red"), (personas.persona.tts_language, "magenta")]))
        click.echo(_render_emoji("❌ ") + _render_colored([("Setting to default!", "red")]))
        personas.persona.tts_language = "en"

@click.command("select-language")
@click.argument("language", required=True, type=str)
def select_tts_language(language):
    """Selects a text-to-speech language for your persona."""
    if language not in txtts.get_available_languages_ids():
        click.echo(_render_emoji("❌ ") + _render_colored([("Invalid text-to-speech language:", "red"), (language, "magenta")]))
        return
    personas.persona.tts_language = language
    personas.save()
    click.echo(_render_emoji("💬 ") + _render_colored([("Selected text-to-speech language:", "green"), (language, "magenta")]))

@click.command("test")
@click.argument("text", required=False, type=str)
def test_tts(text):
    """Tests the text-to-speech engine of your persona."""
    if not text:
        text = "This is a test of ASPER's text-to-speech engine!"
    click.echo(_render_emoji("🔊 ") + _render_colored([("Testing text-to-speech engine with:", "green"), (text, "magenta")]))
    txtts.read_text(text)

@click.command("welcome-message")
@click.argument("message", required=False, type=str)
def welcome_message(message):
    """Shows or changes the welcome message of your persona."""
    if not message:
        click.echo(_render_emoji("👋 ") + _render_colored([("Welcome message:", "green"), (personas.persona.welcome_message, "magenta")]))
        return
    personas.persona.welcome_message = message
    personas.save()
    click.echo(_render_emoji("👋 ") + _render_colored([("Welcome message is now:", "green"), (personas.persona.welcome_message, "magenta")]))

@click.command("read-welcome-message")
def read_welcome_message():
    """Reads the welcome message of your persona."""
    click.echo(_render_emoji("👋 ") + _render_colored([("Reading welcome message:", "green"), (personas.persona.welcome_message, "magenta")]))
    txtts.read_text(personas.persona.welcome_message)



message_processor_settings.add_command(list_message_processor_settings)
message_processor_settings.add_command(add_message_processor_setting)
message_processor_settings.add_command(remove_message_processor_setting)

audio_effects.add_command(enable_audio_effects)
audio_effects.add_command(disable_audio_effects)
audio_effects.add_command(list_audio_effects_packs)
audio_effects.add_command(select_audio_effects_pack)
audio_effects.add_command(play_audio_effect)


tts.add_command(enable_slow_tts)
tts.add_command(disable_slow_tts)
tts.add_command(list_tts_languages)
tts.add_command(selected_tts_language)
tts.add_command(select_tts_language)
tts.add_command(test_tts)



persona.add_command(list_personas)
persona.add_command(selected_persona)
persona.add_command(select_persona)
persona.add_command(destroy_persona)
persona.add_command(change_persona_name)
persona.add_command(change_persona_description)
persona.add_command(change_persona_author)
persona.add_command(list_hotwords)
persona.add_command(change_hotword_engine)
persona.add_command(change_hotword_model)
persona.add_command(change_assistant_engine)
persona.add_command(change_assistant_model)
persona.add_command(change_message_processor)
persona.add_command(message_processor_settings)
persona.add_command(disabled_user_commands)
persona.add_command(disabled_assistant_commands)
persona.add_command(audio_effects)
persona.add_command(tts)
persona.add_command(welcome_message)
persona.add_command(read_welcome_message)