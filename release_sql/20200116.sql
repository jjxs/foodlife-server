CREATE TABLE public.mst_message
(
    id character varying(10) COLLATE pg_catalog."default" NOT NULL,
    language character varying(1024) COLLATE pg_catalog."default" NOT NULL,
    message character varying(1024) COLLATE pg_catalog."default"
);

CREATE SEQUENCE public.mst_parts_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;


CREATE TABLE public.mst_parts
(
    id integer NOT NULL DEFAULT nextval('mst_parts_id_seq'::regclass),
    part_code character varying(8) COLLATE pg_catalog."default",
    part_name character varying(32) COLLATE pg_catalog."default",
    parts_type character varying(8) COLLATE pg_catalog."default",
    part_unit integer,
    create_date timestamp(6) without time zone,
    create_user_id integer,
    create_program character varying(128) COLLATE pg_catalog."default",
    last_update_date timestamp(6) without time zone,
    last_update_user_id integer,
    last_update_program character varying(128) COLLATE pg_catalog."default",
    CONSTRAINT "MST_PARTS_PK" PRIMARY KEY (id)
);




CREATE SEQUENCE public.mst_stock_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

CREATE TABLE public.mst_stock
(
    id integer NOT NULL DEFAULT nextval('mst_stock_id_seq'::regclass),
    receipt_number character varying(32) COLLATE pg_catalog."default",
    part_id integer,
    product_name character varying(32) COLLATE pg_catalog."default",
    product_unit integer,
    parts_processing_category character varying(8) COLLATE pg_catalog."default",
    part_processing_category_id integer,
    remarks character varying(256) COLLATE pg_catalog."default",
    create_date timestamp(6) without time zone,
    create_user_id integer,
    create_program character varying(128) COLLATE pg_catalog."default",
    last_update_date timestamp(6) without time zone,
    last_update_user_id integer,
    last_update_program character varying(128) COLLATE pg_catalog."default",
    parts_theory_inventory_qty integer,
    parts_inventory_qty integer,
    base integer,
    CONSTRAINT "MST_STOCK_PK" PRIMARY KEY (id)
);



CREATE SEQUENCE public.shop_cost_category_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

CREATE TABLE public.shop_cost_category
(
    id integer NOT NULL DEFAULT nextval('shop_cost_category_id_seq'::regclass),
    parent_id integer,
    category_name character varying(32) COLLATE pg_catalog."default",
    create_date timestamp(6) without time zone,
    create_user_id integer,
    create_program character varying(128) COLLATE pg_catalog."default",
    last_update_date timestamp(6) without time zone,
    last_update_user_id integer,
    last_update_program character varying(128) COLLATE pg_catalog."default",
    CONSTRAINT "SHOP_COST_CATEGORY_PK" PRIMARY KEY (id)
);




CREATE SEQUENCE public.shop_cost_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

CREATE TABLE public.shop_cost
(
    id integer NOT NULL DEFAULT nextval('shop_cost_id_seq'::regclass),
    cost_category_id integer,
    cost_name character varying(32) COLLATE pg_catalog."default",
    pay_time timestamp(6) with time zone,
    cost numeric(8,2),
    create_date timestamp(6) without time zone,
    create_user_id integer,
    create_program character varying(128) COLLATE pg_catalog."default",
    last_update_date timestamp(6) without time zone,
    last_update_user_id integer,
    last_update_program character varying(128) COLLATE pg_catalog."default",
    CONSTRAINT "SHOP_COST_PK" PRIMARY KEY (id)
);





ALTER TABLE order_detail add column menu_option jsonb, add column cat_id numeric(8), add column cat_name varchar(100);
ALTER TABLE order_detail_history add column menu_option jsonb, add column cat_id numeric(8), add column cat_name varchar(100);

CREATE UNIQUE INDEX uni_no ON menu (no);