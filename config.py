from sys import platform
from os import environ
import pathlib
import sys
from flask import (
    Flask
    ,make_response
    ,jsonify
    )
import jinja2
import logging
from flask_jwt import JWT
from datetime import timedelta
import logging
from logging.handlers import TimedRotatingFileHandler
import json
from flask_sqlalchemy import SQLAlchemy

print("= config =" * 3)

logger = logging.getLogger(__name__)

app = Flask(__name__)

api_version = '/api/v1'
app.config["APP_ENV"] = environ.get("FLASK_ENV", "production")
app.config["LOG_FILE_NAME"] = "api.log"
app.config["LOG_FILE_UNIX_PATH"] = "./"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/3dmask"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["STR_SUCCESS"] = "success"
app.config["STR_FAILURE"] = "failure"

db = SQLAlchemy(app)

class Tester(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    msg = db.Column(db.String(80), unique = False)

    def __init__ (self,msg):
        self.msg = msg
    
    def toJSON(self):
           
        json = {
            "id"           : str(self.id),
            "msg"          : self.msg
        }

        return json


class Dummy(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    msg = db.Column(db.String(80), unique = False)

    def __init__ (self,msg):
        self.msg = msg



class Result():

    SUCCESS = "success"
    FAILURE = "failure"
    status = ""
    #message = ""
    data = []

    def __init__(self,**kwargs):

        data = kwargs.get("data", [])

        if type(data) != list:
            data = [ data ]

        self.status = kwargs.get("status", "failure")
        self.data = data
        #self.message = kwargs.get("message", "{} rows".format(self.dataCount()))

    def noDataFound(self):
        return len(self.data) == 0

    def dataCount(self):
        #print(self.data)
        return len(self.data)

    def toJSON(self):

        _data = self.data
        
        if not self.data:
            _data = None
        
        return {
            "status": self.status,
            #"message": self.message,
            "data": _data
        }

    def response(self):
        return make_response(self.toJSON(),200)


def setupLogger():

    _logFileName = app.config["LOG_FILE_NAME"]
    _logFilePath = None
    _logFileFQN = None

    if platform == "linux" or platform == "linux2" or platform == "darwin":
        _logFilePath = app.config["LOG_FILE_UNIX_PATH"]
    elif platform == "win32":
        _logFilePath = app.config["LOG_FILE_WIN_PATH"]

    pathlib.Path(_logFilePath).mkdir(parents=True, exist_ok=True)

    _logFileFQN = "{}{}".format(_logFilePath, _logFileName)
    fileHandler = logging.FileHandler(filename=_logFileFQN)
    stdoutHandler = logging.StreamHandler(sys.stdout)

    handlers = [fileHandler, stdoutHandler]

    logging.basicConfig(
        level=logging.INFO
        ,format = "%(asctime)s||%(levelname)s||%(filename)s||%(lineno)s||%(funcName)s()||%(message)s"
        ,datefmt = '%m/%d/%Y %I:%M:%S %p'
        ,handlers=handlers        
    )

    logger = logging.getLogger(__name__)
    logger.warn("Logging under {}".format(platform))
    logger.warn("Log file is [{}]".format(_logFileFQN))

setupLogger()