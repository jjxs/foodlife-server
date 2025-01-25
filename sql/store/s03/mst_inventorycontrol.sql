
SELECT    

    B.part_name,
    B.parts_type,
    A.base,
    A.parts_theory_inventory_qty,
    A.parts_inventory_qty,
    A.parts_processing_category,
    A.part_processing_category_id,
    A.remarks,
    A.receipt_number

from
    MST_STOCK A LEFT JOIN MST_PARTS B ON A.part_id = B.id
WHERE 1=1
{0}

ORDER BY A.receipt_number


