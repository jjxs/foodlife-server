
SELECT
    A.ID AS ID,
    A. order_date,
    A. order_number,
    A. orderer,
    A. order_address,
    A. order_phone_number,
    A. order_summary
    
from
    TBL_ORDER A LEFT JOIN TBL_ORDER_DETAIL B ON A.id = B.ordering_table_unique_id
WHERE 1 = 1
{0}
ORDER BY A.order_number