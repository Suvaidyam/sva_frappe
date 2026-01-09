# Copyright (c) 2026, suvaidyam and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from sva_frappe.controllers.geography.geography_modify import update_geography_details_modify, check_duplicate_open_request


class GeographyDetailsModify(Document):
	def validate(self):
		check_duplicate_open_request(self)
	
	def on_update(self):
		update_geography_details_modify(self)
