SELECT
    org.id
FROM
    mst_organization org
WHERE
    org.org_hierarchy_path LIKE %(path)s
ORDER BY
    org.id