/*
    get entities within x km radius of specified location as a JSON formatted string
*/
delimiter //
create procedure overwatch.get_entities_nearby (
    in p_radius int,
    in p_geo_lat decimal(8,6),
    in p_geo_lon decimal(9,6)
)
begin
    select 
        json_object(
            "id",
            entity_id,
            "source_id",
            source_id,
            "source_name",
            source_name,
            "source_type",
            source_type,
            "media_id",
            media_id,
            "media_type",
            media_type,
            "media_source",
            media_source,
            "media_name",
            media_name,
            "geo_lat",
            geo_lat,
            "geo_lon",
            geo_lon
        ) as dataset,
        (6371 * acos(
            cos(radians(p_geo_lat)) * cos(radians(geo_lat)) * cos(radians(geo_lon) - radians(p_geo_lon)) + sin(radians(p_geo_lat)) * sin(radians(geo_lat))
        )) as distance_km
    from vw_entities_sources
    having distance_km <= p_radius
    order by distance_km;
end //
delimiter ;