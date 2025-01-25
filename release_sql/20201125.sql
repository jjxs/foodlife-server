ALTER TABLE public.counter_detail
    ADD COLUMN print_count numeric(8, 0);


CREATE SEQUENCE public.mst_report_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

CREATE TABLE public.mst_report
(
    id integer NOT NULL DEFAULT nextval('mst_report_id_seq'::regclass),
    report_type character varying(20) COLLATE pg_catalog."default",
    report_date character varying(10) COLLATE pg_catalog."default",
    report json,
    create_time timestamp without time zone,
    CONSTRAINT mst_report_pkey PRIMARY KEY (id)
);

CREATE INDEX idx_report_date ON mst_report ( report_date );
CREATE INDEX idx_report_type ON mst_report ( report_type );


CREATE SEQUENCE public.mst_report_history_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

CREATE TABLE public.mst_report_history
(
    id integer NOT NULL DEFAULT nextval('mst_report_history_id_seq'::regclass),
    report_type character varying(20) COLLATE pg_catalog."default",
    report_date character varying(10) COLLATE pg_catalog."default",
    report json,
    create_time timestamp without time zone,
    CONSTRAINT mst_report_history_pkey PRIMARY KEY (id)
);

CREATE INDEX idx_report_history_report_date ON mst_report_history ( report_date );
CREATE INDEX idx_report_history_report_type ON mst_report_history ( report_type );


CREATE SEQUENCE public.tbl_supplier_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

CREATE TABLE public.tbl_supplie
(
    id integer NOT NULL DEFAULT nextval('tbl_supplier_id_seq'::regclass),
    sup_name character varying(32) COLLATE pg_catalog."default",
    sup_tel character varying(20) COLLATE pg_catalog."default",
    sup_addr character varying(64) COLLATE pg_catalog."default",
    contact_name character varying(20) COLLATE pg_catalog."default",
    extend json,
    create_time timestamp without time zone,
    CONSTRAINT tbl_supplie_pkey PRIMARY KEY (id)
);