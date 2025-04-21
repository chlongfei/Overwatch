""" Application Webserver
"""

from flask import Flask, Response, request, render_template
from ov import OV

app = Flask(__name__)


# Application - Main
@app.route('/')
def route_show_nearby_videogrid():
    """ serves default nearby video grid
    """
    return render_template('nearby-videogrid.html')


# Application - Misc.
@app.route('/nearby')
def route_show_nearby_table():
    """ Serves the nearby cameras in a table
    """
    return render_template('nearby-table.html')

@app.route('/source')
def route_show_sources():
    """ Servces table of sources in database
    """
    return render_template('sources.html')

@app.route('/source/<sourceID>')
def route_show_entities(sourceID):
    """ Serves table of entities specified by source
    """
    return render_template('entities.html', sourceid = sourceID)


# API
@app.route('/api')
def api_henlo():
    """ Henlo
    """
    return Response(status=200)

@app.route('/api/source')
def api_sources():
    """ Returns JSON list of all sources
    """
    if (request.method == 'GET'):
        return OV.getAllSources()
    else:
        return Response(status=500)
    
@app.route('/api/source/<sourceID>')
def api_source_entities(sourceID):
    """ Returns JSON list of entities under specified source
    """
    if (request.method == 'GET'):
        return OV.getEntitiesBySource(sourceID)
    else:
        return Response(status=500)

@app.route('/api/entity/<entityID>')
def api_source_entity(entityID):
    if (request.method == 'GET'):
        return OV.getEntity(entityID)
    else:
        return Response(status=500)


@app.route('/api/entity/<geoLat>/<geoLon>')
def api_source_entity_nearby(geoLat,geoLon):
    if (request.method == 'GET'):
        return OV.getEntitiesNearby(1, geoLat,geoLon)
    else:
        return Response(status=500)