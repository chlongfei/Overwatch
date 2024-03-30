# Overwatch
Traffic camera database for serving publically accessible camera streams via OpenData.

## Sources Supported
 - [x] City of Toronto RESCU
 - [ ] Ministry of Transportation Ontario

## `.env`
The database is defined in the .env file, the following parameters must be defined before attempting to build the docker stack.

- `DB_HOST`: hostname of the database container, leave this as `owdb` unless you defined it in `compose.yaml`
- `MYSQL_DATABASE`: name of the database that Overwatch will use
- `MYSQL_USER`: database non-root user username
- `MYSQL_PASSWORD`: database non-root user password, give it something long and random
- `MYSQL_ROOT_PASSWORD`: database root user password, give it something long and random

## Usage
By default the flask web-server listens at `*:8573` this was chosen arbitrily, if you want to change it to something else. Remember to change it both in `backend/owbackend.py` and in `compose.yaml`.

### SSL
It is always recommended to utilize HTTPS. I found it easiest to utilize NGINX to operate a reverse proxy to the exposed port of the docker container.

See [NGINX documentation](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/) 

## API
### `GET /`
Doesn't do anything. Just returns 200 OK telling you that the server is working.

### `GET /entity`
Returns JSON list of entities.

### `GET /entity/id/<id>`
Returns JSON list with the specified entity identified by `camID`.

### `GET /entity/name/<name>`
Return JSON list with the specific entity identified by `friendly`.

### `GET /cams`
Returns JSON list of all cameras.

### `GET /cams/id/<id>`
Returns JSON list with specific camera identified by `camID`.

### `GET /cams/friendly/<friendly>`
Returns JSON list with specific camera identified by `friendly` name.

### `GET /cams/geo/<lat>/<lon>`
Returns JSON list with specific camera identified by the latitude and longitude of the camera.

### `GET /cams/update/<id>`
> Not yet implemented. Returns 501.

Updates the record for the specific camera identified by `camID`.

### `GET /cams/del/<id>`
> Not yet implemented. Returns 501.

Deletes camera identified by `camID`.

### `GET /cams/geo/<lat>/<lon>/<rad>`
Returns JSON list of cameras within `rads` radius of `lat` and `lon`.

### `GET /util/sync/full`
>This function is only permitted from localhost. 403 Forbidden returned otherwise.

Initiates a full sync across all entities.

### `GET /util/sync/delta`
>This function is only permitted from localhost. 403 Forbidden returned otherwise.

Initiates a delta sync across all entities.

### `GET /util/sync/full/<ent>`
>This function is only permitted from localhost. 403 Forbidden returned otherwise.

Inititates a full sync on the specified entity.

### `GET /util/sync/delta/<ent>`
>This function is only permitted from localhost. 403 Forbidden returned otherwise.

Initiates a delta sync on the specific entity.