import configparser

class AppConfig(object):

    def __init__(self, filename):
        self.__config = configparser.ConfigParser()
        self.__config.read(filename)
    
    def get_sections(self, prefix):
        output = []
        for section in self.__config.sections():
            if section.startswith(prefix):
                output.append(section[len(prefix):])
        return output

    def get_value(self, section, key, default):
        return self.__config.get(section, key, fallback=default)

    def get_section(self, section):
        output = {}
        for option in self.__config[section]:
            output[option] = self.__config[section][option]
        return output
