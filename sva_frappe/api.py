import frappe
from frappe import _
import json
@frappe.whitelist()
def get_states():
    """Get all active states"""
    states = frappe.get_all('State',
        fields=['name', 'state_name', 'state_code'],
        filters={'status': 'Active'},
        order_by='state_name',
        limit=50
    )
    return states

@frappe.whitelist()
def get_districts(state=None):
    """Get districts for given state(s)"""
    filters = {'status': 'Active'}
    if state:
        state = json.loads(state)
        filters['state'] = ['in', state]
    districts = frappe.get_all('District',
        fields=['name', 'district_name', 'district_code', 'state'],
        filters=filters,
        order_by='district_name',
        limit=200
    )
    return districts

@frappe.whitelist()
def get_blocks(district=None):
    """Get blocks for given district(s)"""
    filters = {'status': 'Active'}
    if district:
       district = json.loads(district)
       filters['district'] = ['in', district]
    
    blocks = frappe.get_all('Block',
        fields=['name', 'block_name', 'block_code', 'district', 'state'],
        filters=filters,
        order_by='block_name',
        limit=300
    )
    return blocks

@frappe.whitelist()
def get_gram_panchayats(block=None):
    """Get gram panchayats for given block(s)"""
    filters = {'status': 'Active'}
    if block:
       block = json.loads(block)
       filters['block'] = ['in', block]
    
    gram_panchayats = frappe.get_all('Gram Panchayat',
        fields=['name', 'gram_pachayat_name', 'gram_panchayat_code', 'block', 'district', 'state'],
        filters=filters,
        order_by='gram_pachayat_name',
        limit=300
    )
    return gram_panchayats

@frappe.whitelist()
def get_villages(gram_panchayat=None):
    """Get villages for given gram panchayat(s)"""
    filters = {'status': 'Active'}
    if gram_panchayat:
       gram_panchayat = json.loads(gram_panchayat)
       filters['gram_panchayat'] = ['in', gram_panchayat]
    
    villages = frappe.get_all('Village',
        fields=['name', 'village_name', 'village_code', 'gram_panchayat', 'block', 'district', 'state'],
        filters=filters,
        order_by='village_name',
        limit=500
    )
    return villages

@frappe.whitelist()
def save_geography_details(selection_data, docname=None, lowest_hierarchy=None):
    try:
        selection = json.loads(selection_data)
        
        # Check if document exists
        if docname and frappe.db.exists("Watershed Management", docname):
            # Update existing document
            doc = frappe.get_doc("Watershed Management", docname)
        else:
            # Create new document with a proper name
            doc = frappe.new_doc("Watershed Management")
            # Set a default name if not provided
            if not docname:
                doc.name = frappe.generate_hash("Watershed Management", 10)
        
        # Set the lowest hierarchy
        if lowest_hierarchy:
            doc.lowest_hierarchy = lowest_hierarchy
        
        # Clear existing geography details
        doc.geography_details = []
        
        # Add new geography details
        for item in selection:
            geography_detail = {
                "state": item.get("state", {}).get("id"),
                "district": item.get("district", {}).get("id"),
                "block": item.get("block", {}).get("id"),
                "gram_panchayat": item.get("gramPanchayat", {}).get("id"),
                "village": item.get("village", {}).get("id")
            }
            doc.append("geography_details", geography_detail)
        
        # Save the document
        doc.insert() if not docname else doc.save()
        
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
