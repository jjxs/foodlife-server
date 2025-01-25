SELECT
    code,
    name,
    display_name,
    group_id
FROM
    mst_code_value_v
WHERE   group_id = %(group_id)s
    