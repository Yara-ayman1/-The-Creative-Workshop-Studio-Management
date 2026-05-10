if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('BOOKS') and o.name = 'FK_BOOKS_BOOKS_STUDIO')
alter table BOOKS
   drop constraint FK_BOOKS_BOOKS_STUDIO
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('BOOKS') and o.name = 'FK_BOOKS_BOOKS2_MEMBER')
alter table BOOKS
   drop constraint FK_BOOKS_BOOKS2_MEMBER
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('CONSUMES') and o.name = 'FK_CONSUMES_CONSUMES_WORKSHOP')
alter table CONSUMES
   drop constraint FK_CONSUMES_CONSUMES_WORKSHOP
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('CONSUMES') and o.name = 'FK_CONSUMES_CONSUMES2_RAW_MATE')
alter table CONSUMES
   drop constraint FK_CONSUMES_CONSUMES2_RAW_MATE
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('REGISTERS') and o.name = 'FK_REGISTER_REGISTERS_MEMBER')
alter table REGISTERS
   drop constraint FK_REGISTER_REGISTERS_MEMBER
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('REGISTERS') and o.name = 'FK_REGISTER_REGISTERS_WORKSHOP')
alter table REGISTERS
   drop constraint FK_REGISTER_REGISTERS_WORKSHOP
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('RENTS') and o.name = 'FK_RENTS_RENTS_MEMBER')
alter table RENTS
   drop constraint FK_RENTS_RENTS_MEMBER
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('RENTS') and o.name = 'FK_RENTS_RENTS2_TOOL')
alter table RENTS
   drop constraint FK_RENTS_RENTS2_TOOL
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('TOOL') and o.name = 'FK_TOOL_CONTAINS_STUDIO')
alter table TOOL
   drop constraint FK_TOOL_CONTAINS_STUDIO
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('WORKSHOP') and o.name = 'FK_WORKSHOP_HOLDS_STUDIO')
alter table WORKSHOP
   drop constraint FK_WORKSHOP_HOLDS_STUDIO
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('WORKSHOP') and o.name = 'FK_WORKSHOP_LEADS_RESIDENT')
alter table WORKSHOP
   drop constraint FK_WORKSHOP_LEADS_RESIDENT
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('BOOKS')
            and   name  = 'BOOKS2_FK'
            and   indid > 0
            and   indid < 255)
   drop index BOOKS.BOOKS2_FK
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('BOOKS')
            and   name  = 'BOOKS_FK'
            and   indid > 0
            and   indid < 255)
   drop index BOOKS.BOOKS_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('BOOKS')
            and   type = 'U')
   drop table BOOKS
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('CONSUMES')
            and   name  = 'CONSUMES2_FK'
            and   indid > 0
            and   indid < 255)
   drop index CONSUMES.CONSUMES2_FK
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('CONSUMES')
            and   name  = 'CONSUMES_FK'
            and   indid > 0
            and   indid < 255)
   drop index CONSUMES.CONSUMES_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('CONSUMES')
            and   type = 'U')
   drop table CONSUMES
go

if exists (select 1
            from  sysobjects
           where  id = object_id('MEMBER')
            and   type = 'U')
   drop table MEMBER
go

if exists (select 1
            from  sysobjects
           where  id = object_id('RAW_MATERIAL')
            and   type = 'U')
   drop table RAW_MATERIAL
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('REGISTERS')
            and   name  = 'REGISTERS2_FK'
            and   indid > 0
            and   indid < 255)
   drop index REGISTERS.REGISTERS2_FK
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('REGISTERS')
            and   name  = 'REGISTERS_FK'
            and   indid > 0
            and   indid < 255)
   drop index REGISTERS.REGISTERS_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('REGISTERS')
            and   type = 'U')
   drop table REGISTERS
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('RENTS')
            and   name  = 'RENTS2_FK'
            and   indid > 0
            and   indid < 255)
   drop index RENTS.RENTS2_FK
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('RENTS')
            and   name  = 'RENTS_FK'
            and   indid > 0
            and   indid < 255)
   drop index RENTS.RENTS_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('RENTS')
            and   type = 'U')
   drop table RENTS
go

if exists (select 1
            from  sysobjects
           where  id = object_id('RESIDENT_ARTIST')
            and   type = 'U')
   drop table RESIDENT_ARTIST
go

if exists (select 1
            from  sysobjects
           where  id = object_id('STUDIO')
            and   type = 'U')
   drop table STUDIO
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('TOOL')
            and   name  = 'CONTAINS_FK'
            and   indid > 0
            and   indid < 255)
   drop index TOOL.CONTAINS_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('TOOL')
            and   type = 'U')
   drop table TOOL
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('WORKSHOP')
            and   name  = 'HOLDS_FK'
            and   indid > 0
            and   indid < 255)
   drop index WORKSHOP.HOLDS_FK
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('WORKSHOP')
            and   name  = 'LEADS_FK'
            and   indid > 0
            and   indid < 255)
   drop index WORKSHOP.LEADS_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('WORKSHOP')
            and   type = 'U')
   drop table WORKSHOP
go

/*==============================================================*/
/* Table: BOOKS                                                 */
/*==============================================================*/
create table BOOKS (
   STUDIO_ID            int                  not null,
   MEMBER_ID            int                  not null,
   BOOKING_DATE         datetime             null,
   constraint PK_BOOKS primary key (STUDIO_ID, MEMBER_ID)
)
go

/*==============================================================*/
/* Index: BOOKS_FK                                              */
/*==============================================================*/




create nonclustered index BOOKS_FK on BOOKS (STUDIO_ID ASC)
go

/*==============================================================*/
/* Index: BOOKS2_FK                                             */
/*==============================================================*/




create nonclustered index BOOKS2_FK on BOOKS (MEMBER_ID ASC)
go

/*==============================================================*/
/* Table: CONSUMES                                              */
/*==============================================================*/
create table CONSUMES (
   ARTIST_ID            int                  not null,
   STUDIO_ID            int                  not null,
   WORKSHOP_ID          int                  not null,
   MATERIAL_ID          int                  not null,
   QTY_USED             int                  null,
   constraint PK_CONSUMES primary key (ARTIST_ID, STUDIO_ID, WORKSHOP_ID, MATERIAL_ID)
)
go

/*==============================================================*/
/* Index: CONSUMES_FK                                           */
/*==============================================================*/




create nonclustered index CONSUMES_FK on CONSUMES (ARTIST_ID ASC,
  STUDIO_ID ASC,
  WORKSHOP_ID ASC)
go

/*==============================================================*/
/* Index: CONSUMES2_FK                                          */
/*==============================================================*/




create nonclustered index CONSUMES2_FK on CONSUMES (MATERIAL_ID ASC)
go

/*==============================================================*/
/* Table: MEMBER                                                */
/*==============================================================*/
create table MEMBER (
   MEMBER_ID  int  IDENTITY(1,1)  NOT NULL,
   FIRST_NAME           varchar(50)          null,
   LAST_NAME            varchar(50)          null,
   EMAIL                varchar(100)         null,
   PHONE                varchar(11)          null,
   MEMBERSHIP_START     datetime             null,
   MEMBERSHIP_END       datetime             null,
   MEMBERSHIP_TYPE      varchar(30)          null,
   constraint PK_MEMBER primary key (MEMBER_ID)
)
go

/*==============================================================*/
/* Table: RAW_MATERIAL                                          */
/*==============================================================*/
create table RAW_MATERIAL (
   MATERIAL_ID          int                  not null,
   MAT_NAME             varchar(100)         null,
   UNIT                 varchar(100)         null,
   QUANTITY_IN_STOCK    int                  null,
   CATEGORY             varchar(100)         null,
   constraint PK_RAW_MATERIAL primary key (MATERIAL_ID)
)
go

/*==============================================================*/
/* Table: REGISTERS                                             */
/*==============================================================*/
create table REGISTERS (
   MEMBER_ID            int                  not null,
   ARTIST_ID            int                  not null,
   STUDIO_ID            int                  not null,
   WORKSHOP_ID          int                  not null,
   REG_DATE             datetime             null,
   constraint PK_REGISTERS primary key (ARTIST_ID, STUDIO_ID, MEMBER_ID, WORKSHOP_ID)
)
go

/*==============================================================*/
/* Index: REGISTERS_FK                                          */
/*==============================================================*/




create nonclustered index REGISTERS_FK on REGISTERS (MEMBER_ID ASC)
go

/*==============================================================*/
/* Index: REGISTERS2_FK                                         */
/*==============================================================*/




create nonclustered index REGISTERS2_FK on REGISTERS (ARTIST_ID ASC,
  STUDIO_ID ASC,
  WORKSHOP_ID ASC)
go

/*==============================================================*/
/* Table: RENTS                                                 */
/*==============================================================*/
create table RENTS (
   MEMBER_ID            int                  not null,
   TOOL_ID              int                  not null,
   PICKUP_TIME          datetime             null,
   RETURN_TIME          datetime             null,
   RETURN_CONDITION     varchar(1)           null,
   constraint PK_RENTS primary key (MEMBER_ID, TOOL_ID)
)
go

/*==============================================================*/
/* Index: RENTS_FK                                              */
/*==============================================================*/




create nonclustered index RENTS_FK on RENTS (MEMBER_ID ASC)
go

/*==============================================================*/
/* Index: RENTS2_FK                                             */
/*==============================================================*/




create nonclustered index RENTS2_FK on RENTS (TOOL_ID ASC)
go

/*==============================================================*/
/* Table: RESIDENT_ARTIST                                       */
/*==============================================================*/
create table RESIDENT_ARTIST (
   ARTIST_ID            int                  not null,
   FIRST_NAME           varchar(50)          null,
   LAST_NAME            varchar(50)          null,
   EMAIL                varchar(100)         not null,
   SPECIALTY            varchar(100)         null,
   BIO                  varchar(1)           null,
   constraint PK_RESIDENT_ARTIST primary key (ARTIST_ID)
)
go

/*==============================================================*/
/* Table: STUDIO                                                */
/*==============================================================*/
create table STUDIO (
   STUDIO_ID            int                  not null,
   STUDIO_NAME          varchar(50)          null,
   LOCATION             varchar(100)         null,
   CAPACITY             int                  null,
   STUDIO_TYPE          varchar(50)          null,
   EQUIPMENT            varchar(100)         null,
   constraint PK_STUDIO primary key (STUDIO_ID)
)
go

/*==============================================================*/
/* Table: TOOL                                                  */
/*==============================================================*/
create table TOOL (
   TOOL_ID              int                  not null,
   STUDIO_ID            int                  null,
   TOOL_NAME            varchar(100)         null,
   DESCRIPTION          varchar(1)           null,
   TOOL_CONDITION       varchar(100)         null,
   TOTAL_RENTALS        int                  null,
   constraint PK_TOOL primary key (TOOL_ID)
)
go

/*==============================================================*/
/* Index: CONTAINS_FK                                           */
/*==============================================================*/




create nonclustered index CONTAINS_FK on TOOL (STUDIO_ID ASC)
go

/*==============================================================*/
/* Table: WORKSHOP                                              */
/*==============================================================*/
create table WORKSHOP (
   ARTIST_ID            int                  not null,
   STUDIO_ID            int                  not null,
   WORKSHOP_ID          int                  not null,
   TITLE                varchar(70)          null,
   CRAFT_TYPE           varchar(70)          null,
   WORKSHOP_DATE        datetime             null,
   START_TIME           datetime             null,
   END_TIME             datetime             null,
   MAX_PARTICIPANTS     int                  null,
   constraint PK_WORKSHOP primary key (ARTIST_ID, STUDIO_ID, WORKSHOP_ID)
)
go

/*==============================================================*/
/* Index: LEADS_FK                                              */
/*==============================================================*/




create nonclustered index LEADS_FK on WORKSHOP (ARTIST_ID ASC)
go

/*==============================================================*/
/* Index: HOLDS_FK                                              */
/*==============================================================*/




create nonclustered index HOLDS_FK on WORKSHOP (STUDIO_ID ASC)
go

alter table BOOKS
   add constraint FK_BOOKS_BOOKS_STUDIO foreign key (STUDIO_ID)
      references STUDIO (STUDIO_ID)
go

alter table BOOKS
   add constraint FK_BOOKS_BOOKS2_MEMBER foreign key (MEMBER_ID)
      references MEMBER (MEMBER_ID)
go

alter table CONSUMES
   add constraint FK_CONSUMES_CONSUMES_WORKSHOP foreign key (ARTIST_ID, STUDIO_ID, WORKSHOP_ID)
      references WORKSHOP (ARTIST_ID, STUDIO_ID, WORKSHOP_ID)
go

alter table CONSUMES
   add constraint FK_CONSUMES_CONSUMES2_RAW_MATE foreign key (MATERIAL_ID)
      references RAW_MATERIAL (MATERIAL_ID)
go

alter table REGISTERS
   add constraint FK_REGISTER_REGISTERS_MEMBER foreign key (MEMBER_ID)
      references MEMBER (MEMBER_ID)
go

alter table REGISTERS
   add constraint FK_REGISTER_REGISTERS_WORKSHOP foreign key (ARTIST_ID, STUDIO_ID, WORKSHOP_ID)
      references WORKSHOP (ARTIST_ID, STUDIO_ID, WORKSHOP_ID)
go

alter table RENTS
   add constraint FK_RENTS_RENTS_MEMBER foreign key (MEMBER_ID)
      references MEMBER (MEMBER_ID)
go

alter table RENTS
   add constraint FK_RENTS_RENTS2_TOOL foreign key (TOOL_ID)
      references TOOL (TOOL_ID)
go

alter table TOOL
   add constraint FK_TOOL_CONTAINS_STUDIO foreign key (STUDIO_ID)
      references STUDIO (STUDIO_ID)
go

alter table WORKSHOP
   add constraint FK_WORKSHOP_HOLDS_STUDIO foreign key (STUDIO_ID)
      references STUDIO (STUDIO_ID)
go

alter table WORKSHOP
   add constraint FK_WORKSHOP_LEADS_RESIDENT foreign key (ARTIST_ID)
      references RESIDENT_ARTIST (ARTIST_ID)
go
