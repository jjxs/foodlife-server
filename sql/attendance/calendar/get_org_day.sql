SELECT
    tbl.id,
    tbl.holiday_class,
    tbl.date,
    tbl.name
FROM
    tbl_holiday_def tbl
WHERE
    tbl.authority_id = %(authority_id)s
ORDER BY tbl.date DESC