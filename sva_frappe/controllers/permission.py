import frappe

def get_permission_query_conditions(user, doctype):
    if not user:
            return ""
    if user == "Administrator":
        return ""
    user_settings = frappe.get_cached_doc("User Settings")
    doctype_list = [item.level for item in user_settings.role_level if item.level == doctype]
    if doctype in doctype_list:
        doc = frappe.db.get_value("User Permission", {"user": user,"allow": doctype})
        user_doc = frappe.db.get_value("SVA User", {"email": user}, "role_profile")
        roles_list = [item.role for item in user_settings.role_level if item.level == doctype]
        if user_doc in roles_list:
            if not doc:
                return "1=0"
    return ""