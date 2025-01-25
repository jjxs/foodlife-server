
ALTER TABLE master_data add column theme_id varchar(50) default 'default';
comment on column master_data.theme_id is '页面模板';


ALTER TABLE master_data add column menu_count numeric(8) default 9;
comment on column master_data.menu_count is 'Menu数量';