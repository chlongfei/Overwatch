-- CRUD overwatch.source_notes

/* 
    adds a source note object to tables, returns sysid of new record
*/
delimiter //
create procedure overwatch.add_source_note (
    in p_source_id int,
    in p_content varchar(255),
    out p_new_id int
)
begin
    insert into overwatch.source_notes (
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
create procedure overwatch.get_source_note (
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
    from overwatch.source_notes
    where sysid = p_source_note_id;
end //
delimiter ;

/* 
    updates the source note object referenced by sysid
*/
delimiter //
create procedure overwatch.update_source_note (
    in p_source_note_id int,
    in p_source_id int,
    in p_content varchar(255)
)
begin
    update overwatch.source_notes set
        source_id = p_source_id,
        content = p_content
    where sysid = p_source_note_id;
end //
delimiter ;

/* 
    deletes the source note object referenced by sysid
*/
delimiter //
create procedure overwatch.delete_source_note (
    in p_source_note_id int
)
begin
    delete from overwatch.source_notes where sysid = p_source_note_id;
end //
delimiter ;