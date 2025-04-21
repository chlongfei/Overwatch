# Overwatch
Simple web app that serves traffic cameras nearby.

> See README.md in each service directory for specifics.

## Deployment
Use docker compose to deploy the entire stack
```
docker compose up --build -d
```

## Demolition
Use docker compose to destroy the entire stack
```
docker compose down --volumes
```

## Re-Deployment
Use docker compose to destroy and rebuild the entire stack
```
docker compose down --volumes; docker compose up --build --force-rebuild -d
```