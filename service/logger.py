from os import path, remove
import datetime

from .const import CONST

TYPES = ["debug","info","error","warn"]

class LoggerService:
    def __init__(self, debugMode:bool):
        self.filename = CONST.LOG_PATH
        if not path.exists(self.filename):
            self.createLog()
        self.debugMode = debugMode

    def addLogs(self,type:str,message:str):
        if type not in TYPES:
            raise Exception(f"Invalid type, types can be {TYPES}")
        with open(self.filename,"a") as f:
            f.write(f"[{type}] - {self.getDate()}] {message}\n")
        if self.debugMode and type == "debug":
            print(f"[{type}] - {self.getDate()}] {message}")
        elif not self.debugMode and type == "debug":
            pass
        else:
            print(f"[{type}] - {self.getDate()}] {message}")
    
    def getDate(self):
        return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def createLog(self):
        with open(self.filename,"w") as f:
            f.write("")

    def getLogs(self):
        with open(self.filename,"r") as f:
            return f.read()
        
    def clearLogs(self):
        self.createLog()
        return True
    
    def deleteLogs(self):
        if path.exists(self.filename):
            remove(self.filename)
            return True
        else:
            return False
        
    def getLogPath(self):
        return self.filename
