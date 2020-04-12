class Terminal(object):
    def __init__(self, term_guid, name):
        self.term_guid = term_guid
        self.name = name

    def __str__(self):
        return "Terminal GUID: " + self.term_guid + "\nTerminal name: " + self.name
