"""
Description: Module to read configuration from a file which is in the format of win ini file.
"""

import configparser

class Config:
    """
    Class to read configuration from a file which is in the format of win ini file. 
    """
    def __init__(self, config_file):
        """
        Initialize the configuration object.
        :param config_file: Path to the configuration file.
        """
        self.config_file = config_file
        self.parser = configparser.ConfigParser()
        self.parser.read(config_file)

    def get(self, section, key):
        """
        Method to get the value of a key in a section.
        :param section: Section in the configuration file.
        :param key: Key in the section.
        """
        if key not in self.parser[section]:
            raise KeyError(f"Key '{key}' not found in the configuration.")
        return self.parser[section][key]

    def set(self, section, key, value):
        """
        Method to set the value of a key in a section.
        :param section: Section in the configuration file.
        :param key: Key in the section.
        :param value: Value to set.
        """
        if not self.parser.has_section(section):
            self.parser.add_section(section)
        self.parser[section][key] = value

    def sections(self):
        """Method to get all the sections in the configuration file."""
        return self.parser.sections()

    def save(self):
        """
        Method to save the current configuration to the file.
        """
        with open(self.config_file, 'w', encoding='utf-8') as configfile:
            self.parser.write(configfile)
