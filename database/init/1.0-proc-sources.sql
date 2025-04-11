-- CRUD trafficlens.sources

/* 
    adds a source object to tables, returns sysid of new record
*/
delimiter //
create procedure trafficlens.add_source (
    in p_source_name varchar(255),
    in p_source_type varchar(5),
    in p_origin varchar(255),
    in p_origin_url varchar(4000),
    out p_new_id int
)
begin
    insert into trafficlens.sources (
        source_name,
        source_type,
        origin,
        origin_url
    ) values (
        p_source_name,
        p_source_type,
        p_origin,
        p_origin_url
    );

    select last_insert_id() into p_new_id;
end //
delimiter ;

/* 
    reterives all source objects as a JSON formatted string
*/
delimiter //
create procedure trafficlens.get_sources () 
begin
    select 
        json_object(
            "id",
            trafficlens.sources.sysid,
            "source_name",
            trafficlens.sources.source_name,
            "source_type",
            trafficlens.sources.source_type,
            "origin",
            trafficlens.sources.origin,
            "origin_url",
            trafficlens.sources.origin_url,
            "entity_count",
            ifnull(count(trafficlens.entities.sysid),0)
        ) as dataset
    from trafficlens.sources
    left join trafficlens.entities on trafficlens.sources.sysid = trafficlens.entities.source_id
    group by trafficlens.sources.sysid, trafficlens.sources.source_name, trafficlens.sources.source_type, trafficlens.sources.origin, trafficlens.sources.origin_url;
end //
delimiter ;

/* 
    reterives the source object referenced by sysid as a JSON formatted string
*/
delimiter //
create procedure trafficlens.get_source (
  in p_source_id int
) 
begin
    select 
        json_object(
            "id",
            sysid,
            "source_name",
            source_name,
            "source_type",
            source_type,
            "origin",
            origin,
            "origin_url",
            origin_url
        ) as dataset
    from trafficlens.sources
    where sysid = p_source_id;
end //
delimiter ;

/* 
    reterives the source object referenced by source_name as a JSON formatted string
*/
delimiter //
create procedure trafficlens.get_source_by_name (
  in p_source_name varchar(255)
) 
begin
    select 
        json_object(
            "id",
            sysid,
            "source_name",
            source_name,
            "source_type",
            source_type,
            "origin",
            origin,
            "origin_url",
            origin_url
        ) as dataset
    from trafficlens.sources
    where source_name = p_source_name;
end //
delimiter ;

/* 
    updates the source object referenced by sysid
*/
delimiter //
create procedure trafficlens.update_source (
    in p_sysid int,
    in p_source_name varchar(255),
    in p_source_type varchar(5),
    in p_origin varchar(255),
    in p_origin_url varchar(4000)
)
begin
    update trafficlens.sources set
        source_name = p_source_name,
        source_type = p_source_type,
        origin = p_origin,
        origin_url = p_origin_url
    where sysid = p_sysid;
end //
delimiter ;

/* 
    deletes the source object referenced by sysid
*/
delimiter //
create procedure trafficlens.delete_source (
    in p_sysid int
)
begin
    delete from trafficlens.sources where sysid = p_sysid;
end //
delimiter ;