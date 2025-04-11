# TrafficLens Database

## Schema

### source
table of sources that providers of each camera entity

column      |   datatype        |   nullable    |   comments
------------|-------------------|---------------|---------------
sysid       |   int             |   no          |   is primary key 
source_name        |   varchar2(255)   |   no          |
source_type        |   varchar2(255)   |   no          |   
origin      |   varchar2(255)   |   yes         |
origin_url  |   varchar2(4000)  |   yes         |

### source_notes
table of notes associated with each source

column      |   datatype        |   nullable    |   comments
------------|-------------------|---------------|---------------
sysid       |   int             |   no          |   is primary key
source_id   |   int             |   no          |   references **source.sysid**
tag         |   varchar2(255)   |   no          |

### entities
table of entities such as cameras and their media sources

column                  |   datatype        |   nullable    |   comments
------------------------|-------------------|---------------|---------------
sysid                   |   int             |   no          |   is primary key
source_id               |   int             |   no          |   references **source.sysid**
media_id                |   varchar2(255)   |   no          |   identifier issued by source
media_type              |   varchar2(255)   |   no          |   either "video" or "static"
media_source            |   varchar2(4000)  |   no          | 
media_last_updated      |   date            |   no          |
name                    |   varchar2(255)   |   no          |
geo_lat                 |   decimal(8,6)    |   no          |
geo_lon                 |   decimal(9,6)    |   no          |
additional_view_north   |   varchar2(4000)  |   yes         |
additional_view_east    |   varchar2(4000)  |   yes         |
additional_view_south   |   varchar2(4000)  |   yes         |
additional_view_west    |   varchar2(4000)  |   yes         |

### entity_tags
table containing tags strings associated with sources

column                  |   datatype        |   nullable    |   comments
------------------------|-------------------|---------------|---------------
sysid                   |   int             |   no          |   is primary key
entity_id               |   int             |   no          |   references **entities.sysid**
content                  |   varchar2(255)   |   no          |

### lov
utility table containing a list-of-values for misc. uses like dropdowns and low quantity lookups

column                  |   datatype        |   nullable    |   comments
------------------------|-------------------|---------------|---------------
sysid                   |   int             |   no          |   is primary key
entity_id               |   int             |   no          |   references **entities.sysid**
values                  |   varchar2(255)   |   no          |
