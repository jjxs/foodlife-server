-- takeout_user表添加user-id索引
CREATE UNIQUE INDEX uni_user_id ON takeout_user (user_id);


ALTER TABLE public.menu_course_detail
    ADD COLUMN group_id integer;
ALTER TABLE public."order"
    ADD COLUMN ship_addr character varying(200),
    ADD COLUMN ship_name character varying(50),
    ADD COLUMN ship_tel character varying(32),
    ADD COLUMN ship_time timestamp with time zone;


ALTER TABLE public."order_history"
    ADD COLUMN ship_addr character varying(200),
    ADD COLUMN ship_name character varying(50),
    ADD COLUMN ship_tel character varying(32),
    ADD COLUMN ship_time timestamp with time zone;


ALTER TABLE public.menu
    ADD COLUMN takeout integer DEFAULT 0;

COMMENT ON COLUMN public.menu.takeout
    IS '是否外卖';

ALTER TABLE public.takeout_order
    ADD COLUMN ship_name character varying(30) NOT NULL DEFAULT '';

COMMENT ON COLUMN public.takeout_order.ship_name
    IS '受取人';