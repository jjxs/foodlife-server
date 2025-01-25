SELECT
    (
        SELECT
            MAX(tbl1.punch_time)
        FROM
            tbl_attendance tbl1
        WHERE
            tbl1.time_division = %(start)s
            AND tbl1.emp_id = %(emp_id)s
    ) AS start_time,
    (
        SELECT
            MAX(tbl2.punch_time)
        FROM
            tbl_attendance tbl2
        WHERE
            tbl2.time_division = %(end)s
            AND tbl2.emp_id = %(emp_id)s
    ) AS end_time
FROM
    tbl_attendance tbl
WHERE
    tbl.emp_id = %(emp_id)s
GROUP BY
    tbl.emp_id;