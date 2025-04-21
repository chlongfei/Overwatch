# Overwatch Service
Backend service that powers the Overwatch application.

```
web.py      -   flask web server serving api and frontends
ovsync.py   -   abstract class to be inherited by syncronization scripts
ocsync_*.py -   syncronization scripts that inherit OVSYNC class
ovdb.py     -   utiilty class for interfacing with the mySQL database
ovcli.py    -   simple commandline interface for Overwatch application
ovcli.help  -   help text for when `help` is entered in cli
ov.py       -   main application functions
dockerfile  -   service definition for service container
templates/  -   template html files served by flask
static/     -   folder of static elements served by flask (images, css,  js, etc)

```

# API
The API calls are handled by flask at the root endpoint `/api`.

> APIs return 403 Forbidden when directly called upon from browser. CORS is also enforced.

## `GET /`
Simple health check returns `200 OK` telling applicaiton that service is running.

## `GET /source`
Returns a JSON array containing all sources that exist in the database.

**Schema**
```json
[
    {
        "entity_count": int,
        "id": int,
        "origin": string,
        "origin_url": string,
        "source_name": string,
        "source_type": string
    },
    ...
]
```
**Definitions:**
- `entity_count` - numeric count of number of entities associated with the source
- `id` - database issued ID to the source
- `origin` - type of data, such as Open Data, API, web scrape, etc.
- `origin_url` - url to the datasource
- `source_name` - name of the source
- `source_type` - type of the source, such as city, prov, 511, etc.

## `GET /source/<sourceID>`
Returns a JSON array of all entities belonging tot he specified source.

**Schema**
```json
[
    {
        "additional_view_east": string,
        "additional_view_north": string,
        "additional_view_south": string,
        "additional_view_west": string,
        "geo_lat": float,
        "geo_lon": float,
        "id": int,
        "media_id": string,
        "media_name": string,
        "media_source": string,
        "media_type": string,
        "source_id": int
    },
    ...
]

```
**Definitions:**
- `additional_view_east` - URL to additional images from this view such as directionals
- `additional_view_north` - URL to additional images from this view such as directionals
- `additional_view_south` - URL to additional images from this view such as directionals
- `additional_view_west` - URL to additional images from this view such as directionals
- `geo_lat` - geographical lattitude of the entity
- `geo_lon` - geographical longitude of the entity
- `id` - database issued ID for the entity (unique to application)
- `media_id` - facility issued id for the entity (unique to the source)
- `media_name` - name of the entity
- `media_source` - URI to main image for entity
- `media_type` - type of image source, such as static, video, etc.
- `source_id` - ID of the source entity associated with

## `GET /entity/<geoLat><geoLon>`
Returns a JSON array of all entities within 1km of provided lattitude and longitude

**Schema**
```json
[
    {
        geo_lat: float,
        geo_lon: float,
        id: int,
        media_id: string
        media_name: string
        media_source: string,
        media_type: string,
        source_id: int,
        source_name: string,
        source_type: string
    },
    ...
]
```
**Definitions:**
- `geo_lat` - geographic lattitude of entity
- `geo_lon` - geographic longitude of entity
- `id` - database issued ID for the entity
- `media_id` - facility issued id for entity
- `media_name` - name of entity
- `media_source` - URI to main image of entity
- `media_type` - type of image source, such as static, video, etc.
- `source_id` - ID of the source entity associated with
- `source_name` - name of source
- `source_type` - type of the source, such as city, prov, 511, etc.

# Entity Syncronization
#TODO: DO THIS PART
## `ovsync.py`
The abstract class ment to be inherited by all syncronization scripts for ingesting datasets.
See [README-Sync.md](README-Sync.md) for specifics on creating syncronization scripts and setting it up.


# Sources
- City of Toronto
    - https://opendata.toronto.ca/transportation/tmc/rescucameraimages/Data/tmcearthcameras.json
    - Camera Images: https://opendata.toronto.ca/transportation/tmc/rescucameraimages/CameraImages/loc####.jpg
    - Comparison Images: https://opendata.toronto.ca/transportation/tmc/rescucameraimages/ComparisonImages/loc####D.jpg