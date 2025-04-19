-- CRUD overwatch.entity_tags

/* 
    adds an entity tag object to tables, returns sysid of new record
*/
delimiter //
create procedure overwatch.add_entity_tag (
    in p_entity_id int,
    in p_tag varchar(255),
    out p_new_id int
)
begin
    insert into overwatch.entity_tags (
        entity_id,
        tag
    ) values (
        p_entity_id,
        p_tag
    );

    select last_insert_id() into p_new_id;
end //
delimiter ;

/* 
    reterives an entity tag object referenced by sysid as a JSON formatted string
*/
delimiter //
create procedure overwatch.get_entity_tag (
    in p_entity_tag_id int
)
begin
    select 
        json_object(
            "id",
            sysid,
            "content",
            tag
        ) as dataset
    from overwatch.entity_tags
    where sysid = p_entity_tag_id;
end //
delimiter ;

/* 
    updates an entity tag object referenced by sysid
*/
delimiter //
create procedure overwatch.update_entity_tag (
    in p_entity_tag_id int,
    in p_entity_id int,
    in p_tag varchar(255)
)
begin
    update overwatch.entity_tag set
        entity_id = p_entity_id,
        tag = p_tag
    where sysid = p_entity_tag_id;
end //
delimiter ;

/* 
    deletes an entity tag object referenced by sysid
*/
delimiter //
create procedure overwatch.delete_entity_tag (
    in p_entity_tag_id int
)
begin
    delete from overwatch.entity_tag where sysid = p_entity_tag_id;
end //
delimiter ;