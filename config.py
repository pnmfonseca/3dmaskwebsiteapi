from sys import platform
from os import environ
import pathlib
import sys
import logging
from flask_sqlalchemy import SQLAlchemy
from flask import (
    Flask,
    make_response
)
print("= config =" * 3)

logger = logging.getLogger(__name__)

app = Flask(__name__)

api_version = '/api/v1'
app.config["LOG_FILE_NAME"] = "3dmaskapi-sandbox.log"
app.config["LOG_FILE_NAME_QA"] = "3dmaskapi-qa.log"
app.config["LOG_FILE_NAME_PRD"] = "3dmaskapi-prd.log"
app.config["LOG_FILE_UNIX_PATH"] = "./"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}@localhost/mask"
app.config["SQLALCHEMY_DATABASE_URI_QA"] = "mysql+pymysql://{}@localhost/mask"
app.config["SQLALCHEMY_DATABASE_URI_PRD"] = "mysql+pymysql://{}@localhost/mask"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["STR_SUCCESS"] = "success"
app.config["STR_FAILURE"] = "failure"

db = SQLAlchemy(app)


def setupLogger():

    _logFileName = getAppConfig("LOG_FILE_NAME")
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
        level=logging.INFO,
        format='''%(asctime)s||%(levelname)s||%(filename)s||%(lineno)s
                ||%(funcName)s()||%(message)s''',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        handlers=handlers
    )

    logger = logging.getLogger(__name__)
    logger.warn("Logging under {}".format(platform))
    logger.warn("Log file is [{}]".format(_logFileFQN))


def getAppConfig(pName):

    ret = None

    try:

        ret = app.config[("{}_{}".format(pName, getLandscape())).upper()]

    except Exception:
        ret = app.config[pName]

    finally:
        return ret


def getLandscape():

    _env = environ.get("MASK_LANDSCAPE", "sandbox").lower()
    if _env in ("dev", "qa", "prd", "sandbox"):
        return _env
    else:
        return "sandbox"


class Tester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(80), unique=False)

    def __init__(self, msg):
        self.msg = msg

    def toJSON(self):

        json = {
            "id": str(self.id),
            "msg": self.msg
        }

        return json


class Result():

    SUCCESS = "success"
    FAILURE = "failure"
    status = ""
    # message = ""
    data = []

    def __init__(self, **kwargs):

        data = kwargs.get("data", [])

        if type(data) != list:
            data = [data]

        self.status = kwargs.get("status", "failure")
        self.data = data
        # self.message = \
        #       kwargs.get("message", "{} rows".format(self.dataCount()))

    def noDataFound(self):
        return len(self.data) == 0

    def dataCount(self):
        # print(self.data)
        return len(self.data)

    def toJSON(self):

        _data = self.data

        if not self.data:
            _data = None

        return {
            "status": self.status,
            # "message": self.message,
            "data": _data
        }

    def response(self):
        return make_response(self.toJSON(), 200)
