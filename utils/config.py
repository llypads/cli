import configparser

class Config(object):
    def __init__(self, path, account):
        self.path = path
        self.account = account
        self.config = configparser.ConfigParser()
        self.config.read(self.path)
        self.attributes = self.config[self.account]

    def write(self):
        with open(self.path, 'w') as configfile:
            self.config.write(configfile)
            print('Wrote config to: %s' % self.path)
