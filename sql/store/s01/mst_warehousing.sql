
SELECT
    A.ID AS ID,
    A. order_number,
    A. receipt_number,
    B. part_name,
    A. base,
    A. supplier,
    A. remarks
    
from
    TBL_WAREHOUSING A LEFT JOIN TBL_WAREHOUSING_DETAIL B ON A.id = B.receipt_id
WHERE 1 = 1
{0}
ORDER BY A.receipt_number