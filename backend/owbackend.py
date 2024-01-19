from owdb import OWDB
from flask import Flask
from flask import jsonify
from flask_cors import CORS
import json

# init db connector
db = OWDB()

app = Flask(__name__)
CORS(app)

@app.route('/')
def henlo():
    return 'overwatch backend api<br>if you see this- service is running.'


# Camera Operations #

@app.route('/cams')
def getCameras():
    return jsonify(db.getCamerasJson())

@app.route('/cams/geo/<lon>/<lat>/<rad>')
def getCameraNearGeopoint(lon, lat, rad):
    return jsonify(db.getCameraNearGeopoint(lon,lat,rad))


if __name__ == '__main__':
    from waitress import serve
    serve(app,host='0.0.0.0',port=8573)