SELECT main.order_detail_id AS detail_id,
       detail.order_id,
       main.pay_price AS price,
       main.ori_price AS ori_price,
       main.pay_count AS count,
       main.tax_in,
       menu.id AS menu_id,
       menu.no AS menu_no,
       menu.name AS menu_name,
       menu.note AS menu_note,
       master.code AS status_code,
       master.display_name AS status_name,
       detail_free.id AS detail_free_id,
       detail_free.usable AS detail_free_usable,
       ord.seat_id,
       seat.seat_no AS seat_no,
       seat.name AS seat_name,
       main.is_ready,
       main.is_delete,
       main.is_split,
       main.tax,
       ord.order_time
FROM counter_detail_order main
  LEFT JOIN order_detail_history detail ON detail.id = main.order_detail_id
  LEFT JOIN order_history ord ON ord.id = detail.order_id
  INNER JOIN seat_status_history seat_status
          ON seat_status.seat_id = ord.seat_id
         AND seat_status.counter_no = ord.counter_no
  LEFT JOIN menu ON menu.id = detail.menu_id
  LEFT JOIN order_detail_status_history status
         ON status.order_detail_id = detail.id
        AND status.current = TRUE
  LEFT JOIN master_data master ON status.status_id = master.id
  LEFT JOIN order_detail_menu_free_history detail_free ON detail_free.order_detail_id = detail.id
  LEFT JOIN seat ON seat.id = ord.seat_id
WHERE main.counter_id = %(counter_id)s
AND   main.counter_detail_id IS NULL
order by ord.order_time

