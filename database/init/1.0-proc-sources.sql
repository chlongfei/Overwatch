-- CRUD overwatch.sources

/* 
    adds a source object to tables, returns sysid of new record
*/
delimiter //
create procedure overwatch.add_source (
    in p_source_name varchar(255),
    in p_source_type varchar(5),
    in p_origin varchar(255),
    in p_origin_url varchar(4000),
    out p_new_id int
)
begin
    insert into overwatch.sources (
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
create procedure overwatch.get_sources () 
begin
    select 
        json_object(
            "id",
            overwatch.sources.sysid,
            "source_name",
            overwatch.sources.source_name,
            "source_type",
            overwatch.sources.source_type,
            "origin",
            overwatch.sources.origin,
            "origin_url",
            overwatch.sources.origin_url,
            "entity_count",
            ifnull(count(overwatch.entities.sysid),0)
        ) as dataset
    from overwatch.sources
    left join overwatch.entities on overwatch.sources.sysid = overwatch.entities.source_id
    group by overwatch.sources.sysid, overwatch.sources.source_name, overwatch.sources.source_type, overwatch.sources.origin, overwatch.sources.origin_url;
end //
delimiter ;

/* 
    reterives the source object referenced by sysid as a JSON formatted string
*/
delimiter //
create procedure overwatch.get_source (
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
    from overwatch.sources
    where sysid = p_source_id;
end //
delimiter ;

/* 
    reterives the source object referenced by source_name as a JSON formatted string
*/
delimiter //
create procedure overwatch.get_source_by_name (
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
    from overwatch.sources
    where source_name = p_source_name;
end //
delimiter ;

/* 
    updates the source object referenced by sysid
*/
delimiter //
create procedure overwatch.update_source (
    in p_sysid int,
    in p_source_name varchar(255),
    in p_source_type varchar(5),
    in p_origin varchar(255),
    in p_origin_url varchar(4000)
)
begin
    update overwatch.sources set
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
create procedure overwatch.delete_source (
    in p_sysid int
)
begin
    delete from overwatch.sources where sysid = p_sysid;
end //
delimiter ;