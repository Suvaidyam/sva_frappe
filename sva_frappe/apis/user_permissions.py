import frappe
import json

@frappe.whitelist()
def create_user_permissions(doc=None):
    document = json.loads(doc)
    allow = document.get('allow')
    for_value = document.get('for_value')
    doctype = document.get('doctype')
    user = document.get('user')
    
    if allow == "State":
        exist = frappe.db.exists("User Permission", {"allow": "State", "for_value": for_value, "user": user})
        if not exist:
            state_perm = frappe.get_doc({
                'doctype': 'User Permission',
                'allow': 'State',
                'for_value': for_value,
                'user': user
            })
            state_perm.insert(ignore_permissions=True)
    elif allow == "District":
        state_value = frappe.db.get_value("District", for_value, "state")
        if state_value:
            state_exist = frappe.db.exists("User Permission", {"allow": "State", "for_value": state_value, "user": user})
            dist_exist = frappe.db.exists("User Permission", {"allow": "District", "for_value": for_value, "user": user})
            if not state_exist:
                state_perm = frappe.get_doc({
                    'doctype': 'User Permission',
                    'allow': 'State',
                    'for_value': state_value,
                    'user': user
                })
                state_perm.insert(ignore_permissions=True)
            if not dist_exist:
                dist_perm = frappe.get_doc({
                    'doctype': 'User Permission',
                    'allow': 'District',
                    'for_value': for_value,
                    'user': user
                })
                dist_perm.insert(ignore_permissions=True)
    elif allow == "Block":
        state_value = frappe.db.get_value("Block", for_value, "state")
        dist_value = frappe.db.get_value("Block", for_value, "district")
        if state_value and dist_value:
            state_exist = frappe.db.exists("User Permission", {"allow": "State", "for_value": state_value, "user": user})
            dist_exist = frappe.db.exists("User Permission", {"allow": "District", "for_value": dist_value, "user": user})
            block_exist = frappe.db.exists("User Permission", {"allow": "Block", "for_value": for_value, "user": user})
            if not state_exist:
                state_perm = frappe.get_doc({
                    'doctype': 'User Permission',
                    'allow': 'State',
                    'for_value': state_value,
                    'user': user
                })
                state_perm.insert(ignore_permissions=True)
            if not dist_exist:
                dist_perm = frappe.get_doc({
                    'doctype': 'User Permission',
                    'allow': 'District',
                    'for_value': dist_value,
                    'user': user
                })
                dist_perm.insert(ignore_permissions=True)
            if not block_exist:
                block_perm = frappe.get_doc({
                    'doctype': 'User Permission',
                    'allow': 'Block',
                    'for_value': for_value,
                    'user': user
                })
                block_perm.insert(ignore_permissions=True)
    elif allow == "Grampanchayat":
        state_value = frappe.db.get_value("Grampanchayat", for_value, "state")
        dist_value = frappe.db.get_value("Grampanchayat", for_value, "district")
        block_value = frappe.db.get_value("Grampanchayat", for_value, "block")
        if state_value and dist_value and block_value:
            state_exist = frappe.db.exists("User Permission", {"allow": "State", "for_value": state_value, "user": user})
            dist_exist = frappe.db.exists("User Permission", {"allow": "District", "for_value": dist_value, "user": user})
            block_exist = frappe.db.exists("User Permission", {"allow": "Block", "for_value": block_value, "user": user})
            grampanchayat_exist = frappe.db.exists("User Permission", {"allow": "Grampanchayat", "for_value": for_value, "user": user})
            if not state_exist:
                state_perm = frappe.get_doc({
                    'doctype': 'User Permission',
                    'allow': 'State',
                    'for_value': state_value,
                    'user': user
                })
                state_perm.insert(ignore_permissions=True)
            if not dist_exist:
                dist_perm = frappe.get_doc({
                    'doctype': 'User Permission',
                    'allow': 'District',
                    'for_value': dist_value,
                    'user': user
                })
                dist_perm.insert(ignore_permissions=True)
            if not block_exist:
                block_perm = frappe.get_doc({
                    'doctype': 'User Permission',
                    'allow': 'Block',
                    'for_value': block_value,
                    'user': user
                })
                block_perm.insert(ignore_permissions=True)
            if not grampanchayat_exist:
                gp_perm = frappe.get_doc({
                    'doctype': 'User Permission',
                    'allow': 'Grampanchayat',
                    'for_value': for_value,
                    'user': user
                })
                gp_perm.insert(ignore_permissions=True)
    elif allow == "Village":
        state_value = frappe.db.get_value("Village", for_value, "state")
        dist_value = frappe.db.get_value("Village", for_value, "district")
        block_value = frappe.db.get_value("Village", for_value, "block")
        gp_value = frappe.db.get_value("Village", for_value, "grampanchayat")
        if state_value and dist_value and block_value and gp_value:
            state_exist = frappe.db.exists("User Permission", {"allow": "State", "for_value": state_value, "user": user})
            dist_exist = frappe.db.exists("User Permission", {"allow": "District", "for_value": dist_value, "user": user})
            block_exist = frappe.db.exists("User Permission", {"allow": "Block", "for_value": block_value, "user": user})
            gp_exist = frappe.db.exists("User Permission", {"allow": "Grampanchayat", "for_value": gp_value, "user": user})
            village_exist = frappe.db.exists("User Permission", {"allow": "Village", "for_value": for_value, "user": user})
            if not state_exist:
                state_perm = frappe.get_doc({
                    'doctype': 'User Permission',
                    'allow': 'State',
                    'for_value': state_value,
                    'user': user
                })
                state_perm.insert(ignore_permissions=True)
            if not dist_exist:
                dist_perm = frappe.get_doc({
                    'doctype': 'User Permission',
                    'allow': 'District',
                    'for_value': dist_value,
                    'user': user
                })
                dist_perm.insert(ignore_permissions=True)
            if not block_exist:
                block_perm = frappe.get_doc({
                    'doctype': 'User Permission',
                    'allow': 'Block',
                    'for_value': block_value,
                'user': user
            })
            block_perm.insert(ignore_permissions=True)
            if not gp_exist:
                gp_perm = frappe.get_doc({
                    'doctype': 'User Permission',
                    'allow': 'Grampanchayat',
                    'for_value': gp_value,
                    'user': user
                })
                gp_perm.insert(ignore_permissions=True)
            if not village_exist:
                village_perm = frappe.get_doc({
                    'doctype': 'User Permission',
                    'allow': 'Village',
                    'for_value': for_value,
                    'user': user
                })
                village_perm.insert(ignore_permissions=True)
    else:
        return "Invalid allow value"