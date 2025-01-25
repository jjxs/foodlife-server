select
    ord.id as order_id,
    detail.id as detail_id,
    detail_free.id as detail_free_id,
    detail.count as count,
    detail.menu_id as menu_id,
    menu_free.id as menu_free_id,
    menu_free.free_type_id,
    menu_free.usable_time,
    detail_free.usable,
    detail_free.start,
    detail_free.end
from order_detail_menu_free detail_free
left join order_detail detail on detail.id = detail_free.order_detail_id
left join "order" ord on ord.id = detail_free.order_id
left join menu_free on menu_free.id = detail_free.menu_free_id 
where
ord.seat_id = %(seat_id)s 