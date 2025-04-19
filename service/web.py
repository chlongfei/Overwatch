from flask import Flask, Response, request, render_template
from tl import TL

app = Flask(__name__)

# App Console
@app.route('/')
def route_root():
    return render_template('nearby.html')


# Admin Console
@app.route('/source')
def route_admin_root():
    return render_template('admin/sources.html')

@app.route('/source/<sourceID>')
def route_admin_entities(sourceID):
    return render_template('admin/entities.html', sourceid = sourceID)


# API
@app.route('/api')
def api_henlo():
    return Response(status=200)

@app.route('/api/source')
def api_sources():
    if (request.method == 'GET'):
        return TL.getAllSources()
    else:
        return Response(status=500)
    
@app.route('/api/source/<sourceID>')
def api_source_entities(sourceID):
    if (request.method == 'GET'):
        return TL.getEntitiesBySource(sourceID)
    else:
        return Response(status=500)

@app.route('/api/entity/<entityID>')
def api_source_entity(entityID):
    if (request.method == 'GET'):
        return TL.getEntity(entityID)
    else:
        return Response(status=500)


@app.route('/api/entity/<geoLat>/<geoLon>')
def api_source_entity_nearby(geoLat,geoLon):
    if (request.method == 'GET'):
        return TL.getEntitiesNearby(1, geoLat,geoLon)
    else:
        return Response(status=500)