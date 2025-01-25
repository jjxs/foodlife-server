select distinct menu_id
from menu_free_detail
where exists 
( 
    select 1
from order_detail_menu_free detail_free
    left join "order" ord on ord.id = detail_free.order_id
where
    ord.seat_id = %(seat_id)s 
	and detail_free.usable = true
    and detail_free.end > now()
    and detail_free.menu_free_id = menu_free_detail.menu_free_id
)
