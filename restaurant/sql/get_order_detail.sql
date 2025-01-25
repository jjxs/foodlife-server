select detail.id,
       detail.order_id,
       detail.price,
       detail.count,
       detail.option,
       detail.menu_option,
       menu.id as menu_id,
       menu.no as menu_no,
       menu.name as menu_name,
       menu.tax_in as menu_tax_in,
       status.start_time as status_start,
       status.id as status_id,
       master.code as status_code,
       master.display_name as status_name,
       detail_free.id as detail_free_id,
       detail_free.start as detail_free_start,
       detail_free.end as detail_free_end,
       detail_free.usable as detail_free_usable,
       ord.seat_id
from order_detail detail
  left join menu on menu.id = detail.menu_id
  left join order_detail_status status
         on status.order_detail_id = detail.id
        and status.current = true
  left join master_data master on status.status_id = master.id
  left join order_detail_menu_free detail_free on detail_free.order_detail_id = detail.id
  left join "order" ord on ord.id = detail.order_id
  left join seat_status on seat_status.seat_id = ord.seat_id
where 1 = 1 {0}