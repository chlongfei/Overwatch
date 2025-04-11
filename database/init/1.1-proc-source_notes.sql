-- CRUD trafficlens.source_notes

/* 
    adds a source note object to tables, returns sysid of new record
*/
delimiter //
create procedure trafficlens.add_source_note (
    in p_source_id int,
    in p_content varchar(255),
    out p_new_id int
)
begin
    insert into trafficlens.source_notes (
        source_id,
        content
    ) values (
        p_source_id,
        p_content
    );

    select last_insert_id() into p_new_id;
end //
delimiter ;

/* 
    reterives the source note object referenced by sysid as a JSON formatted string
*/
delimiter //
create procedure trafficlens.get_source_note (
    in p_source_note_id int
)
begin
    select 
        json_object(
            "id",
            sysid,
            "content",
            content
        ) as dataset
    from trafficlens.source_notes
    where sysid = p_source_note_id;
end //
delimiter ;

/* 
    updates the source note object referenced by sysid
*/
delimiter //
create procedure trafficlens.update_source_note (
    in p_source_note_id int,
    in p_source_id int,
    in p_content varchar(255)
)
begin
    update trafficlens.source_notes set
        source_id = p_source_id,
        content = p_content
    where sysid = p_source_note_id;
end //
delimiter ;

/* 
    deletes the source note object referenced by sysid
*/
delimiter //
create procedure trafficlens.delete_source_note (
    in p_source_note_id int
)
begin
    delete from trafficlens.source_notes where sysid = p_source_note_id;
end //
delimiter ;