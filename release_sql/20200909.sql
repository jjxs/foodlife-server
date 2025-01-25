-- 订单表添加配送方式-配送1自取0
ALTER TABLE public.takeout_order
    ADD COLUMN delivery_type integer;