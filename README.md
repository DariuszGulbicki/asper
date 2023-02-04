# ASPER Python Package

![Asper LOGO](https://github.com/DariuszGulbicki/asper/raw/main/images/asper_logo_mid.png)

ASPER (Assistant Personalities) is a Python package for quickly creating voice assistants. It provides an easy-to-use interface for building and customizing your own personal voice assistant.

## Contents

- [ASPER Python Package](#asper-python-package)
  - [Contents](#contents)
    - [Introduction](#introduction)
    - [Installation](#installation)
    - [Usage](#usage)
    - [API Reference](#api-reference)
      - [User command detection](#user-command-detection)
      - [Message processing](#message-processing)
      - [Assistant command parsing](#assistant-command-parsing)
    - [Examples](#examples)
    - [Contributing](#contributing)
    - [License](#license)

### Introduction

ASPER is designed to make it easy for developers to create their own voice assistants without needing to have extensive knowledge of natural language processing and speech recognition. The package provides a set of tools that handle the heavy lifting, so you can focus on building a unique and engaging assistant personality.

### Installation

To install ASPER, you can use pip:

```bash
pip install asper
```

### Usage

Run the following command to start the assistant:

```bash
asper run
```

You can also use the following commands to manage current assistants personality:

```bash
# Shows available commands
asper persona

# Creates a new personality or loads an existing personality
asper persona select <personality_name>

# Switches personas message processor
asper persona message_processor <processor_id>
```

You can view all available commands by running:

```bash
asper --help
```

### API Reference

Asper has three main stages (User command detection, message processing and assistant command parsing). When you say a hotword, the assistant is activated and starts listening for your command. Firstly users voice input is checked for user commands (e.g. "exit"). If no user command is detected or user command returns True, the message is passed to the message processor. The message processor is responsible for processing the message and returning a response. Then the response is parsed to a queue for assistant commands (e.g. "print"). If no assistant command is detected, the response is spoken by the assistant. Next, the assistant commands are executed and resulting text is read.

#### User command detection

User command detection is simple. If the first word of the users voice input matches a user command, the command is executed and the assistant is deactivated. Rest of the voice input is treated as arguments for the command.

You can create custom user commands by creating a new class in .py file in the asper directory (/home/username/.asper/user_commands/ or %APPDATA%/asper/user_commands/). The class must inherit from the CustomCommand class and implement the execute method. The execute method takes a string as an input and returns a boolean.

Here is a template for creating a new user command:

```python
from commands.custom_command import CustomCommand
from utils import text_to_speech as tts

class ExampleUserCommand(CustomCommand):
    
    # Returns a command name
    # When first word of the users voice input matches this command, the command is executed
    # Name is not case sensitive but SHOULD be written in lowercase
    def get_command(self):
        return "example"

    # Returns a command description
    def get_description(self):
        return "Says example and skips later stages"

    # Returns a command author
    def get_author(self):
        return "Example Author"

    # Returns a command version (number.number.number format)
    def get_version(self):
        return "1.0.0"

    # This method is executed when the command is detected
    # Returns False if the assistant should skip later stages
    def execute(self, args):
        tts.read_text("Example")
        return False
```

> **Note:** \
> User commands should only be used for system related tasks (e.g. exit, nothing, read).
> If you want to complete more complex tasks, you should code them into your message procesor or use an assistant command.

#### Message processing

Message processor is responsible for processing the message and returning a response. The message processor is set in the assistant settings. You can set the message processor by using the asper persona message_processor command. Message prrocessor can use an external API or service (e.g. chatbot) to provide responses. You can also create your own message processor by creating a new class in .py file in the asper directory (/home/username/.asper/processors/ or %APPDATA%/asper/processors/). The class must inherit from the MessageProcessor class and implement the process_message method. The process_message method takes a string as an input and returns a string. Here is an example of a message processor that returns the same message as the input (this is the default message processor called null):

```python
from message_processing.message_processor import MessageProcessor

class null_message_processor(MessageProcessor):
    
        # Uses initilization to load the config
        def initialize(self, config):
            self.config = config
    
        # Returns a processor id
        def get_processor_id(self):
            return "null"
    
        # Returns a processor name
        def get_processor_name(self):
            return "Null (default)"
        
        # Returns a processor description
        def get_processor_description(self):
            return "Message processor that does nothing"
        
        # Returns a processor author
        def get_processor_author(self):
            return "Dariusz Gulbicki"

        # This method is executed to process the message
        # In this case it returns the input
        def process_message(self, message):
            return message

        # Returns a processor version (number.number.number format)
        def get_processor_version(self):
            return "1.0.0"
```


#### Assistant command parsing

Assistant command parsing is similar to user command detection. Assistant commands are in form of XML tags. The assistant command is executed when the assistant reads the tag. Text inside the tag is passed as an argument to the command. If the execute function returns True the assistant will read the text inside the tag after executing the command. Here is an example of a string with an assistant command:

```xml
This is a <example>test</example> string.
```

You can create custom assistant commands by creating a new class in .py file in the asper directory (/home/username/.asper/assistant_commands/ or %APPDATA%/asper/assistant_commands/). The class must inherit from the CustomCommand class and implement the execute method. The execute method takes a string as an input and returns a boolean.

Here is a template for creating a new assistant command:

```python
from commands.custom_command import CustomCommand

class ExampleUserCommand(CustomCommand):
    
    # Returns a command name
    # When first word of the users voice input matches this command, the command is executed
    # Name is not case sensitive but SHOULD be written in lowercase
    def get_command(self):
        return "example"

    # Returns a command description
    def get_description(self):
        return "Prints example and skips later stages"

    # Returns a command author
    def get_author(self):
        return "Example Author"

    # Returns a command version (number.number.number format)
    def get_version(self):
        return "1.0.0"

    # This method is executed when the command is detected
    # Returns True if you want the assistant to read the text inside the tag after executing the command
    def execute(self, args):
        print("Example")
        return True
```

### Examples

Creating a new assistant. Setting assistant message processor to chatgpt and setting hotword to "hey test assistant".

```bash
# Create a new assistant (or select an existing one)
asper persona select new
# Set the assistant name, author, and description
asper persona name "Test Assistant"
asper persona author "Example Author"
asper persona description "New assistant created with ASPER"
# Set the assistant message processor to chatgpt
asper persona message_processor chat-gpt
# Clear the default hotwords and add a new one
asper persona hotwords --clear
# --add "hey test assistant." is used to detect a hotword even if it is at the end of a sentence
asper persona hotwords --add "hey test assistant" --add "hey test assistant."
asper run
```

> **Note:** \
> ChatGPT will not work by default since it relies on a library that is not included in the package. \
> This library uses webscraping to connect with chatgpt which may be against the website's terms of service. \
> **Use at your own risk** \
> To install the library, run the following command: \
> `pip install git+https://github.com/mmabrouk/chatgpt-wrapper` \
> Then run the following command to log in to chatgpt: \
> `chatgpt install` \

### Contributing

We welcome and encourage contributions to ASPER! There are many ways to get involved, such as fixing bugs, adding new features, improving documentation, and spreading the word.

If you would like to contribute to the development of ASPER, here are some guidelines to get started:

1. Check the existing issues on GitHub to see if your idea or bug report has already been submitted.
2. If you can't find an issue that matches your contribution, please create a new issue to describe it.
3. Fork the repository on GitHub.
4. Clone your fork to your local machine.
5. Create a new branch for your changes.
6. Make your changes and commit them to your branch.
7. Push your branch to your fork on GitHub.
8. Submit a pull request to the main repository, referencing the issue you created.

For new features, it is especially important to create an issue first so that we can discuss the design and implementation details before you start writing code. This helps to ensure that your contribution is a good fit for the project, and reduces the risk of wasting time on a feature that may not be accepted.

Please be sure to include a clear and concise description of your changes, and why they are necessary. We will review your pull request and provide feedback as soon as possible.

### License

ASPER is licensed under the [MIT License](https://opensource.org/licenses/MIT), which means that the software is open-source and free to use, distribute, and modify. The license includes certain restrictions, such as the requirement to include the original copyright notice and permission notice in any copies or substantial portions of the software. However, it also includes provisions for liability and warranty disclaimers, to protect users and contributors from potential legal issues.