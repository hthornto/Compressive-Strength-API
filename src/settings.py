import configparser
import sqlalchemy


class Config(object):
    config = configparser.ConfigParser()
    config.read("settings.ini")

    TESTING = True


class Development(Config):

    def __init__(self):
        SQL_ALCHEMY_BINDS = {}
        if "Projects Database" in self.config:
            # SQL_ALCHEMY_BINDS['Projects Database'] =
            pass


class Production(Config):
    pass
