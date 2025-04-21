/* CREATE VIEWS */

create view vw_entities_sources as
    select
        sources.sysid as source_id,
        sources.source_name as source_name,
        sources.source_type as source_type,
        entities.sysid as entity_id,
        entities.media_id as media_id,
        entities.media_type as media_type,
        entities.media_name as media_name,
        entities.media_source as media_source,
        entities.geo_lat as geo_lat,
        entities.geo_lon as geo_lon
    from entities
    inner join sources on entities.source_id = sources.sysid;