/*
    Overwatch DB build script
    init.sql

    lchen@chlf.dev
    2024-04-10
*/

-- create (if not exist) and connect to overwatch db
create database if not exists overwatch;
connect overwatch;

-- entity database
create table entity(
    id int not null auto_increment,
    entityName varchar(255),
    primary key (id)
);

-- cameras database
create table cameras(
    id int not null auto_increment,
    camId int not null,
    entity int not null,
    friendly varchar(255),
    direction varchar(255),
    geoPoint point,
    streamType varchar(2),
    baseUrl varchar(2000),
    hasAlt char(1),
    primary key (id),
    foreign key (entity) references entity(id)
);

-- camera urls
create table camera_alt(
    id int not null auto_increment,
    camera int not null,
    uri varchar(2000),
    primary key (id),
    foreign key (camera) references cameras(id)
);