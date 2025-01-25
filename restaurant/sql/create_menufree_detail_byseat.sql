select menu_free_detail.*
from menu_free_detail
where exists (select 1
              from order_detail_menu_free detail_free
                left join "order" ord on ord.id = detail_free.order_id
              where ord.seat_id = %(seat_id)s
              and   detail_free.usable = true
              and   detail_free.start is not null
              and   detail_free.end > now()
              and   detail_free.menu_free_id = menu_free_detail.menu_free_id)
and   menu_free_detail.menu_id = %(menu_id)s
limit 1 offset 0;