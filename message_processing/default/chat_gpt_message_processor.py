from message_processing.message_processor import MessageProcessor
from chatgpt_wrapper import ChatGPT
from logging_system import logger
from utils import text_to_speech as tts

class chat_gpt_message_processor(MessageProcessor):

    def _send_initial_prompt(self):
        init_prompt = "I want you to act as a voice assistant."
        try:
            init_prompt = self._config["initial_prompt"]
        except KeyError:
            logger.warn("No initial prompt found in config. Using default.", "Chat GPT Message Processor")
        return self._conversation.ask(init_prompt)

    def initialize(self, config):
        self._config = config
        logger.debug("Initializing Chat GPT message processor", "Chat GPT Message Processor")
        self._conversation = ChatGPT()
        logger.info("Chat GPT is ready", "Chat GPT Message Processor")
        init_ans = self._send_initial_prompt()
        return_func = "log"
        try:
            return_func = self._config["initial_prompt_return_function"]
        except KeyError:
            logger.warn("No initial prompt return function found in config. Using default.", "Chat GPT Message Processor")
        if return_func == "log":
            logger.info(init_ans, "Chat GPT Message Processor")
        elif return_func == "print":
            print(init_ans)
        elif return_func == "read":
            tts.read_text(init_ans)


    def get_processor_id(self):
        return "chat-gpt"

    def get_processor_name(self):
        return "Chat GPT (default)"
    
    def get_processor_description(self):
        return "Message processor that uses the ChatGPT model"

    def get_processor_author(self):
        return "Dariusz Gulbicki"
        
    def process_message(self, message):
        logger.info("Asking Chat GPT: " + message, "Chat GPT Message Processor")
        return self._conversation.ask(message)

    def get_processor_version(self):
        return "1.0.0"