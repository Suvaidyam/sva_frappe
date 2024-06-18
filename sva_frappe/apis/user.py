import frappe

@frappe.whitelist(allow_guest=True)
def get_user_permission(user, join_con=[]):
    sql_query = f"""
        SELECT
            CASE
                WHEN UP.allow = 'State' THEN TS.state_name
                WHEN UP.allow = 'District' THEN TD.district_name
                WHEN UP.allow = 'Block' THEN TB.block_name
                WHEN UP.allow = 'Village' THEN TCS.village_name
            END AS name_value,
            UP.for_value,
            UP.name,
            UP.allow,
            UP.user
        FROM `tabUser Permission` AS UP
        LEFT JOIN `tabState` AS TS ON UP.for_value = TS.name AND UP.allow = 'state'
        LEFT JOIN `tabDistrict` AS TD ON UP.for_value = TD.name AND UP.allow = 'district'
        LEFT JOIN `tabBlock` AS TB ON UP.for_value = TB.name AND UP.allow = 'block'
        LEFT JOIN `tabVillage` AS TCS ON UP.for_value = TCS.name AND UP.allow = 'village'
        WHERE UP.user = '{user}'
    """
    return frappe.db.sql(sql_query, as_dict=True)

@frappe.whitelist()
def get_user_settings():
    settings = frappe.get_doc('User Settings')
    return settings