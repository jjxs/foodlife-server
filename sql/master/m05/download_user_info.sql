SELECT
    MU.ID                      AS ID,
    MU.USER_ACCOUNT            AS USER_ACCOUNT,
    MU.USER_NAME               AS USER_NAME,
    M_GROUP.CODE_VALUE_1       AS USER_GROUP,
    M_JOBSYSTEM.CODE_VALUE_1   AS USER_JOBSYSTEM,
    M_AUTHORITY.CODE_VALUE_1   AS WF_AUTHORITY,
    MU.EMAIL,
    M_LANGUAGE.CODE_VALUE_1    AS LANGUAGE,
    MO.ORG_NAME                AS ORG_NAME
FROM
    MST_USER MU
    LEFT JOIN MST_CODE_VALUE_V     M_GROUP ON M_GROUP.CODE_TYPE = '0040'
                                   AND M_GROUP.CODE = MU.USER_GROUP
                                   AND M_GROUP.LANGUAGE = %(LANGUAGE)s
    LEFT JOIN MST_CODE_VALUE_V         M_JOBSYSTEM ON M_JOBSYSTEM.CODE_TYPE = '0041'
                                       AND M_JOBSYSTEM.CODE = MU.USER_JOBSYSTEM
                                       AND M_JOBSYSTEM.LANGUAGE = %(LANGUAGE)s
    LEFT JOIN MST_CODE_VALUE_V         M_AUTHORITY ON M_AUTHORITY.CODE_TYPE = '0020'
                                       AND M_AUTHORITY.CODE = MU.WF_AUTHORITY
                                       AND M_AUTHORITY.LANGUAGE = %(LANGUAGE)s
    LEFT JOIN MST_CODE_VALUE_V         M_LANGUAGE ON M_LANGUAGE.CODE_TYPE = '0010'
                                      AND M_LANGUAGE.CODE = MU.LANGUAGE
                                      AND M_LANGUAGE.LANGUAGE = %(LANGUAGE)s
    LEFT JOIN MST_ORG_USER_RELATION   MOR ON MOR.USER_ID = MU.ID
                                      AND MOR.DISPLAY_SEQ = 1
    LEFT JOIN MST_ORGANIZATION        MO ON MO.ID = MOR.ORG_ID

WHERE 1 = 1
{0}