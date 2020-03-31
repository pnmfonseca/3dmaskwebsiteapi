from sys import platform
from os import environ
import pathlib
import sys
import logging
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask import Flask, request
from dataclasses import dataclass, field
import datetime
from flask.json import JSONEncoder
from sqlalchemy.sql import func

print("= config =" * 3)

logger = logging.getLogger(__name__)


class CustomJSONEncoder(JSONEncoder):
    "Add support for serializing timedeltas"

    def default(self, o):
        if type(o) == datetime.timedelta:
            return str(o)
        elif type(o) == datetime.datetime:
            return o.isoformat()
        else:
            return super().default(o)


app = Flask(__name__)

app.json_encoder = CustomJSONEncoder

api_version = '/api/v1'
app.config["LOG_FILE_NAME"] = "3dmaskapi-sandbox.log"
app.config["LOG_FILE_NAME_QA"] = "3dmaskapi-qa.log"
app.config["LOG_FILE_NAME_PRD"] = "3dmaskapi-prd.log"
app.config["LOG_FILE_UNIX_PATH"] = "./"
app.config["AUTH_TOKEN"] = "MASK_TOKEN"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}@localhost/mask"
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
        format="%(asctime)s||%(levelname)s||%(filename)s||%(lineno)s||%(funcName)s()||%(message)s",
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


def secured():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                if request.headers.get('Authorization') == \
                        environ.get(getAppConfig("AUTH_TOKEN")):
                    return f(*args, **kwargs)
                else:
                    return Result(status="error", message="Not authorized")\
                        .toJSON(), 401
            except Exception as ex:
                logger.error(str(ex))
                return Result(status="error", message="Not authorized")\
                    .toJSON(), 401

        return wrapped
    return wrapper


@dataclass
class Entrega(db.Model):
    id: int
    when: datetime = field(default_factory=datetime)
    deliveredTo: str
    amount: int

    id = db.Column(db.Integer, primary_key=True)
    when = db.Column(db.DateTime(timezone=True), server_default=func.now())
    deliveredTo = db.Column(db.String(120), unique=False)
    amount = db.Column(db.Integer, primary_key=False)

    def __init__(self, deliveredTo, amount):
        self.deliveredTo = deliveredTo
        self.amount = amount


class Result():
    # TODO Deprecate this

    SUCCESS = app.config["STR_SUCCESS"]
    FAILURE = app.config["STR_FAILURE"]
    status = ""
    data = []

    def __init__(self, **kwargs):

        data = kwargs.get("data", [])

        if type(data) != list:
            data = [data]

        self.status = kwargs.get("status", self.FAILURE)
        self.data = data

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
            "data": _data
        }
