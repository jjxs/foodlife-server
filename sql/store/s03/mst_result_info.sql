
SELECT    

    A.part_name,
    A.parts_type,
    B.base,
    B.parts_theory_inventory_qty,
    C.id AS insp_id,
    C.parts_inventory_qty,
    C.part_id,
    B.remarks

from
    MST_PARTS A INNER JOIN MST_STOCK B ON A.id = B.part_id
    INNER JOIN TBL_INSPECTION C ON B.part_id = C.part_id
    
WHERE inspection_delete = 0 OR inspection_delete IS NULL
