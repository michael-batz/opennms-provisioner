"""
opennms-provisioner config module

This module is for accessing the configuration of
opennms-provisioner.

:license: MIT, see LICENSE for more details
:copyright: (c) 2018 by Michael Batz, see AUTHORS for more details
"""
import configparser

class AppConfig(object):
    """ An AppConfig object.

    This class handles access to an INI-styled configuration file.

    Attributes:
        filename: ame of the configuration file to load
    """

    def __init__(self, filename):
        """ creates a new instance """
        self.__config = configparser.ConfigParser()
        self.__config.read(filename)

    def get_sections(self, prefix):
        """ return a list with all sections having the given prefix"""
        output = []
        for section in self.__config.sections():
            if section.startswith(prefix):
                output.append(section[len(prefix):])
        return output

    def get_value(self, section, key, default):
        """ return a value from configuration.

        Return a value from configuration. If the value does
        not exist, the default value will be returned.

        Parameters:
            section: configuration section
            key: key of the configuration option
            default: default value to use, if the option does not
                exist in configuration.
        """
        return self.__config.get(section, key, fallback=default)

    def get_value_boolean(self, section, key, default):
        """ return a value from configuration as boolean.

        Return a value from configuration as boolean. If the
        value does not exist, the default value will be returned.

        Parameters:
            section: configuration section
            key: key of the configuration option
            default: default value to use, if the option does not
                exist in configuration.
        """
        return self.__config.getboolean(section, key, fallback=default)

    def get_section(self, section):
        """ return a dictionary with all configuration items of the given section """
        output = {}
        for option in self.__config[section]:
            output[option] = self.__config[section][option]
        return output
