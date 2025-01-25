-- SEQUENCE: public.auth_menu_id_seq

-- DROP SEQUENCE public.auth_menu_id_seq;

CREATE SEQUENCE public.auth_menu_id_seq
    INCREMENT 1
    START 1018
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.auth_menu_id_seq
    OWNER TO postgres;

-- SEQUENCE: public.machine_id_seq

-- DROP SEQUENCE public.machine_id_seq;

CREATE SEQUENCE public.machine_id_seq
    INCREMENT 1
    START 107
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.machine_id_seq
    OWNER TO postgres;

CREATE TABLE public.auth_menu
(
    id integer NOT NULL DEFAULT nextval('auth_menu_id_seq'::regclass),
    menu_path character varying(80) COLLATE pg_catalog."default",
    group_id integer,
    CONSTRAINT auth_menu_pkey PRIMARY KEY (id)
);

CREATE TABLE public.machine
(
    id integer NOT NULL DEFAULT nextval('machine_id_seq'::regclass),
    sign character varying(128) COLLATE pg_catalog."default",
    update_data timestamp without time zone,
    status boolean,
    last_data timestamp without time zone,
    is_delete integer,
    CONSTRAINT machine_pkey PRIMARY KEY (id)
);

INSERT INTO public.master_config(
	 key, value)
	VALUES ('license','{"machine_count": 100}');

    

-- SEQUENCE: public.tbl_inspection_id_seq

-- DROP SEQUENCE public.tbl_inspection_id_seq;

CREATE SEQUENCE public.tbl_inspection_id_seq
    INCREMENT 1
    START 26
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.tbl_inspection_id_seq
    OWNER TO postgres;
  -- Table: public.tbl_inspection

-- DROP TABLE public.tbl_inspection;

CREATE TABLE public.tbl_inspection
(
    id integer NOT NULL DEFAULT nextval('tbl_inspection_id_seq'::regclass),
    part_id integer,
    part_type integer,
    part_unit character varying(16) COLLATE pg_catalog."default",
    parts_unit_price numeric(8,2),
    parts_currency character varying(16) COLLATE pg_catalog."default",
    parts_inventory_qty integer,
    inspection_date date,
    inspector character varying(16) COLLATE pg_catalog."default",
    inspection_result_confirmation character varying(8) COLLATE pg_catalog."default",
    remarks character varying(256) COLLATE pg_catalog."default",
    create_date timestamp(6) without time zone,
    create_user_id integer,
    create_program character varying(128) COLLATE pg_catalog."default",
    last_update_date timestamp(6) without time zone,
    last_update_user_id integer,
    last_update_program character varying(128) COLLATE pg_catalog."default",
    inspection_delete integer,
    base integer,
    CONSTRAINT "TBL_INSPECTION_PK" PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.tbl_inspection
    OWNER to postgres;
COMMENT ON TABLE public.tbl_inspection
    IS '点検テーブル';

COMMENT ON COLUMN public.tbl_inspection.id
    IS 'ユニークID';

COMMENT ON COLUMN public.tbl_inspection.part_id
    IS '部品ID';
    
COMMENT ON COLUMN public.tbl_inspection.part_type
    IS '部品类型1:材料 2:メニュー';

COMMENT ON COLUMN public.tbl_inspection.part_unit
    IS '部品単位';

COMMENT ON COLUMN public.tbl_inspection.parts_unit_price
    IS '部品単価';

COMMENT ON COLUMN public.tbl_inspection.parts_currency
    IS '部品通貨';

COMMENT ON COLUMN public.tbl_inspection.parts_inventory_qty
    IS '部品在庫数量';

COMMENT ON COLUMN public.tbl_inspection.inspection_date
    IS '点検日期';

COMMENT ON COLUMN public.tbl_inspection.inspector
    IS '点検人';

COMMENT ON COLUMN public.tbl_inspection.inspection_result_confirmation
    IS '点検結果確認';

COMMENT ON COLUMN public.tbl_inspection.remarks
    IS '備考';

COMMENT ON COLUMN public.tbl_inspection.create_date
    IS '作成日';

COMMENT ON COLUMN public.tbl_inspection.create_user_id
    IS '作成者';

COMMENT ON COLUMN public.tbl_inspection.create_program
    IS '作成プログラム';

COMMENT ON COLUMN public.tbl_inspection.last_update_date
    IS '最終更新日';

COMMENT ON COLUMN public.tbl_inspection.last_update_user_id
    IS '最終更新者';

COMMENT ON COLUMN public.tbl_inspection.last_update_program
    IS '最終更新プログラム';

COMMENT ON COLUMN public.tbl_inspection.inspection_delete
    IS '点検削除';

COMMENT ON COLUMN public.tbl_inspection.base
    IS '拠点';


-- SEQUENCE: public.menu_top_id_seq

-- DROP SEQUENCE public.menu_top_id_seq;

CREATE SEQUENCE public.menu_top_id_seq
    INCREMENT 1
    START 107
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.menu_top_id_seq
    OWNER TO postgres;

-- 0716 menu_top 新增列 zyx
CREATE TABLE public.menu_top
(
    menu_type character varying(20) COLLATE pg_catalog."default",
    -- zyx 0721 add id变为自增字段
    id integer NOT NULL DEFAULT nextval('menu_top_id_seq'::regclass)
);



-- SEQUENCE: public.tbl_recipe_id_seq

-- DROP SEQUENCE public.tbl_recipe_id_seq;

CREATE SEQUENCE public.tbl_recipe_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.tbl_recipe_id_seq
    OWNER TO postgres;

-- Table: public.tbl_recipe

-- DROP TABLE public.tbl_recipe;

CREATE TABLE public.tbl_recipe
(
    id integer NOT NULL DEFAULT nextval('tbl_recipe_id_seq'::regclass),
    ing_id integer,
    serving numeric(8,2),
    amount_to_use numeric(8,2),
    menu_id integer,
    CONSTRAINT "TBL_RECIPE_PK" PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.tbl_recipe
    OWNER to postgres;
COMMENT ON TABLE public.tbl_recipe
    IS 'レシピテーブル';

COMMENT ON COLUMN public.tbl_recipe.id
    IS 'ユニークID';

COMMENT ON COLUMN public.tbl_recipe.ing_id
    IS '材料ID';

COMMENT ON COLUMN public.tbl_recipe.serving
    IS '分量';

COMMENT ON COLUMN public.tbl_recipe.amount_to_use
    IS '使用量';

COMMENT ON COLUMN public.tbl_recipe.menu_id
    IS 'メニューID';




-- SEQUENCE: public.mst_ingredients_id_seq

-- DROP SEQUENCE public.mst_ingredients_id_seq;

CREATE SEQUENCE public.mst_ingredients_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.mst_ingredients_id_seq
    OWNER TO postgres;


-- Table: public.mst_ingredients

-- DROP TABLE public.mst_ingredients;

CREATE TABLE public.mst_ingredients
(
    id integer NOT NULL DEFAULT nextval('mst_ingredients_id_seq'::regclass),
    ing_no character varying(16) COLLATE pg_catalog."default",
    ing_name character varying(64) COLLATE pg_catalog."default",
    ing_cat_id integer,
    stock_unit character varying(8) COLLATE pg_catalog."default",
    consumption_unit character varying(8) COLLATE pg_catalog."default",
    unit_conv_rate numeric(8,2),
    ave_price numeric(8,2),
    create_date timestamp(6) without time zone,
    create_user_id integer,
    create_program character varying(128) COLLATE pg_catalog."default",
    last_update_date timestamp(6) without time zone,
    last_update_user_id integer,
    last_update_program character varying(128) COLLATE pg_catalog."default",
    CONSTRAINT "MST_INGREDIENTS_PK" PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.mst_ingredients
    OWNER to postgres;
COMMENT ON TABLE public.mst_ingredients
    IS '材料マスタ';

COMMENT ON COLUMN public.mst_ingredients.id
    IS 'ユニークID';

COMMENT ON COLUMN public.mst_ingredients.ing_no
    IS '材料番号';

COMMENT ON COLUMN public.mst_ingredients.ing_name
    IS '材料名';

COMMENT ON COLUMN public.mst_ingredients.ing_cat_id
    IS '材料カテゴリーID';

COMMENT ON COLUMN public.mst_ingredients.stock_unit
    IS '在庫単位';

COMMENT ON COLUMN public.mst_ingredients.consumption_unit
    IS '消費単位';

COMMENT ON COLUMN public.mst_ingredients.unit_conv_rate
    IS '単位換算レート（在庫単位/消耗単位）';

COMMENT ON COLUMN public.mst_ingredients.ave_price
    IS '平均単価';

COMMENT ON COLUMN public.mst_ingredients.create_date
    IS '作成日';

COMMENT ON COLUMN public.mst_ingredients.create_user_id
    IS '作成者';

COMMENT ON COLUMN public.mst_ingredients.create_program
    IS '作成プログラム';

COMMENT ON COLUMN public.mst_ingredients.last_update_date
    IS '最終更新日';

COMMENT ON COLUMN public.mst_ingredients.last_update_user_id
    IS '最終更新者';

COMMENT ON COLUMN public.mst_ingredients.last_update_program
    IS '最終更新プログラム';





-- SEQUENCE: public.mst_ingredients_cat_id_seq

-- DROP SEQUENCE public.mst_ingredients_cat_id_seq;

CREATE SEQUENCE public.mst_ingredients_cat_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.mst_ingredients_cat_id_seq
    OWNER TO postgres;
-- Table: public.mst_ingredients_cat

-- DROP TABLE public.mst_ingredients_cat;

CREATE TABLE public.mst_ingredients_cat
(
    id integer NOT NULL DEFAULT nextval('mst_ingredients_cat_id_seq'::regclass),
    cat_no integer,
    cat_name character varying(32) COLLATE pg_catalog."default",
    explanation character varying(64) COLLATE pg_catalog."default",
    parent_id integer,
    hierarchy_path character varying(256) COLLATE pg_catalog."default",
    create_date timestamp(6) without time zone,
    create_user_id integer,
    create_program character varying(128) COLLATE pg_catalog."default",
    last_update_date timestamp(6) without time zone,
    last_update_user_id integer,
    last_update_program character varying(128) COLLATE pg_catalog."default",
    CONSTRAINT "MST_INGREDIENTS_CAT_PK" PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.mst_ingredients_cat
    OWNER to postgres;
COMMENT ON TABLE public.mst_ingredients_cat
    IS '材料カテゴリーマスタ';

COMMENT ON COLUMN public.mst_ingredients_cat.id
    IS 'ユニークID';

COMMENT ON COLUMN public.mst_ingredients_cat.cat_no
    IS 'カテゴリー番号';

COMMENT ON COLUMN public.mst_ingredients_cat.cat_name
    IS 'カテゴリー名';

COMMENT ON COLUMN public.mst_ingredients_cat.explanation
    IS '説明';

COMMENT ON COLUMN public.mst_ingredients_cat.parent_id
    IS '親ID';

COMMENT ON COLUMN public.mst_ingredients_cat.hierarchy_path
    IS '階層パス';

COMMENT ON COLUMN public.mst_ingredients_cat.create_date
    IS '作成日';

COMMENT ON COLUMN public.mst_ingredients_cat.create_user_id
    IS '作成者';

COMMENT ON COLUMN public.mst_ingredients_cat.create_program
    IS '作成プログラム';

COMMENT ON COLUMN public.mst_ingredients_cat.last_update_date
    IS '最終更新日';

COMMENT ON COLUMN public.mst_ingredients_cat.last_update_user_id
    IS '最終更新者';

COMMENT ON COLUMN public.mst_ingredients_cat.last_update_program
    IS '最終更新プログラム';