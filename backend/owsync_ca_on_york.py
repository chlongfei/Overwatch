"""Middleware syncronization script for York Region traffic camera datasource

Implementing the owsync, this module performs databse updates for the York Region
traffic camera open-data datasource.

May 2024
lchen@chlf.dev

Reference: https://insights-york.opendata.arcgis.com/datasets/york::traffic-camera/about
"""

import requests
from owsync import OWSYNC

class CA_ON_YORK(OWSYNC):

    def __init__(self):
        super().__init__("owsync_ca_on_york")

    def _getData(self):
        dataUrl = "https://ww8.yorkmaps.ca/arcgis/rest/services/OpenData/Traffic/MapServer/0/query?outFields=*&where=1%3D1&f=geojson"
        data = requests.get(dataUrl).json()
        dataCams = data["features"]

        for cam in dataCams:
            camCoordinates = cam["geometry"]["coordinates"]
            camProperties = cam["properties"]
            self._addCamera(camProperties["FACILITYID"],
                            camProperties["cameralocation"],
                            None,
                            camCoordinates[0],
                            camCoordinates[1],
                            "s",
                            camProperties["photo"],
                            None
                            )
            
            print(self._entityName,":: added camera (", camProperties["FACILITYID"], ")",camProperties["cameralocation"])