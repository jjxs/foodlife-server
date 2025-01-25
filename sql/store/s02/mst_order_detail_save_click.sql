
SELECT
    B.ID AS ID,
    B.part_name,
    B.parts_type,
    B.parts_unit_price,
    B.parts_currency,
    B.parts_qty,
    B.supplier,
    B.remarks
    
from
    TBL_ORDER A LEFT JOIN TBL_ORDER_DETAIL B ON A.id = B.ordering_table_unique_id
WHERE 
    A.id =  %(id)s
ORDER BY A.order_number