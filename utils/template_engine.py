class Template():

    _template_text = ""
    _placeholder_headers = []

    _placeholder_prefix = "{"
    _placeholder_suffix = "}"

    def __init__(self, template_text, placeholder_prefix="{", placeholder_suffix="}"):
        self._template_text = template_text
    
    def set_placeholder_prefix(self, prefix):
        self._placeholder_prefix = prefix

    def set_placeholder_suffix(self, suffix):
        self._placeholder_suffix = suffix

    def set_placeholder_headers(self, headers):
        self._placeholder_headers = headers

    # If placeholders are a list of lists than assume that the first element of nested list is a heder (value to be replaced)
    # and the second element is the value to replace the header with (can be a string or a function that returns a string)
    # If placeholders are a list of strings than assume that the string is a value to replace the header with and value to replace is element of _placeholder_headers with the same index
    def _process_placeholders(self, placeholders):
        temp = self._template_text
        if placeholders == None:
            return temp
        if isinstance(placeholders, list):
            if isinstance(placeholders[0], list):
                for placeholder in placeholders:
                    temp = temp.replace(self._placeholder_prefix + placeholder[0] + self._placeholder_suffix, placeholder[1])
            else:
                for i in range(len(placeholders)):
                    temp = temp.replace(self._placeholder_prefix + self._placeholder_headers[i] + self._placeholder_suffix, placeholders[i])
        return temp

    def render(self, placeholders):
        temp = self._template_text
        for i in range(len(placeholders)):
            temp = temp.replace(self._placeholder_prefix + self._placeholder_headers[i] + self._placeholder_suffix, placeholders[i])
        return temp

    def render_with_headers(self, placeholders):
        temp = self._template_text
        for i in range(len(placeholders)):
            temp = temp.replace(self._placeholder_prefix + placeholders[i][0] + self._placeholder_suffix, placeholders[i][1])
        return temp
        