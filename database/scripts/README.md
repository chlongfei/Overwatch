# Overwatch <sub>DATABASE</sub>
> This does not actually contain a DBA, but rather the resources and scripts required to create it.

## Usage
Build the entire application stack utilizing docker compose and the `compose.yaml` file in the project root dir.

Database parameters are defined in the `.env` in the project root, and is identified int he `compose.yaml` file.

## Schema

```
Entity:
    id  (primary key)
    entityName
```

```
Cameras:
    id  (primary key)
    camID
    entity  (references Entity(id))
    friendly
    direction
    geoPoint
    streamType
    baseUrl
    hasAlt
    dHash
```

```
Camera_Alt:
    id (primary key)
    camera (references Cameras(id))
    uri
```