from owdb import OWDB
from owsync_coordinator import OWSyncCoordinator
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

"""Flask web server for Overwatch backend API

    lchen@chlf.dev
    January 2024

    Usage:
        python ./owbackend.py
"""

# initialize Overwatch DB connector
db = OWDB()

# init OWSync Connector
owsync = OWSyncCoordinator()

# initialize Flask and CORS
app = Flask(__name__)
CORS(app)

## UTILITY FUNCTIONS ##
def __isLocal() -> bool:
    return (request.remote_addr == "127.0.0.1")
        

## ROUTES ##
@app.route('/')
def henlo():
    """Root path handler.
    it's useful for checking if the server's alive.

    API:
        GET /
        
    Response:
        200 OK
    """
    return 'OK',200


## ENTITY OPS ##
@app.route('/entity')
def getEntities():
    """Serves a json list of all entities in the database

    API:
        GET /entity
    
    Response:
        JSON body containing all entities in the database
    """
    return jsonify(db.getEntity(asJSON=True))


@app.route('/entity/id/<id>')
def getEntityByID(id):
    """Serves the entity identitfied by ID

    API:
        GET /entity/id/<id>

    Params:
        id: id of the entity to reterive
    
    Response:
        JSON body containing the entity
    """
    return jsonify(db.getEntityByID(id, asJSON=True))


@app.route('/entity/name/<name>')
def getEntityByName(name):
    """Serves the entity identitfied by name

    API:
        GET /entity/name/<name>

    Params:
        name: name of the entity to reterive
    
    Response:
        JSON body containing the entity
    """
    return jsonify(db.getEntityByName(name, asJSON=True))

## CAMERA OPS ##
@app.route('/cams')
def getCameras():
    """Serves the entire camera database to client
    This action is crazy costly especially on the client, probably shouldn't use this in production.

    API:
        GET /cams

    Response:
        JSON body containing all the cameras in the database.
    """
    return jsonify(db.getCameras(asJSON=True))


@app.route('/cams/id/<id>')
def getCamerasByID(id):
    """Serves the camera identified by ID
    
    API:
        GET /cams/id/<id>
    
    Param:
        id: id of the camera to reterive

    Response:
        JSON body containing the camera identified by id
    """
    return jsonify(db.getCameraById(id, asJSON=True))


@app.route('/cams/friendly/<friendly>')
def getCamerasByFriendly(friendly):
    """Serves the camera identified by friendly name
    
    API:
        GET /cams/friendly/<friendly>
    
    Param:
        friendly: friendly name of the camera to reterive

    Response:
        JSON body containing the camera identified by friendly name
    """
    return jsonify(db.getCamerasByFriendly(friendly, asJSON=True))


@app.route('/cams/geo/<lat>/<lon>')
def getCamerasByGeopoint(lat, lon):
    """Serves the camera identified by geographic coordinates
    
    API:
        GET /cams/geo/<lat>/<lon>
    
    Param:
        lat: geographical lattitude of camera
        lon: geographical longitude of camera

    Response:
        JSON body containing the camera identified by geographic coordinates
    """
    return jsonify(db.getCamerasByGeo(lat, lon, asJSON=True))


#TODO:
@app.route('/cams/update/<id>')
def updateCamera(id):
    return 'FUTURE FEATURE', 501


#TODO:
@app.route('/cams/del/<id>')
def delCamera(id):
    return 'FUTURE FEATURE', 501


@app.route('/cams/geo/<lat>/<lon>/<rad>')
def getCameraNearGeopoint(lat, lon, rad):
    """Serves list of cameras within specified radius of geopoint

    API:
        GET /cams/geo/<lat>/<lon>/<rad>
    
    Params:
        lat: lattitude
        lon: longitude
        rad: radius in KM

    Response:
        JSON list of all cameras within {rad}KM of geopoint ordered by distance from geopoint.
    """
    return jsonify(db.getCamerasNearGeopoint(lat,lon,rad))


## SYNC APIs (localhost accessible only)##
@app.route('/util/sync/full')
def initSyncFull():
    """Initiates a full sync of dataset for every registered entity
    Essentially replaces evey camera under each registered entity.

    API:
        GET /util/sync/full

    Response:
        "200 OK" on successful sync
        "500 Internal Server Error" on failed sync    
    """

    if __isLocal():
        owsync.fullSync()
        return "SYNC SUCCESS", 200
    else:
        return "FORBIDDEN", 403


@app.route('/util/sync/delta')
def initSyncDelta():
    """Initiates a delta sync of dataset for every registered entity
    Updates camera records that have changed and adds new cameras available from datastream for every entity.

    API:
        GET /util/sync/delta

    Response:
        "200 OK" on successful sync
        "500 Internal Server Error" on failed sync    
    """
    if __isLocal():
        owsync.deltaSync()
        return "SYNC SUCCESS", 200
    else:
        return "FORBIDDEN", 403


@app.route('/util/sync/full/<ent>')
def initEntSyncFull(ent):
    """Initiates a full sync for specified entity
    Replaces all the cameras associated with the entity.
    Entity must be already registered in the application.

    API:
        GET /util/sync/full/<ent>

    Params:
        ent: entity ID
    
    Response:
        "200 OK" on successful sync
        "500 Internal Server Error" on failed sync    
    """
    if __isLocal():
        entName = db.getEntityByID(ent, asJSON=True)["name"]
        owsync.fullSyncByEntity(entName)
        return "SYNC SUCCESS", 200
    else:
        return "FORBIDDEN", 403


@app.route('/util/sync/delta/<ent>')
def initEntSyncDelta(ent):
    """Initiates a delta sync for specified entity
    Updates camera records that have changed and adds new cameras available from datastream associated with the entity specified.
    Entity must be already registered in the application.

    API:
        GET /util/sync/delta/<ent>

    Params:
        ent: entity ID
    
    Response:
        "200 OK" on successful sync
        "500 Internal Server Error" on failed sync    
    """
    if __isLocal():
        entName = db.getEntityByID(ent, asJSON=True)["name"]
        owsync.deltaSyncByEntity(entName)
        return "SYNC SUCCESS", 200
    else:
        return "FORBIDDEN", 403



## SERVE FLASK ##
if __name__ == '__main__':
    from waitress import serve
    serve(app,host='0.0.0.0',port=8573)