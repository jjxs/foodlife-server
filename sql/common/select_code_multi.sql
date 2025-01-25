SELECT
    CODE,
    CODE_VALUE_1,
    CODE_VALUE_2,
    CODE_VALUE_3
FROM
    MST_CODE_VALUE_V
WHERE      LANGUAGE = %(language)S  AND CODE_TYPE in %(code_type_list)s
ORDER BY t.code_type