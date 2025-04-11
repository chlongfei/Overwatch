-- CRUD trafficlens.lov

/*  
    adds a lov object to tables, returns sysid of new record
*/
delimiter //
create procedure trafficlens.add_lov_item (    
    in p_list_name varchar(255),
    in p_item_name varchar(255),
    in p_item_value varchar(255),
    in p_sort_order int,
    out p_new_id int
)
begin
    insert into trafficlens.lov (
        list_name,
        item_name,
        item_value,
        sort_order
    ) values (
        p_list_name,
        p_item_name,
        p_item_value,
        p_sort_order
    );

    select last_insert_id() into p_new_id;
end //
delimiter ;

/*  
    reterives a lov object referenced by sysid as a JSON formatted string
*/
delimiter //
create procedure trafficlens.get_lov_item (
    in p_lov_id int
)
begin
    select 
        json_object(
            "id",
            sysid,
            "list_name",
            list_name,
            "item_name",
            item_name,
            "item_value",
            item_value,
            "sort_order",
            sort_order
        ) as dataset
    from trafficlens.lov
    where sysid = p_lov_id;
end //
delimiter ;

/*  
    updates a lov object referenced by sysid
*/
delimiter //
create procedure trafficlens.update_lov_item (
    in p_lov_id int,
    in p_list_name varchar(255),
    in p_item_name varchar(255),
    in p_item_value varchar(255),
    in p_sort_order int
)
begin
    update trafficlens.lov set
        list_name = p_list_name,
        item_name = p_item_name,
        item_value = p_item_value,
        sort_order = p_sort_order
    where sysid = p_lov_id;
end //
delimiter ;

/*  
    deletes a lov object referenced by sysid
*/
delimiter //
create procedure trafficlens.delete_lov_item (
    p_lov_id int
)
begin
    delete from trafficlens.lov where sysid = p_lov_id;
end //
delimiter ;