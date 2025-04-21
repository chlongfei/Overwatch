""" Application Webserver
"""

from flask import Flask, Response, request, render_template
from flask_cors import CORS
from ov import OV

## Utilities
def isDirectlyAccessed():
    """ Checks if endpoint is being accessed outside of app
    Utilizing the referrer header, requests coming directly from browser usually would not
    have a referrer set. This is a simple way of checking and locking out direct API calls.
    """
    if (request.referrer == None):
        return True
    else:
        return False


## Web Server
app = Flask(__name__)
CORS(app)


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
    Simple health response that returns 200 when running.
    """
    if (isDirectlyAccessed()):
        return Response(status=403)
    else:
        return Response(status=200)

@app.route('/api/source')
def api_sources():
    """ Returns JSON list of all sources
    """
    
    if (isDirectlyAccessed()):
        return Response(status=403)  
    else:
        if (request.method == 'GET'):
            return OV.getAllSources()
        else:
            return Response(status=500)  
    
@app.route('/api/source/<sourceID>')
def api_source_entities(sourceID):
    """ Returns JSON list of entities under specified source
    """

    if (isDirectlyAccessed()):
        return Response(status=403)
    else:
        if (request.method == 'GET'):
            return OV.getEntitiesBySource(sourceID)
        else:
            return Response(status=500)

@app.route('/api/entity/<geoLat>/<geoLon>')
def api_source_entity_nearby(geoLat,geoLon):
    """ Returns JSON list of entities near provided geoLat and geoLon
    """
    
    if (isDirectlyAccessed()):
        return Response(status=403)
    else:
        if (request.method == 'GET'):
            return OV.getEntitiesNearby(1, geoLat,geoLon)
        else:
            return Response(status=500)