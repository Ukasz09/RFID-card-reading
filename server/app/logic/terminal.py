class Terminal(object):
    def __init__(self, term_guid, name, is_engaged=False):
        """
        :param term_guid: GUID of terminal
        :param name: Name of terminal
        :param is_engaged: bool value which indicate if terminal is free or engage
        """
        self.term_guid = term_guid
        self.name = name
        self.is_engaged = is_engaged

    def __str__(self):
        """
        :return: Text representation of RegistryLog object
        """
        return "Terminal GUID: " + self.term_guid + "\nTerminal name: " + self.name
