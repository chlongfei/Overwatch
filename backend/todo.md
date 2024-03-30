# `owdb.py`

## Bugs
1. `GET /util/sync/full/<ent>` produces `TypeError: list indices must be integers or slices, not str`

## Entity

- [x] Create
- [x] Read
    - [x] All
    - [x] by ID
    - [x] by Name
- [ ] Update
- [x] Delete
- [x] Exists
    - [x] by ID
    - [x] by Name

## Camera
- [x] Create
- [x] Read
    - [x] All
    - [x] Camera x ID
    - [x] Camera x Entity
    - [x] Camera x Friendly
    - [x] Camera x Geo
- [x] Update
- [x] Delete

## Queries
- [x] Camera within x Geo


# `owbackend.py`
- [ ] Entities
  - [ ] POST New Entity
  - [x] GET All
  - [x] GET by ID
  - [x] GET by Name
  - [ ] PUT (Update)
  - [ ] DELETE Entity
- [ ] Cameras
  - [ ] POST New Camera
  - [x] GET All
  - [x] GET by ID
  - [x] GET by Entity
  - [x] GET by Friendly
  - [x] GET by Geo
  - [ ] PUT (Update) Camera
  - [ ] DELETE Camera
- [X] GET cameras within x rad
- [x] INIT sync
  - [x] all
    - [x] delta
    - [x] full
  - [x] per entitiy
    - [x] delta
    - [x] full