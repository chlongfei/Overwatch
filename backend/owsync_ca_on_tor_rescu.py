"""Middleware syncronization script for City of Toronto RESCU datasource
Implementing the owsync, this module performs database updates for the
City of Toronto RESCU traffic camera opendata datasourec.

March 2024

lchen@chlf.dev

Reference:
    https://open.toronto.ca/dataset/traffic-cameras/
"""
import requests, csv, json
from owsync import OWSYNC

class CA_ON_TOR_RESCU(OWSYNC):
    
    def __init__(self):
        super().__init__("ca-on-tor-rescu")

    def _getData(self):
        baseUrl = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
        dataStreamUrl = baseUrl + "/api/3/action/package_show"
        params = { "id": "traffic-cameras"}
        package = requests.get(dataStreamUrl, params = params).json()
        
        camCsv = None

        for resource in package["result"]["resources"]:
            if resource["datastore_active"]:
                camCsv = requests.get(resource["url"]).text
                break

        print(self._entityName,":: reterived camera csv from OpenData source")

        #read in csv  and convert into tcbase array list format
        camReader = list(csv.reader(camCsv.split('\n'), delimiter=','))

        print(self._entityName,":: adding cameras to database")

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
                camLon = camCoords[0]
                camLat = camCoords[1]
            except Exception as err:
                print("an error happend::", err)

            friendlyName = str(mainroad + "/" + crossroad)

            self._addCamera(camNo, friendlyName, None, camLat, camLon, "s", camBaseUri, "y")
            print(self._entityName,":: added camera (", camNo, ")",friendlyName)
