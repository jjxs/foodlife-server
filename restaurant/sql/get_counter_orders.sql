SELECT distinct detail.id AS detail_id,
       detail.order_id,
       detail.price,
       detail.count,
       detail.ori_price,
       menu.id AS menu_id,
       menu.no AS menu_no,
       menu.name AS menu_name,
       menu.tax_in AS tax_in,
       menu.note AS menu_note,
       master.code AS status_code,
       master.display_name AS status_name,
       detail_free.id AS detail_free_id,
       detail_free.usable AS detail_free_usable,
       ord.seat_id,
       seat.seat_no AS seat_no,
       seat.name AS seat_name,
       CASE
         WHEN detail_free.id IS NULL THEN master.code = 999
         ELSE detail_free.usable = TRUE
       END AS is_ready,
       false as is_delete,
       false as is_split,
       ord.order_time
FROM order_detail detail --明細
  LEFT JOIN "order" ord ON ord.id = detail.order_id
  INNER JOIN seat_status  
        ON seat_status.seat_id = ord.seat_id 
        and seat_status.counter_no = ord.counter_no
  LEFT JOIN menu ON menu.id = detail.menu_id
  LEFT JOIN order_detail_status status
        ON status.order_detail_id = detail.id
        AND status.current = TRUE
  LEFT JOIN master_data master ON status.status_id = master.id
  LEFT JOIN order_detail_menu_free detail_free ON detail_free.order_detail_id = detail.id
  LEFT JOIN seat ON seat.id = ord.seat_id
where seat.id in %(seat_ids)s
order by ord.order_time
