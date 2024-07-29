import frappe
class ReportFilter:
    def rport_filter_by_user_permissions(mappings):
        permissions = frappe.db.get_list("User Permission",filters={'user':frappe.session.user},fields=['allow','for_value'],ignore_permissions=True)
        conditions = []
        final_cond = None
        perm_dict = {}
        if len(permissions):
            for perm in permissions:
                perm_dict.setdefault(perm['allow'], []).append(perm['for_value'])
        for key, values in perm_dict.items():
            if key in mappings and key and values:
                alias, column = mappings[key]
                if alias == 'no_alias':
                    formatted_values = ', '.join(f"'{value}'" for value in values)
                    conditions.append(f"{column} IN ({formatted_values})")
                else:
                    formatted_values = ', '.join(f"'{value}'" for value in values)
                    conditions.append(f"{alias}.{column} IN ({formatted_values})")
        return ' AND '.join(conditions) if len(conditions) else None