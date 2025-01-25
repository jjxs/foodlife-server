SELECT
    mst.id,
    mst.company_code,
    mst.company_name,
    mst.company_name_kana,
    mst.capital,
    mst.phone_number,
    mst.fax_number,
    mst.industry,
    base.id AS base_id,
    base.base_code,
    base.postal_code,
    concat(base.address_1, base.address_2) AS address,
    emp.emp_name,
    emp.job_code AS job,
    (
        SELECT
            COUNT(0)
        FROM
            mst_employee   emp
        WHERE
            emp.company_id = mst.id
    ) AS emp_qty
FROM
    mst_company        mst
    LEFT JOIN mst_base           base ON base.id = mst.base_id
    LEFT JOIN mst_employee       emp ON emp.id = mst.representative_id
WHERE
   mst.id = %(company_id)s