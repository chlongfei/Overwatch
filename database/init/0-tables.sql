/* CREATE DATABASE */
create database if not exists overwatch;

/* CREATE TABLES */
/* table to hold all the sources for entities*/
create table overwatch.sources (
    sysid int not null auto_increment,
    source_name varchar(255) not null,
    source_type varchar(20) not null,
    origin varchar(255),
    origin_url varchar(4000),

    primary key (sysid)
);

/* table to hold notes for sources */
create table overwatch.source_notes (
    sysid int not null auto_increment,
    source_id int not null,
    content varchar(255) not null,

    primary key (sysid),
    foreign key (source_id) references overwatch.sources (sysid) on delete cascade
);

/* table to hold entities from sources */
create table overwatch.entities (
    sysid int not null auto_increment,
    source_id int not null,
    media_id varchar(255) not null,
    media_type varchar(255) not null,
    media_source text(2000) not null,
    media_name varchar(255) not null,
    geo_lat decimal(8,6) not null,
    geo_lon decimal(9,6) not null,
    additional_view_north varchar(2000),
    additional_view_east varchar(2000),
    additional_view_south varchar(2000),
    additional_view_west varchar(2000),

    primary key (sysid),
    foreign key (source_id) references overwatch.sources (sysid) on delete cascade
);

/* table to hold tags for entities */
create table overwatch.entity_tags (
    sysid int not null auto_increment,
    entity_id int not null,
    content varchar(255) not null,

    primary key (sysid),
    foreign key (entity_id) references overwatch.entities (sysid) on delete cascade
);

/* table to hold list of misc. items used by application */
create table overwatch.lov (
    sysid int not null auto_increment,
    list_name varchar(255) not null,
    item_name varchar(255) not null,
    item_value varchar(255) not null,
    sort_order int,

    primary key (sysid)
);

SET GLOBAL log_bin_trust_function_creators = 1;