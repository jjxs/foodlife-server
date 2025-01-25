-- add update time to no cache img
ALTER TABLE public.menu
    ADD COLUMN updated_at timestamp with time zone;

COMMENT ON COLUMN public.menu.updated_at
    IS 'update time';