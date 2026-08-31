import frappe
from utility.utils import get_state_closure_by_type


def check_duplicate_open_request(doc):
	if doc.is_new():
		negative_closure = get_state_closure_by_type("Geography Details Modify", "Negative")
		positive_closure = get_state_closure_by_type("Geography Details Modify")

		existing_request = frappe.db.exists(
			"Geography Details Modify",
			{
				"document_type": doc.document_type,
				"docname": doc.docname,
				"workflow_state": ["not in", [negative_closure, positive_closure]],
				"name": ["!=", doc.name],
			},
		)

		if existing_request:
			frappe.throw("Already open request exists. Please wait for approval of existing request.")


def update_geography_details_modify(doc):
	positive_closure = get_state_closure_by_type("Geography Details Modify")

	if doc.workflow_state == positive_closure:
		# Check if Geography Details record exists
		geography_doc = frappe.db.exists(
			"Geography Details", {"document_type": doc.document_type, "docname": doc.docname}
		)

		if geography_doc:
			existing_doc = frappe.get_doc("Geography Details", geography_doc)
			existing_doc.lowest_geography_level = doc.lowest_geography_level
			existing_doc.geography_details = doc.geography_details
			existing_doc.save()
		else:
			# Create new Geography Details record
			new_doc = frappe.get_doc(
				{
					"doctype": "Geography Details",
					"document_type": doc.document_type,
					"docname": doc.docname,
					"lowest_geography_level": doc.lowest_geography_level,
					"geography_details": doc.geography_details,
				}
			)
			new_doc.insert()
