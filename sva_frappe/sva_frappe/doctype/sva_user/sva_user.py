import frappe
from frappe.model.document import Document


class SVAUser(Document):
	def before_save(self):
		if self.last_name:
			self.full_name = self.first_name + " " + self.last_name
		else:
			self.full_name = self.first_name
		if isinstance(self.email, tuple):
			self.email = self.email[0]

		# Reject duplicate (module, value) pairs in the child table
		seen = set()
		for row in self.get("table_pdop", []):
			pair = (row.module, row.value)
			if pair in seen:
				frappe.throw(
					f"Duplicate entry in Data Permissions: <b>{row.module} — {row.value}</b> already exists at row {row.idx}."
				)
			seen.add(pair)

		# Fetch all existing User Permissions for this user in one query
		all_up = frappe.db.get_all(
			"User Permission",
			filters={"user": self.email},
			fields=["name", "allow", "for_value"],
			ignore_permissions=True,
		)
		existing_map = {(p.allow, p.for_value): p.name for p in all_up}

		# Guard prevents on_user_permission_change hook from cascading back during our sync
		frappe.flags.sva_user_permission_syncing = True
		try:
			new_pairs = set()
			for table in self.get("table_pdop", []):
				pair = (table.module, table.value)
				new_pairs.add(pair)
				if not existing_map.get(pair):
					user_permission = frappe.new_doc("User Permission")
					user_permission.user = self.email
					user_permission.allow = table.module
					user_permission.for_value = table.value
					user_permission.insert(ignore_permissions=True)

			# Delete User Permissions that are no longer in the child table
			for (allow, for_value), name in existing_map.items():
				if (allow, for_value) not in new_pairs:
					frappe.delete_doc("User Permission", name, ignore_permissions=True)
		finally:
			frappe.flags.sva_user_permission_syncing = False

		if self.status == "Inactive" and self.is_verified == 1:
			self.is_verified = 0

	def after_insert(self):
		# Create a new User document after SVAUser is inserted
		if self.get("password"):
			password = self.get_password("password")
		else:
			password = None
		new_user = frappe.new_doc("User")
		new_user.email = self.email
		new_user.first_name = self.first_name
		new_user.middle_name = self.middle_name
		new_user.last_name = self.last_name
		new_user.username = self.username if self.username else self.email
		new_user.mobile_no = self.mobile_number
		new_user.role_profile_name = self.role_profile
		new_user.user_image = self.user_image
		new_user.new_password = password
		new_user.insert(
			ignore_permissions=True
		)  # Insert to trigger 'before_insert' or 'after_insert' for User

	def on_update(self):
		# check user verified or not
		# exists = frappe.db.exists("Email Unsubscribe", {"email": self.email})
		# if not self.is_verified and not exists:
		# 	new_doc = frappe.new_doc("Email Unsubscribe")
		# 	new_doc.email = self.email
		# 	new_doc.global_unsubscribe = 1
		# 	new_doc.insert(ignore_permissions=True)
		# elif exists and self.is_verified:
		# 	frappe.delete_doc("Email Unsubscribe", exists, ignore_permissions=True)

		# Check if the user is already created
		if not self.get("localname"):
			if self.get("password"):
				password = self.get_password("password")
			else:
				password = None
			user_doc = frappe.get_doc("User", self.email)
			# Update user details
			user_doc.enabled = self.status == "Active"
			user_doc.email = self.email
			user_doc.first_name = self.first_name
			user_doc.middle_name = self.middle_name
			user_doc.last_name = self.last_name
			user_doc.username = self.username if self.username else self.email
			user_doc.mobile_no = self.mobile_number
			user_doc.user_image = self.user_image
			user_doc.new_password = password
			user_doc.role_profiles = [
				frappe.get_doc(
					{
						"doctype": "User Role Profile",
						"role_profile": self.role_profile,
						"parent": self.email,
						"parenttype": "User",
						"parentfield": "role_profiles",
					}
				).save(ignore_permissions=True)
			]
			user_doc.save(ignore_permissions=True)

	def on_trash(self):
		exists = frappe.db.exists("Email Unsubscribe", {"email": self.email})
		if exists:
			frappe.delete_doc("Email Unsubscribe", exists, ignore_permissions=True)
		# Delete the associated User document if it exists
		if frappe.db.exists("User", self.email):
			frappe.delete_doc("User", self.email, ignore_permissions=True)
			frappe.msgprint(f"The user {self.email} has been deleted.")
		else:
			frappe.msgprint(f"The user {self.email} does not exist.")


@frappe.whitelist()
def on_user_permission_change(doc, method):
	# Skip when SVA User's own before_save is managing permissions — avoids cascade
	if frappe.flags.get("sva_user_permission_syncing"):
		return

	sva_user = frappe.db.get_value("SVA User", {"email": doc.user}, "name")
	if not sva_user:
		return

	if method == "on_update":
		exists = frappe.db.exists(
			"User Data Permissions",
			{"parent": sva_user, "module": doc.allow, "value": doc.for_value},
		)
		if not exists:
			new_entry = frappe.get_doc(
				{
					"doctype": "User Data Permissions",
					"parent": sva_user,
					"parentfield": "table_pdop",
					"parenttype": "SVA User",
					"module": doc.allow,
					"value": doc.for_value,
				}
			)
			new_entry.insert(ignore_permissions=True)

	elif method == "on_trash":
		permissions_to_delete = frappe.get_all(
			"User Data Permissions",
			filters={"parent": sva_user, "module": doc.allow, "value": doc.for_value},
			pluck="name",
		)
		for perm_name in permissions_to_delete:
			frappe.delete_doc("User Data Permissions", perm_name, ignore_permissions=True)
