import config
import logging
from os import environ
from flask import (
    request, jsonify
 )
from config import (
    logger, app, db, Result, secured,
    Entrega
)


@app.route('/entrega', methods=['GET'])
@secured()
def listEntrega():
    entregas = Entrega.query.all()
    entregas = jsonify(entregas)
    return entregas


@app.route('/entrega/id/<pID>', methods=['DELETE'])
@secured()
def delete(pID):
    _status = Result.SUCCESS
    try:

        db.session.commit()

    except Exception as ex:
        logger.warning(str(ex))
        _status = Result.FAILURE

    return Result(status=_status).toJSON()


@app.route('/entrega', methods=['POST'])
@secured()
def insert():

    _status = Result.SUCCESS
    try:

        payload = request.get_json()
        print(payload)
        entregas = buildListOfEntregaFromPayload(payload.get("data"))

        for entrega in entregas:
            db.session.add(entrega)

        db.session.commit()

    except Exception as ex:
        logger.warning(str(ex))
        _status = Result.FAILURE

    return Result(status=_status).toJSON()


def buildListOfEntregaFromPayload(pData):

    listOfEntrega = []

    try:

        for _data in pData:

            _deliveredTo = _data.get("local")
            _amount = _data.get("qtd")

            if (_deliveredTo and _amount):
                listOfEntrega.append(
                    Entrega(
                        deliveredTo=_deliveredTo,
                        amount=_amount
                    )
                )

    except Exception as ex:
        logger.error(str(ex))

    return listOfEntrega


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
