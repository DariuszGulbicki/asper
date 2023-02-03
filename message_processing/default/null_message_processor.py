from message_processing.message_processor import MessageProcessor

class null_message_processor(MessageProcessor):
    
        def initialize(self, config):
            self.config = config
    
        def get_processor_id(self):
            return "null"
    
        def get_processor_name(self):
            return "Null (default)"
        
        def get_processor_description(self):
            return "Message processor that does nothing"
        
        def get_processor_author(self):
            return "Dariusz Gulbicki"

        def process_message(self, message):
            return message

        def get_processor_version(self):
            return "1.0.0"