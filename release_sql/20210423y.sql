ALTER TABLE public.seat_status
    ADD COLUMN utype character varying(20);

ALTER TABLE public.seat_status_history
    ADD COLUMN utype character varying(20);