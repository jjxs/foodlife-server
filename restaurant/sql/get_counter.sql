SELECT counter.*,
    total.total_price,
    pay.pay_price
FROM counter
LEFT JOIN (SELECT counter_id,
                    SUM(price) AS total_price
            FROM counter_detail_order
            LEFT JOIN order_detail_history ON order_detail_history.id = counter_detail_order.order_detail_id
            WHERE is_delete is null or (not is_delete)
            AND   price <> 0
            AND   is_ready
            GROUP BY counter_id) total ON total.counter_id = counter.id --支払金額合計
LEFT JOIN (SELECT counter_id,
                    SUM(total) AS pay_price
            FROM counter_detail 
            WHERE canceled is null or (not canceled)
            GROUP BY counter_id) pay ON pay.counter_id = counter.id --支払済み金額
WHERE 1 = 1     
{0}
ORDER BY counter.create_time DESC