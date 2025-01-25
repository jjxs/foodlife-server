-- SEQUENCE: public.company_data_id_seq

-- DROP SEQUENCE public.company_data_id_seq;

CREATE SEQUENCE public.company_data_id_seq
    INCREMENT 1
    START 14
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.company_data_id_seq
    OWNER TO postgres;
    
-- 添加公司表
CREATE TABLE public.company_data
(
    id integer NOT NULL DEFAULT nextval('company_data_id_seq'::regclass),
    com_name character varying(100) COLLATE pg_catalog."default",
    com_tel character varying(100) COLLATE pg_catalog."default",
    com_address character varying(200) COLLATE pg_catalog."default",
    seat_no integer,
    create_time timestamp without time zone,
    CONSTRAINT company_data_pkey PRIMARY KEY (id)
);

-- seat表添加了takeout_type字段区分是否是外卖坐席（1是外卖坐席）
ALTER TABLE seat ADD FieldName1 INTEGER;

-- seat表group_id变为可以为空
alter table seat drop column group_id 
ALTER TABLE seat ADD group_id INTEGER