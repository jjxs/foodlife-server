
SELECT
    A.ID AS ID,
    A. goods_issue_number,
    A. goods_issue_quantity,
    A. base,
    A. issue_date,
    A. remarks,
    B. part_name,
    B. parts_type
    
from
    TBL_ISSUE A LEFT JOIN MST_PARTS B ON A.part_id = B.id
WHERE 1 = 1
{0}
ORDER BY A.goods_issue_number