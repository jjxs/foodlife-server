ALTER TABLE mst_stock ADD COLUMN parts_inventory_actual Integer NOT NULL DEFAULT 0;

DROP SEQUENCE if EXISTS "profit_inventory_id_seq";
CREATE SEQUENCE "profit_inventory_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 2147483647
 START 1
 CACHE 1;

DROP SEQUENCE if EXISTS "profit_inventory_detail_id_seq";
CREATE SEQUENCE "profit_inventory_detail_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 2147483647
 START 1
 CACHE 1;

DROP SEQUENCE if EXISTS "mst_user_id_seq";
CREATE SEQUENCE "mst_user_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 2147483647
 START 1
 CACHE 1;

DROP SEQUENCE if EXISTS "menu_gift_id_seq";
CREATE SEQUENCE "menu_gift_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 2147483647
 START 1
 CACHE 1;
 

CREATE TABLE profit_inventory(
   id integer NOT NULL DEFAULT nextval('profit_inventory_id_seq'::regclass),
   inventory_date timestamp without time zone NOT NULL,
   inventory_user character varying(32),
   status integer,
   create_date timestamp(6) without time zone,
   create_user_id integer,
   create_program character varying(128),
   last_update_date timestamp(6) without time zone,
   last_update_user_id integer,
   last_update_program character varying(128),
   CONSTRAINT "PROFIT_INVENTORY_PK" PRIMARY KEY (id) 
);

CREATE TABLE profit_inventory_detail(
   id integer NOT NULL DEFAULT nextval('profit_inventory_detail_id_seq'::regclass),
   inventory_id integer NOT NULL,
   inventory_date timestamp without time zone NOT NULL,
   part_id integer NOT NULL,
   parts_type character varying(32),
   part_name character varying(32) NOT NULL,
   parts_inventory_qty integer NOT NULL,
   parts_inventory_actual integer NOT NULL,
   ave_price integer NOT NULL,
   remarks character varying(256),
   create_date timestamp(6) without time zone,
   create_user_id integer,
   create_program character varying(128),
   last_update_date timestamp(6) without time zone,
   last_update_user_id integer,
   last_update_program character varying(128),
   CONSTRAINT "PROFIT_INVENTORY_DETAIL_PK" PRIMARY KEY (id) 
);

CREATE TABLE profit_inventory_detail(
   id integer NOT NULL DEFAULT nextval('profit_inventory_detail_id_seq'::regclass),
   inventory_id integer NOT NULL,
   inventory_date timestamp without time zone NOT NULL,
   part_id integer NOT NULL,
   parts_type character varying(32),
   part_name character varying(32) NOT NULL,
   parts_inventory_qty integer NOT NULL,
   parts_inventory_actual integer NOT NULL,
   ave_price integer NOT NULL,
   remarks character varying(256),
   create_date timestamp(6) without time zone,
   create_user_id integer,
   create_program character varying(128),
   last_update_date timestamp(6) without time zone,
   last_update_user_id integer,
   last_update_program character varying(128),
   CONSTRAINT "PROFIT_INVENTORY_DETAIL_PK" PRIMARY KEY (id) 
);

CREATE TABLE mst_user(
   id integer NOT NULL DEFAULT nextval('mst_user_id_seq'::regclass),
   account character varying(64) NOT NULL,
   password character varying(256) NOT NULL,
   level integer NOT NULL DEFAULT 1,
   point integer NOT NULL DEFAULT 0,
   gift_count integer DEFAULT 0,
   user_name character varying(32),
   sex integer,
   phone_number character varying(32),
   remarks character varying(256),
   CONSTRAINT "MST_USER_PK" PRIMARY KEY (id),
   CONSTRAINT mst_user_account_key UNIQUE (account)
);

CREATE TABLE menu_gift(
   id integer NOT NULL DEFAULT nextval('menu_gift_id_seq'::regclass),
   menu_id integer NOT NULL,
   use_gift_count integer NOT NULL,
   flg boolean NOT NULL,
   CONSTRAINT "MENU_GIFT_PK" PRIMARY KEY (id),
   CONSTRAINT menu_gift_menu_id_key UNIQUE (menu_id)
);
