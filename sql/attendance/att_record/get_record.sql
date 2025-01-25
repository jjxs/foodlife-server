SELECT
    working_day,
    attendance_time,
    leaving_time,
    working_time,
    break_time,
    m_code.display_name AS category,
    emp_id
FROM
    tbl_att_record     tbl
    LEFT JOIN mst_code_value_v   m_code ON m_code.group_id = 8
                                         AND m_code.code = tbl.attendance_category
WHERE
    tbl.emp_id = %(emp_id)s
    AND ( tbl.working_day >= %(startDate)s
          AND tbl.working_day <= %(endDate)s )
ORDER BY tbl.working_day