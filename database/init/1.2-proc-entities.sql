-- CRUD trafficlens.entities

/* 
    adds an entity object to tables, returns sysid of new record
*/
delimiter //
create procedure trafficlens.add_entity (
    in p_source_id int,
    in p_media_id varchar(255),
    in p_media_type varchar(255),
    in p_media_source text(2000),
    in p_media_last_updated date,
    in p_media_name varchar(255),
    in p_geo_lat decimal(8,6),
    in p_geo_lon decimal(9,6),
    in p_additional_view_north varchar(2000),
    in p_additional_view_east varchar(2000),
    in p_additional_view_south varchar(2000),
    in p_additional_view_west varchar(2000),
    out p_new_id int
)
begin
    insert into trafficlens.entities (
        source_id,
        media_id,
        media_type,
        media_source,
        media_last_updated,
        media_name,
        geo_lat,
        geo_lon,
        additional_view_north,
        additional_view_east,
        additional_view_south,
        additional_view_west
    ) values (
        p_source_id,
        p_media_id,
        p_media_type,
        p_media_source,
        p_media_last_updated,
        p_media_name,
        p_geo_lat,
        p_geo_lon,
        p_additional_view_north,
        p_additional_view_east,
        p_additional_view_south,
        p_additional_view_west
    );

    select last_insert_id() into p_new_id;
end //
delimiter ;

/* 
    reterives the entity object referenced by sysid as a JSON formatted string
*/
delimiter //
create procedure trafficlens.get_entity (
    in p_entity_id int
)
begin
    select 
        json_object(
            "id",
            sysid,
            "source_id",
            source_id,
            "media_id",
            media_id,
            "media_type",
            media_type,
            "media_source",
            media_source,
            "media_last_updated",
            media_last_updated,
            "media_name",
            media_name,
            "geo_lat",
            geo_lat,
            "geo_lon",
            geo_lon,
            "additional_view_north",
            additional_view_north,
            "additional_view_east",
            additional_view_east,
            "additional_view_south",
            additional_view_south,
            "additional_view_west",
            additional_view_west
        ) as dataset
    from trafficlens.entities
    where sysid = p_entity_id;
end //
delimiter ;

/* 
    reterives the entities belonging to a specified source as a JSON formatted string
*/
delimiter //
create procedure trafficlens.get_entity_by_source (
    in p_source_id int
)
begin
    select 
        json_object(
            "id",
            sysid,
            "source_id",
            source_id,
            "media_id",
            media_id,
            "media_type",
            media_type,
            "media_source",
            media_source,
            "media_last_updated",
            media_last_updated,
            "media_name",
            media_name,
            "geo_lat",
            geo_lat,
            "geo_lon",
            geo_lon,
            "additional_view_north",
            additional_view_north,
            "additional_view_east",
            additional_view_east,
            "additional_view_south",
            additional_view_south,
            "additional_view_west",
            additional_view_west
        ) as dataset
    from trafficlens.entities
    where source_id = p_source_id;
end //
delimiter ;

/*
    get entities within x km radius of specified location as a JSON formatted string
*/
delimiter //
create procedure trafficlens.get_entities_nearby (
    in p_radius int,
    in p_geo_lat decimal(8,6),
    in p_geo_lon decimal(9,6)
)
begin
    select 
        json_object(
            "id",
            sysid,
            "source_id",
            source_id,
            "media_id",
            media_id,
            "media_type",
            media_type,
            "media_source",
            media_source,
            "media_last_updated",
            media_last_updated,
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
    from trafficlens.entities
    having distance_km <= p_radius
    order by distance_km;
end //
delimiter ;

/* 
    updates the entity object referenced by sysid
*/
delimiter //
create procedure trafficlens.update_entity (
    in p_entity_id int,
    in p_source_id int,
    in p_media_id varchar(255),
    in p_media_type varchar(255),
    in p_media_source text(2000),
    in p_media_last_updated date,
    in p_media_name varchar(255),
    in p_geo_lat decimal(8,6),
    in p_geo_lon decimal(9,6),
    in p_additional_view_north varchar(2000),
    in p_additional_view_east varchar(2000),
    in p_additional_view_south varchar(2000),
    in p_additional_view_west varchar(2000)
)
begin
    update trafficlens.entities set
        source_id = p_source_id,
        media_id = p_media_id,
        media_type = p_media_type,
        media_source = p_media_source,
        media_last_updated = p_media_last_updated,
        media_name = p_media_name,
        geo_lat = p_geo_lat,
        geo_lon = p_geo_lon,
        additional_view_north = p_additional_view_north,
        additional_view_east = p_additional_view_east,
        additional_view_south = p_additional_view_south,
        additional_view_west = p_additional_view_west
    where sysid = p_entity_id;
end //
delimiter ;

/* 
    deletes the entity object referenced by sysid
*/
delimiter //
create procedure trafficlens.delete_entity (
    in p_sysid int
)
begin
    delete from trafficlens.entities where sysid = p_sysid;
end //
delimiter ;