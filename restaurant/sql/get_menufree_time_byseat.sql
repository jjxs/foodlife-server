select 
    menu_free.free_type_id, 
    menu.id as menu_id, 
    menu.no as menu_no, 
    menu.name as menu_name,  
    detail_free.start,  
    detail_free.end
from order_detail_menu_free detail_free
left join "order" ord on ord.id = detail_free.order_id
left join menu_free on menu_free.id = detail_free.menu_free_id 
left join menu on menu.id = menu_free.menu_id
where
    ord.seat_id = 1
	and detail_free.usable = true;