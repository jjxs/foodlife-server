SELECT
    mst.id,
    mst.base_code,
    mst.base_name,
    concat(mst.address_1, mst.address_2) AS address
FROM
    mst_base   mst
WHERE 1 = 1
{0}
ORDER BY mst.base_code