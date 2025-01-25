select 
ord.id as order_id ,
ord.order_time as order_time,
ord.ship_addr,
ord.ship_name,
ord.ship_tel,
ord.ship_time,
detail.id as detail_id,
detail.count as count,
detail.menu_option,
menu.id as menu_id,
menu.no as menu_no,
menu.name as menu_name,
menu.note as menu_note,
menu.image as menu_image,
detail.price as price,
detail.option as option,
seat.id as seat_id,
seat.seat_no as seat_no,
seat.name as seat_name,
status.id as detail_status_id,
master.code as status_code,
usr.username as status_username
from order_detail detail
left join "order" ord on ord.id = detail.order_id
left join menu on detail.menu_id = menu.id
left join order_detail_status status on status.order_detail_id = detail.id and status.current = True
left join auth_user usr on usr.id = status.user_id
left join master_data master on status.status_id = master.id 
left join seat on ord.seat_id = seat.id
{1}
where
master.code in (-1, 100, 200, 300, 999) 
{0} 
order by status.start_time

