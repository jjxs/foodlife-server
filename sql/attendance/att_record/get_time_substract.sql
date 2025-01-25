SELECT
    tbl.punch_time,
    tbl.time_division
FROM
    tbl_attendance tbl
WHERE
    tbl.emp_id = %(emp_id)s 
    AND tbl.working_day = %(working_day)s
    AND ( tbl.time_division = %(start_time)s OR tbl.time_division = %(end_time)s )
ORDER BY tbl.punch_time