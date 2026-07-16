import json

import frappe
from frappe import _

from sva_frappe.controllers.geography.geography_merge import LEVEL_FIELDS, merge_full_path


def _existing_rows(doc):
	return [{field: row.get(field) for field in LEVEL_FIELDS} for row in doc.geography_details]


def _get_or_create_geography_details(document_type, docname):
	filters = {"document_type": document_type, "docname": docname}
	exists = frappe.db.exists("Geography Details", filters)
	if exists:
		doc = frappe.get_doc("Geography Details", exists)
	else:
		doc = frappe.new_doc("Geography Details")
		doc.update(filters)
	return doc


@frappe.whitelist()
def get_states(filters):
	if isinstance(filters, str):
		filters = json.loads(filters)
	"""Get all active states"""
	states = frappe.get_all(
		"State",
		fields=["name", "state_name", "state_code"],
		filters=[["status", "=", "Active"]] + (filters if filters else []),
		order_by="state_name",
	)
	return states


@frappe.whitelist()
def get_districts(state=None, filters=None):
	"""Get districts for given state(s)"""
	if isinstance(filters, str):
		filters = json.loads(filters)
	_filters = [["District", "status", "=", "Active"]]
	if state:
		if isinstance(state, str):
			state = json.loads(state)

		_filters.append(["District", "state", "in", state])

	districts = frappe.get_all(
		"District",
		fields=["name", "district_name", "district_code", "state"],
		filters=_filters + (filters if filters else []),
		order_by="district_name",
	)
	return districts


@frappe.whitelist()
def get_blocks(district=None, filters=None):
	"""Get blocks for given district(s)"""
	if isinstance(filters, str):
		filters = json.loads(filters)
	_filters = [["Block", "status", "=", "Active"]]
	if district:
		if isinstance(district, str):
			district = json.loads(district)
		_filters.append(["Block", "district", "in", district])

	blocks = frappe.get_all(
		"Block",
		fields=["name", "block_name", "block_code", "district", "state"],
		filters=_filters + (filters if filters else []),
		order_by="block_name",
	)
	return blocks


@frappe.whitelist()
def get_gram_panchayats(block=None, filters=None):
	"""Get gram panchayats for given block(s)"""
	if isinstance(filters, str):
		filters = json.loads(filters)
	_filters = [["Gram Panchayat", "status", "=", "Active"]]
	if block:
		if isinstance(block, str):
			block = json.loads(block)
		_filters.append(["Gram Panchayat", "block", "in", block])

	gram_panchayats = frappe.get_all(
		"Gram Panchayat",
		fields=["name", "gram_pachayat_name", "gram_panchayat_code", "block", "district", "state"],
		filters=_filters + (filters if filters else []),
		order_by="gram_pachayat_name",
	)
	return gram_panchayats


@frappe.whitelist()
def get_villages(gram_panchayat=None, filters=None):
	"""Get villages for given gram panchayat(s)"""
	if isinstance(filters, str):
		filters = json.loads(filters)
	_filters = [["Village", "status", "=", "Active"]]
	if gram_panchayat:
		if isinstance(gram_panchayat, str):
			gram_panchayat = json.loads(gram_panchayat)
		_filters.append(["Village", "gram_panchayat", "in", gram_panchayat])

	villages = frappe.get_all(
		"Village",
		fields=["name", "village_name", "village_code", "gram_panchayat", "block", "district", "state"],
		filters=_filters + (filters if filters else []),
		order_by="village_name",
	)
	return villages


@frappe.whitelist()
def save_geography_details(selection_data, document_type=None, docname=None, lowest_hierarchy=None):
	try:
		selection = json.loads(selection_data)
		filters = {"document_type": document_type, "docname": docname}
		# Check if document exists
		exists = frappe.db.exists("Geography Details", filters)
		if exists:
			# Update existing document
			doc = frappe.get_doc("Geography Details", exists)
		else:
			# Create new document with a proper name
			doc = frappe.new_doc("Geography Details")
			doc.update(filters)
		doc.set("lowest_geography_level", lowest_hierarchy)
		# Add new geography details
		doc.geography_details = []
		for item in selection:
			doc.append(
				"geography_details",
				{
					"state": item.get("state", {}).get("id"),
					"district": item.get("district", {}).get("id"),
					"block": item.get("block", {}).get("id"),
					"gram_panchayat": item.get("gramPanchayat", {}).get("id"),
					"village": item.get("village", {}).get("id"),
				},
			)
		# Save the document
		doc.insert(ignore_permissions=True) if doc.is_new() else doc.save(ignore_permissions=True)
		frappe.db.commit()
		return {"status": "success", "message": "Geography details saved successfully", "docname": doc.name}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Error in save_geography_details")
		return {"status": "error", "message": str(e)}


@frappe.whitelist()
def save_geography_level(document_type, docname, level_selections, lowest_hierarchy=None):
	"""
	Cascading, level-scoped Save used by the Geography wizard's Save button. `level_selections`
	is an ordered list of {level, scope, selected} entries, one per level from State through the
	current step's level. Each level's diff (add/cascade-delete) is applied in order, so an
	ancestor uncheck (e.g. a state) is correctly applied even when Save is triggered from a
	deeper step (e.g. Districts) - while a sibling branch that's still checked (e.g. a different
	state) is never touched, since it's still present in the State-level `selected` list.
	"""
	try:
		if isinstance(level_selections, str):
			level_selections = json.loads(level_selections)

		doc = _get_or_create_geography_details(document_type, docname)
		merged_rows = merge_full_path(_existing_rows(doc), level_selections)

		if lowest_hierarchy:
			doc.set("lowest_geography_level", lowest_hierarchy)
		doc.geography_details = []
		for row in merged_rows:
			doc.append("geography_details", row)

		doc.insert(ignore_permissions=True) if doc.is_new() else doc.save(ignore_permissions=True)
		frappe.db.commit()
		return {"status": "success", "message": "Geography details saved successfully", "docname": doc.name}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Error in save_geography_level")
		return {"status": "error", "message": str(e)}


@frappe.whitelist()
def get_geography_details(filters):
	filters = json.loads(filters) if isinstance(filters, str) else filters
	exists = frappe.db.exists("Geography Details", filters)
	if exists:
		doc = frappe.get_cached_doc("Geography Details", exists)
		return doc.as_dict()
	else:
		return None


@frappe.whitelist()
def get_user_settings():
	user_settings = frappe.get_cached_doc("User Settings")
	return user_settings


@frappe.whitelist()
def get_assigned_user_permission(allow, for_value):
	existing = frappe.get_all(
		"User Permission", filters={"allow": allow, "for_value": for_value}, fields=["user"]
	)
	result = []
	if existing:
		for user in existing:
			user_data = frappe.get_cached_value(
				"SVA User", {"email": user.user}, ["email", "role_profile", "name", "full_name"], as_dict=True
			)
			if user_data:
				result.append({
					"user": user_data.name,
					"role": user_data.role_profile,
					"user_title": user_data.get("full_name") or user_data.name,
					"user_email": user_data.email,
				})
	return result


@frappe.whitelist()
def set_assigned_user_permission(parent, assigned_roles, allow_doctype):
	if isinstance(assigned_roles, str):
		assigned_roles = json.loads(assigned_roles)
	old_users = frappe.get_all(
		"User Permission", filters={"allow": allow_doctype, "for_value": parent}, pluck="user"
	)
	old_users = {row for row in old_users}
	new_users = set()

	for role in assigned_roles:
		user_email = frappe.get_cached_value("SVA User", role.get("user"), "email")
		new_users.add(user_email)
	manage_user_permissions(parent, new_users, old_users, allow_doctype)
	return True


def manage_user_permissions(parent, new_users, old_users, allow_doctype):
	"""
	Synchronise User Permission Doc with child table.
	"""

	removed_users = old_users - new_users
	for user in removed_users:
		perms = frappe.get_all(
			"User Permission", filters={"user": user, "allow": allow_doctype, "for_value": parent}
		)
		for p in perms:
			frappe.delete_doc("User Permission", p.name, force=True)

	for user in new_users:
		existing = frappe.get_all(
			"User Permission", filters={"user": user, "allow": allow_doctype, "for_value": parent}, limit=1
		)

		if not existing:
			up = frappe.new_doc("User Permission")
			up.user = user
			up.allow = allow_doctype
			up.for_value = parent
			up.insert(ignore_permissions=True)


@frappe.whitelist()
def get_geography_details_for_modify(document_type, docname):
	"""Get geography details for modification with preserve data"""
	try:
		filters = {"document_type": document_type, "docname": docname}
		exists = frappe.db.exists("Geography Details", filters)
		if exists:
			doc = frappe.get_cached_doc("Geography Details", exists)
			return {
				"status": "success",
				"data": doc.as_dict(),
				"preserve_data": {"geography_details": doc.geography_details},
			}
		else:
			return {"status": "success", "data": None, "preserve_data": {}}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Error in get_geography_details_for_modify")
		return {"status": "error", "message": str(e)}
