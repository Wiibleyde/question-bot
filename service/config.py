import yaml
from os import path

from .const import CONST
from .logger import LoggerService

class ConfigService:
    def __init__(self,filename):
        self.filename = filename
        if not path.exists(filename):
            self.createConfig()
        else:
            self.config = self.loadConfig

    def createConfig(self):
        with open(self.filename,"w") as f:
            config = {
                "bot_token":"Your discord bot token",
                "prefix":"Your bot prefix"
            }
            f.write(yaml.dump(config))

    def loadConfig(self):
        with open(self.filename,"r") as f:
            return yaml.load(f.read(),Loader=yaml.FullLoader)
        
    def getKey(self,key):
        return self.config[key]
    
    def setKey(self,key,value):
        self.config[key] = value
        self.saveConfig()
        return True
    
    def saveConfig(self):
        with open(self.filename,"w") as f:
            f.write(yaml.dump(self.config))
        return True
    
    def getConfig(self):
        return self.config
