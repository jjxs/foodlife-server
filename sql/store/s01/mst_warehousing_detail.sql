
SELECT
    B.ID AS ID,
    A. order_number,
    A. receipt_number,
    A. base,
    A. supplier,
    B. part_name,
    B. parts_type,
    B. part_unit,
    B. parts_unit_price_tax_inc,
    B. parts_currency,
    B. parts_receipt_qty,
    B. receipt_status_confirmation,
    B. receipt_parts_checker,
    B. remarks,
    B. receipt_id

from
    TBL_WAREHOUSING A LEFT JOIN TBL_WAREHOUSING_DETAIL B ON A.id = B.receipt_id
WHERE  A.id = %(id)s

ORDER BY A.receipt_number