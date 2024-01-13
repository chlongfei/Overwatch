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


if __name__ == '__main__':
    app.run(host='0.0.0.0')