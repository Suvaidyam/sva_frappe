import frappe
from frappe import _
from frappe.utils import sha256_hash
from frappe.rate_limiter import rate_limit


@frappe.whitelist(methods=["POST"])
def impersonate(user: str, reason: str):
    allowed_roles = ["Administrator", "Impersonate User"]

    if not any(role in frappe.get_roles() for role in allowed_roles):
        frappe.throw(_("You are not allowed to impersonate users"), frappe.PermissionError)

    impersonator = frappe.session.user

    # Activity Log
    frappe.get_doc({
        "doctype": "Activity Log",
        "user": user,
        "status": "Success",
        "subject": _("User {0} impersonated as {1}").format(impersonator, user),
        "operation": "Impersonate",
    }).insert(ignore_permissions=True, ignore_links=True)

    # Notification
    notification = frappe.new_doc("Notification Log")
    notification.for_user = user
    notification.from_user = impersonator
    notification.subject = _(
        "{0} just impersonated as you. Reason: {1}"
    ).format(impersonator, reason)
    notification.type = "Alert"
    notification.insert(ignore_permissions=True)

    # Impersonate
    frappe.local.login_manager.impersonate(user)
