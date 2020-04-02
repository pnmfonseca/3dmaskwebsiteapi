import config
import logging
from os import environ
from flask import (
    request, jsonify
 )
from config import (
    logger, app, db, Result, secured,
    Entrega, Voluntario
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

        deletable = Entrega.query.filter(Entrega.id == pID).first()

        if deletable:
            db.session.delete(deletable)
            db.session.commit()
        else:
            logger.warning("ID [{}] not found".format(pID))

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


def buildListOfVoluntarioFromPayload(pData):

    listOfVoluntario = []

    try:

        for _data in pData:

            _nome = _data.get("nome")

            if (_nome):
                listOfVoluntario.append(
                    Voluntario(
                        nome=_nome
                    )
                )

    except Exception as ex:
        logger.error(str(ex))

    return listOfVoluntario


@app.route('/voluntario', methods=['GET'])
@secured()
def listVoluntario():
    voluntarios = Voluntario.query.all()
    voluntarios = jsonify(voluntarios)
    return voluntarios


@app.route('/voluntario', methods=['POST'])
@secured()
def insertVoluntario():

    _status = Result.SUCCESS
    try:

        payload = request.get_json()
        print(payload)
        voluntarios = buildListOfVoluntarioFromPayload(payload.get("data"))

        for voluntario in voluntarios:
            db.session.add(voluntario)

        db.session.commit()

    except Exception as ex:
        logger.warning(str(ex))
        _status = Result.FAILURE

    return Result(status=_status).toJSON()


@app.route('/voluntario/id/<pID>', methods=['DELETE'])
@secured()
def deleteVoluntario(pID):
    _status = Result.SUCCESS
    try:

        deletable = Voluntario.query.filter(Voluntario.id == pID).first()

        if deletable:
            db.session.delete(deletable)
            db.session.commit()
        else:
            logger.warning("ID [{}] not found".format(pID))

    except Exception as ex:
        logger.warning(str(ex))
        _status = Result.FAILURE

    return Result(status=_status).toJSON()


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

    print(config.getAppConfig("SQLALCHEMY_DATABASE_URI"))

    useDebug = config.getLandscape() == "sandbox"
    usePort = 5000 if useDebug else None
    config.setupLogger()
    print("\n" * 2)
    logging.warning('=== Launching 3DMask Web API ({}) ==='
                    .format(config.getLandscape()))
    app.run(debug=useDebug, use_reloader=True, port=usePort, host="0.0.0.0")
