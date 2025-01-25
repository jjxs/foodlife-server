-- seat表添加了takeout_type字段区分是否是外卖坐席（1是外卖坐席）-字段名修改
ALTER TABLE seat ADD takeout_type INTEGER DEFAULT 0;

-- seat表group_id变为可以为空 - 语句修改
alter table seat alter COLUMN group_id drop not null;

-- SEQUENCE: public.takeout_order_id_seq

-- DROP SEQUENCE public.takeout_order_id_seq;

CREATE SEQUENCE public.takeout_order_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.takeout_order_id_seq
    OWNER TO postgres;

-- SEQUENCE: public.takeout_order_detail_id_seq

-- DROP SEQUENCE public.takeout_order_detail_id_seq;

CREATE SEQUENCE public.takeout_order_detail_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.takeout_order_detail_id_seq
    OWNER TO postgres;

-- 创建订单表
CREATE TABLE public.takeout_order
(
    id integer NOT NULL DEFAULT nextval('takeout_order_id_seq'::regclass),
    ship_addr character varying(200) COLLATE pg_catalog."default",
    ship_time timestamp with time zone,
    ship_tel character varying(100) COLLATE pg_catalog."default",
    pay_type integer,
    pay_status integer DEFAULT 0,
    order_status integer DEFAULT 0,
    user_id integer,
    create_time timestamp with time zone,
    CONSTRAINT takeout_order_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.takeout_order
    OWNER to postgres;

-- 创建订单详细表
CREATE TABLE public.takeout_order_detail
(
    id integer NOT NULL DEFAULT nextval('takeout_order_detail_id_seq'::regclass),
    order_id integer,
    menu_id integer,
    menu_name character varying(100) COLLATE pg_catalog."default",
    price character varying(100) COLLATE pg_catalog."default",
    count integer,
    create_time timestamp with time zone,
    CONSTRAINT takeout_order_detail_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.takeout_order_detail
    OWNER to postgres;

-- company_data表更名为takeout_user
ALTER TABLE company_data RENAME TO takeout_user;
-- 已有字段改名
ALTER TABLE takeout_user RENAME COLUMN com_name TO user_name;
ALTER TABLE takeout_user RENAME COLUMN com_tel TO user_tel;
ALTER TABLE takeout_user RENAME COLUMN com_address TO user_address;
-- 未有字段添加
ALTER TABLE takeout_user ADD user_id character varying(100);
ALTER TABLE takeout_user ADD user_pass character varying(128);
ALTER TABLE takeout_user ADD user_email character varying(100);

