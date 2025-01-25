SELECT
    mst.id,
    mst.company_code,
    mst.company_name,
    concat(m_base.address_1, m_base.address_2) AS address
FROM
    mst_company   mst
    LEFT JOIN mst_base      m_base ON m_base.id = mst.base_id
WHERE 1 = 1
{0}
ORDER BY mst.company_name