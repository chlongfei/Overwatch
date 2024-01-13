"""
    Overwatch Updater Middleware for City of Toronto RESCU datasource
    lchen@chlf.dev

    January 11, 2024

    https://open.toronto.ca/dataset/traffic-cameras/
    
"""

import requests
import csv
import json
from owdb import OWDB

entityName = "ca-on-tor-rescu"

# init db connection
db = OWDB()
entityId = None

# check if entity exists in db, reterives id if exist, create new otherwise
if (not db.entityExists(entityName)):
    entityId = db.addEntity(entityName)
    print(entityName,":: entity not exists - entity created", entityId)
else:
    entityId = list(db.getEntity(entityName)[0])[0]
    print(entityName,":: entity exists - id reterived", entityId)


# get active camera list
baseUrl = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
url = baseUrl + "/api/3/action/package_show"
params = { "id": "traffic-cameras"}
package = requests.get(url, params = params).json()

camCsv = None

for resource in package["result"]["resources"]:
    if resource["datastore_active"]:
        camCsv = requests.get(resource["url"]).text
        break

print(entityName,":: reterived camera csv from OpenData source")


#read in csv  and convert into tcbase array list format
camReader = list(csv.reader(camCsv.split('\n'), delimiter=','))

print(entityName,":: adding cameras to database")

for i in range(1,len(camReader)-1):
    cam = camReader[i]
    camNo = None
    camBaseUri = None
    camNorthUri = None
    camEastUri = None
    camSouthUri = None
    camWestUri = None

    mainroad = None
    crossroad = None

    camLat = None
    camLon = None

    # capture cam ID
    try:
        camNo = cam[1]
    except Exception as err:
        camNo = "[NoCam]"
        print("an error happend::", err)

    # capture cam base uri
    try:
        camBaseUri = cam[2]
    except Exception as err:
        camBaseUri = "[NoCamUri]"
        print("an error happend::", err)

    # capture cam compare North    
    try:
        camNorthUri = cam[3]
    except Exception as err:
        camNorthUri = None
        print("an error happend::", err)

    # capture cam compare East    
    try:
        camEastUri = cam[5]
    except Exception as err:
        camEastUri = None
        print("an error happend::", err)

    # capture cam mainroad 
    try:
        mainroad = cam[7]
    except Exception as err:
        mainroad = ""
        print("an error happend::", err)

    # capture cam crossroad
    try:
        crossroad = cam[8]
    except Exception as err:
        crossroad = ""
        print("an error happend::", err)

    # capture cam compare South    
    try:
        camSouthUri = cam[10]
    except Exception as err:
        camSouthUri = None
        print("an error happend::", err)

    # capture cam compare West    
    try:
        camWestUri = cam[12]
    except Exception as err:
        camWestUri = None
        print("an error happend::", err)

    # capture coordinates
    try:
        camCoords = json.loads(cam[14])["coordinates"]
        camLat = camCoords[0]
        camLon = camCoords[1]
    except Exception as err:
        print("an error happend::", err)

    friendlyName = str(mainroad + "/" + crossroad)
    db.addCamera(camNo, entityId, friendlyName, None, camLat, camLon, "s", camBaseUri, "y")
    print(entityName,":: added camera (", camNo, ")",friendlyName)