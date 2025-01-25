ALTER TABLE order_detail add column ori_price numeric(8);
comment on column order_detail.ori_price is '原始价格';

ALTER TABLE order_detail_history add column ori_price numeric(8);
comment on column order_detail_history.ori_price is '原始价格';

ALTER TABLE counter_detail_order add column ori_price numeric(8);
comment on column counter_detail_order.ori_price is '原始价格';

ALTER TABLE menu add column ori_price numeric(8);
comment on column menu.ori_price is '原始价格';
