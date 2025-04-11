from flask import Flask, Response, request, render_template
from tl import TL

app = Flask(__name__)

# App Console
@app.route('/')
def route_root():
    return render_template('index.html')


# Admin Console
@app.route('/admin')
def route_admin_root():
    return render_template('admin/sources.html')


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
