# Copyright (c) 2025, suvaidyam and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class GeographyDetails(Document):
    def on_update(self):
        if not self.lowest_geography_level:
            return

        levels = ["state", "district", "block", "gram_panchayat", "village"]
        current = {
            "State": "state",
            "District": "district",
            "Block": "block",
            "Gram Panchayat": "gram_panchayat",
            "Village": "village",
        }.get(self.lowest_geography_level)

        fields = levels[levels.index(current) + 1:]
        if not fields:
            return
        if any(row.get(f) for row in self.geography_details for f in fields):
            for row in self.geography_details:
                for f in fields:
                    print(f"Clearing field: {f} for row: {row.name}")
                    row.set(f, None)
                    row.set(f"{f}_name", None)