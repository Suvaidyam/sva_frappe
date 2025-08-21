import frappe
import json

@frappe.whitelist()
def create_user_permissions(doc=None):
    document = json.loads(doc)
    allow = document.get('allow')
    for_value = document.get('for_value')
    doctype = document.get('doctype')
    user = document.get('user')
    is_zone_mandatory = frappe.db.get_single_value('User Settings','is_zone_mandatory')
    if allow =="Zone":
        exist = frappe.db.exists("User Permission", {"allow": "Zone", "for_value": for_value, "user": user})
        if not exist:
            zone_perm = frappe.get_doc({
                'doctype': 'User Permission',
                'allow': 'Zone',
                'for_value': for_value,
                'user': user
            })
            zone_perm.insert(ignore_permissions=True)
            #
    elif allow == "Company Profile":
        state_exist = frappe.db.exists("User Permission", {"allow": "Company Profile", "for_value": for_value, "user": user})

        if not state_exist:
            state_perm = frappe.get_doc({
                'doctype': 'User Permission',
                'allow': 'Company Profile',
                'for_value': for_value,
                'user': user
            })
            state_perm.insert(ignore_permissions=True)
            #
    elif allow == "State":
        state_exist = frappe.db.exists("User Permission", {"allow": "State", "for_value": for_value, "user": user})
        if is_zone_mandatory:
            zone_value = frappe.db.get_value("State", for_value, "zone")
            zone_exist = frappe.db.exists("User Permission", {"allow": "Zone", "for_value": zone_value, "user": user})
            if not zone_exist:
                zone_perm = frappe.get_doc({
                    'doctype': 'User Permission',
                    'allow': 'Zone',
                    'for_value': zone_value,
                    'user': user
                })
                zone_perm.insert(ignore_permissions=True)
        if not state_exist:
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
            if is_zone_mandatory:
                zone_value = frappe.db.get_value("State", state_value, "zone")
                zone_exist = frappe.db.exists("User Permission", {"allow": "Zone", "for_value": zone_value, "user": user})
                if not zone_exist:
                    zone_perm = frappe.get_doc({
                        'doctype': 'User Permission',
                        'allow': 'Zone',
                        'for_value': zone_value,
                        'user': user
                    })
                    zone_perm.insert(ignore_permissions=True)
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
    elif allow == "Center":
        state_value = frappe.db.get_value("Center", for_value, "state")
        dist_value = frappe.db.get_value("Center", for_value, "district")
        if state_value :
            if is_zone_mandatory:
                zone_value = frappe.db.get_value("Center", for_value, "zone")
                zone_exist = frappe.db.exists("User Permission", {"allow": "Zone", "for_value": zone_value, "user": user})
                if not zone_exist:
                    zone_perm = frappe.get_doc({
                        'doctype': 'User Permission',
                        'allow': 'Zone',
                        'for_value': zone_value,
                        'user': user
                    })
                    zone_perm.insert(ignore_permissions=True)
            state_exist = frappe.db.exists("User Permission", {"allow": "State", "for_value": state_value, "user": user})
            dist_exist = frappe.db.exists("User Permission", {"allow": "District", "for_value": dist_value, "user": user})
            center_exist = frappe.db.exists("User Permission", {"allow": "Center", "for_value": for_value, "user": user})
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
            if not center_exist:
                center_perm = frappe.get_doc({
                    'doctype': 'User Permission',
                    'allow': 'Center',
                    'for_value': for_value,
                    'user': user
                })
                center_perm.insert(ignore_permissions=True)
    elif allow == "Block":
        state_value = frappe.db.get_value("Block", for_value, "state")
        dist_value = frappe.db.get_value("Block", for_value, "district")
        if state_value and dist_value:
            if is_zone_mandatory:
                zone_value = frappe.db.get_value("State", state_value, "zone")
                zone_exist = frappe.db.exists("User Permission", {"allow": "Zone", "for_value": zone_value, "user": user})
                if not zone_exist:
                    zone_perm = frappe.get_doc({
                        'doctype': 'User Permission',
                        'allow': 'Zone',
                        'for_value': zone_value,
                        'user': user
                    })
                    zone_perm.insert(ignore_permissions=True)
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
            if is_zone_mandatory:
                zone_value = frappe.db.get_value("State", state_value, "zone")
                zone_exist = frappe.db.exists("User Permission", {"allow": "Zone", "for_value": zone_value, "user": user})
                if not zone_exist:
                    zone_perm = frappe.get_doc({
                        'doctype': 'User Permission',
                        'allow': 'Zone',
                        'for_value': zone_value,
                        'user': user
                    })
                    zone_perm.insert(ignore_permissions=True)
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

from frappe import _

@frappe.whitelist(allow_guest=True)
def get_roles_and_permissions_by_profile(role_profile):
    """Fetch roles and their assigned permissions for a given role profile."""

    # Get roles assigned to the role profile
    roles = frappe.get_all(
        "Has Role",
        filters={"parent": role_profile},
        fields=["role"],
        pluck="role"
    )

    if not len(roles):
        return {"message": "No roles found for this role profile"}

    # Define fields to fetch from permissions tables
    permission_fields = [
        "parent", "role", "permlevel", "read", "write", "create", "delete",
        "submit", "cancel", "amend", "email", "export", "import", "print",
        "report", "select", "share"
    ]

    # Fetch permissions from DocPerm
    doctypes_with_custom_perms = frappe.get_all("Custom DocPerm", pluck="parent",filters={"role": ["in", roles]}, distinct=True)
    custom_perms = frappe.get_all("Custom DocPerm", fields=permission_fields, filters={"role": ["in", roles]})
    perms = frappe.get_all("DocPerm", fields=permission_fields, filters={"role": ["in", roles], 'parent': ['not in', doctypes_with_custom_perms]})
    custom_perms.extend(perms)

    if not custom_perms:
        return {"message": "No permissions found for roles in this role profile"}

    # Formatting response
    # result = {
    #     "role_profile": role_profile,
    #     "roles_and_permissions": sorted([
    #         {field: role[field] for field in permission_fields}
    #         for role in custom_perms
    #     ], key=lambda x: (x["parent"], x["role"], x['permlevel']))
    # }
    result = {
        "role_profile": role_profile,
        "roles_and_permissions": sorted([
            {field: role[field] for field in permission_fields}
            for role in custom_perms
        ], key=lambda x: (
            x["parent"] if x["parent"] is not None else "",
            x["role"] if x["role"] is not None else "",
            x["permlevel"] if x["permlevel"] is not None else 0
        ))
    }

    return result
