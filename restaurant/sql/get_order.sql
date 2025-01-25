select ord.id,
       ord.order_time,
       master1.display_name as order_type_name,
       master2.display_name as order_method_name,
       usr.username as user_name,
       guest.nickname as guest_name,
       seat.id as seat_id,
       seat.seat_no as seat_no,
       seat.name as seat_name,
       case when detail_free.id is not null then True else False end as is_menu_free,
       detail_free.usable as menu_free_usable
from "order" ord
  left join auth_user usr on usr.id = ord.user_id
  left join master_data master1 on master1.id = ord.order_type_id
  left join master_data master2 on master2.id = ord.order_method_id
  left join seat on seat.id = ord.seat_id
  left join guest on guest.id = ord.guest_id
  left join seat_status on seat_status.seat_id = ord.seat_id
  left join order_detail_menu_free detail_free on detail_free.order_id = ord.id
where 1 = 1 
  {0}
  