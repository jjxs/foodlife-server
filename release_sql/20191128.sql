
CREATE TABLE public.menu_bind
(
    menu_id integer,
    bind_id integer,
    PRIMARY KEY (menu_id)
);


ALTER TABLE menu_top add column option text default '';

