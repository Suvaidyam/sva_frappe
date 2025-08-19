import frappe
from frappe import _
import json

@frappe.whitelist()
def get_states(filters):
    if isinstance(filters, str):
        filters = json.loads(filters)
    """Get all active states"""
    states = frappe.get_all('State',
        fields=['name', 'state_name', 'state_code'],
        filters=[
            ["status", "=", "Active"]
        ] + (filters if filters else []),
        order_by='state_name',
        limit=50
    )
    return states

@frappe.whitelist()
def get_districts(state=None,filters=None):
    """Get districts for given state(s)"""
    if isinstance(filters, str):
        filters = json.loads(filters)
    _filters = [["District","status","=", "Active"]]
    if state:
        if isinstance(state, str):
            state = json.loads(state)
        
        
        _filters.append(["District", "state", "in", state])

    districts = frappe.get_all('District',
        fields=['name', 'district_name', 'district_code', 'state'],
        filters=_filters + (filters if filters else []),
        order_by='district_name',
        limit=200
    )
    return districts

@frappe.whitelist()
def get_blocks(district=None, filters=None):
    """Get blocks for given district(s)"""
    if isinstance(filters, str):
        filters = json.loads(filters)
    _filters = [["Block",'status',"=", 'Active']]
    if district:
        if isinstance(district, str):
            district = json.loads(district)
        _filters.append(["Block", "district", "in", district])

    blocks = frappe.get_all('Block',
        fields=['name', 'block_name', 'block_code', 'district', 'state'],
        filters=_filters + (filters if filters else []),
        order_by='block_name',
        limit=300
    )
    return blocks

@frappe.whitelist()
def get_gram_panchayats(block=None , filters=None):
    """Get gram panchayats for given block(s)"""
    if isinstance(filters, str):
        filters = json.loads(filters)
    _filters = [["Gram Panchayat", "status", "=", "Active"]]
    if block:
        if isinstance(block, str):
           block = json.loads(block)
        _filters.append(["Gram Panchayat", "block", "in", block])

    gram_panchayats = frappe.get_all('Gram Panchayat',
        fields=['name', 'gram_pachayat_name', 'gram_panchayat_code', 'block', 'district', 'state'],
        filters= _filters + (filters if filters else []),
        order_by='gram_pachayat_name',
        limit=300
    )
    return gram_panchayats

@frappe.whitelist()
def get_villages(gram_panchayat=None , filters=None):
    """Get villages for given gram panchayat(s)"""
    if isinstance(filters, str):
        filters = json.loads(filters)
    _filters = [["Village", "status", "=", "Active"]]
    if gram_panchayat:
       if isinstance(gram_panchayat, str):
           gram_panchayat = json.loads(gram_panchayat)
       _filters.append(["Village", "gram_panchayat", "in", gram_panchayat])

    villages = frappe.get_all('Village',
        fields=['name', 'village_name', 'village_code', 'gram_panchayat', 'block', 'district', 'state'],
        filters=_filters + (filters if filters else []),
        order_by='village_name',
        limit=500
    )
    return villages

@frappe.whitelist()
def save_geography_details(selection_data, document_type=None, docname=None, lowest_hierarchy=None):
    try:
        selection = json.loads(selection_data)
        filters = {
            'document_type': document_type,
            'docname': docname
        }
        # Check if document exists
        exists = frappe.db.exists('Geography Details', filters)
        if exists:
            # Update existing document
            doc = frappe.get_doc('Geography Details', exists)
        else:
            # Create new document with a proper name
            doc = frappe.new_doc('Geography Details')
            doc.update(filters)
        doc.set('lowest_geography_level', lowest_hierarchy)
        # Add new geography details
        doc.geography_details = []
        for item in selection:
            doc.append('geography_details', {
                "state": item.get("state", {}).get("id"),
                "district": item.get("district", {}).get("id"),
                "block": item.get("block", {}).get("id"),
                "gram_panchayat": item.get("gramPanchayat", {}).get("id"),
                "village": item.get("village", {}).get("id")
            })
        # Save the document
        doc.insert(ignore_permissions=True) if doc.is_new() else doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {
            "status": "success",
            "message": "Geography details saved successfully",
            "docname": doc.name
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in save_geography_details")
        return {
            "status": "error",
            "message": str(e)
        }

@frappe.whitelist()
def get_geography_details(filters):
    filters = json.loads(filters) if isinstance(filters, str) else filters
    exists = frappe.db.exists('Geography Details', filters)
    if exists:
        doc = frappe.get_cached_doc('Geography Details', exists)
        return doc.as_dict()
    else:
        return None
