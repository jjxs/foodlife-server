SELECT
    mst.id,
    mst.org_hierarchy_path,
    mst.org_code,
    mst.org_name,
    mst.company_id,
    mst.base_id,
    org.upper_organization_id,
    org.org_name   AS upper_organization_name,
    chief.emp_name     AS chief_name,
    contact.emp_name   AS contact_name,
    mst.phone_number,
    mst.fax_number
FROM
    mst_organization   mst
    LEFT JOIN mst_employee       chief ON chief.id = mst.org_chief_id
    LEFT JOIN mst_employee       contact ON contact.id = mst.contact_id
    LEFT JOIN mst_organization   org ON org.id = mst.upper_organization_id
WHERE
    mst.id = %(org_id)s