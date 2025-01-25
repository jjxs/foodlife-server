ALTER TABLE public.tbl_inspection
    ADD COLUMN part_cat integer DEFAULT 0;
    
ALTER TABLE public.mst_stock
    ADD COLUMN part_type integer DEFAULT 0;

-- Table: public.mst_stock_history

-- DROP TABLE public.mst_stock_history;

CREATE TABLE public.mst_stock_history
(
    id integer NOT NULL,
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
    part_type integer,
    CONSTRAINT "MST_STOCK_HISTORY_PK" PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.mst_stock_history
    OWNER to postgres;

ALTER TABLE public.menu_option
    ADD COLUMN price integer DEFAULT 0;

ALTER TABLE public.seat_status
    ADD CONSTRAINT uni_seat_id UNIQUE (seat_id);