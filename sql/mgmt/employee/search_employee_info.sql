SELECT
    emp.id,
    emp.emp_number,
    emp.emp_name,
    emp.job_code,
    emp.company_id,
    emp.employment_status,
    org.org_name,
    info.photo,
    info.last_name_kanji,
    info.last_name_kana,
    info.first_name_kana,
    info.first_name_kanji,
    info.birthday,
    info.sex,
    info.phone_number_extension,
    info.phone_number_personal,
    info.mail,
    info.postal_code,
    info.address,
    info.hire_date,
    info.employment_class,
    info.retirement_date
FROM
    mst_employee        emp
LEFT JOIN mst_employee_info   info ON info.emp_id = emp.id
LEFT JOIN mst_organization    org ON org.id = emp.org_id
WHERE
    1 = 1
and emp.id = %(emp_id)s