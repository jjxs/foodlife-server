SELECT
    mst.id,
    mst.base_code,
    mst.base_name,
    mst.country,
    mst.state,
    mst.postal_code,
    mst.address_1,
    mst.address_2,
    mst.phone_number,
    mst.fax_number,
    mst.mail,
    emp.emp_name,
    emp.job_code AS job
FROM
    mst_base       mst
    LEFT JOIN mst_employee   emp ON emp.id = mst.contact_id
WHERE
    mst.id = %(base_id)s