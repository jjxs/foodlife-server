SELECT
    mst.id,
    mst.emp_number,
    mst.emp_name,
    job.display_name AS job,
    org.org_name
FROM
    mst_employee       mst
    LEFT JOIN mst_organization   org ON mst.org_id = org.id
    LEFT JOIN mst_code_value_v   job ON job.group_id = 4
                                      AND job.code = mst.job_code
WHERE 1 = 1
{0}
ORDER BY mst.emp_number