import config
import logging
from os import environ
from flask import (
    request, jsonify
 )
from config import (
    logger, app, db, Result, Tester, secured
)


@app.route('/test', methods=['POST'])
@secured()
def testInsertOne():

    msg = {}
    try:

        data = request.get_json()

        if data.get("message"):
            record = Tester(data.get("message"))
            db.session.add(record)
            db.session.commit()

            return jsonify(record)

    except Exception as ex:
        logger.error(str(ex))
        pass

    return msg


@app.route('/test', methods=['GET'])
@secured()
def test():

    msg = None
    stat = Result.SUCCESS

    if request.method == "GET":
        msg = "{}".format(request.method)

    return Result(data="this is a message", status=Result.SUCCESS).toJSON()
    return Result(data=msg, status=stat).toJSON()


@app.route('/test/id/<pID>', methods=['GET'])
@secured()
def testGetByID(pID):

    ret = Tester.query.filter(Tester.id == pID).all()
    if ret:
        return jsonify(ret)
    else:
        return Result().toJSON()


@app.route('/test/all', methods=['GET'])
@secured()
def testGetAll():
    tests = Tester.query.all()
    tests = jsonify(tests)
    return tests


@app.route('/createtables', methods=['POST'])
@secured()
def createTables():

    msg = None
    stat = None
    try:
        logger.warn("CREATING TABLES")
        db.create_all()
        msg = "Non existent tables created!"
        stat = Result.SUCCESS
    except Exception as ex:
        msg = str(ex)
        stat = Result.FAILURE

    return Result(data=msg, status=stat).toJSON()


if __name__ == "__main__":
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        config.getAppConfig("SQLALCHEMY_DATABASE_URI")\
        .format(environ.get("MASK_CREDENTIALS", "root:root"))
    useDebug = config.getAppConfig("3DMASK_LANDSCAPE") == "sandbox"
    usePort = 5000 if useDebug else None
    config.setupLogger()
    print("\n" * 2)
    logging.warning('=== Launching 3DMask Web API ({}) ==='
                    .format(config.getLandscape()))
    app.run(debug=useDebug, use_reloader=True, port=usePort, host="0.0.0.0")
