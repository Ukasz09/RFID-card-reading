class Terminal(object):
    def __init__(self, term_guid, name, is_engaged=False):
        self.term_guid = term_guid
        self.name = name
        self.is_engaged = is_engaged

    def __str__(self):
        return "Terminal GUID: " + self.term_guid + "\nTerminal name: " + self.name
