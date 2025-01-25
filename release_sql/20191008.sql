CREATE TABLE public.menu_top
(
    id numeric NOT NULL,
    name character varying(20),
    target_type character varying(20),
    link character varying(200),
    image character varying(200),
    note character varying(200),
    sort numeric,
    enabled numeric,
    PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);


    
ALTER TABLE master_data_group add column enabled numeric(8) default 1;



CREATE TABLE public.seat_free
(
    id SERIAL  NOT NULL,
    seat_id numeric,
    menu_free_id numeric,
    start timestamp with time zone,
    status numeric,
    PRIMARY KEY (id)
);
