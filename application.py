import config
import logging
import json
from flask import (
    request
 ) #,send_from_directory, render_template, jsonify, make_response
from config import (
    logger
    , app, db, Result
    ,Tester
)


@app.route('/testinsertone', methods=['POST'])
def testInsertOne():

    msg = None
    stat = Result.SUCCESS
    try:
        
        data = request.get_json()

        
        if data.get("message"):
            record = Tester(data.get("message"))
            db.session.add(record)
            db.session.commit()

            msg = record.toJSON()

    except Exception as ex:
        pass
    
    return Result(data = msg, status = stat).response()
    
@app.route('/test', methods=[ 'GET','POST'])
def test():

    msg = None
    stat = Result.SUCCESS

    if request.method == "GET":
        msg ={"{}".format(request.method)}
        
    if request.method == "POST":
        msg ={"{}".format(request.method)}
        stat = Result.FAILURE

    return Result(data = msg, status = stat).response()    

@app.route('/createtables', methods=[ 'POST'])
def resetTables():

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
        
    return Result(data = msg, status = stat ).toJSON()    

if __name__ == "__main__":
    useDebug = app.config["APP_ENV"] == "development"
    usePort = 5000 if useDebug else None
    config.setupLogger()
    print("\n" * 2)
    logging.warning('=== Launching 3DMask Web API ===')
    app.run(debug=useDebug, use_reloader=True, port=usePort)