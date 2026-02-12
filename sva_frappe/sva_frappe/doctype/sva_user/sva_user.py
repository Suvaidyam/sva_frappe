import frappe
from frappe.model.document import Document


class SVAUser(Document):
	def before_save(self):
		# Update full name
		if self.last_name:
			self.full_name = self.first_name + " " + self.last_name
		else:
			self.full_name = self.first_name
		if isinstance(self.email, tuple):
			self.email = self.email[0]
		# Insert new permissions if they don’t exist
		for table in self.get("table_pdop", []):
			user_permission = None
			up_docs = frappe.db.get_list(
				"User Permission",
				filters={"user": self.email, "allow": table.module, "for_value": table.value},
				fields=["name"],
				limit=1,
				ignore_permissions=True,
			)
			exists = len(up_docs)
			if not exists:
				user_permission = frappe.new_doc("User Permission")
			else:
				user_permission = frappe.get_doc("User Permission", up_docs[0].name)

			user_permission.user = self.email
			user_permission.allow = table.module
			user_permission.for_value = table.value
			if not exists:
				new_doc = user_permission.insert(ignore_permissions=True)
				table.name = new_doc.name
			else:
				user_permission.save(ignore_permissions=True)

		existing_permissions = frappe.get_all(
			"User Permission", filters={"user": self.email}, fields=["name", "for_value"]
		)

		existing_for_values = {perm["for_value"]: perm["name"] for perm in existing_permissions}
		new_for_values = {table.value for table in self.get("table_pdop", [])}
		# Delete permissions that are not in the child table
		for for_value, name in existing_for_values.items():
			if for_value not in new_for_values:
				frappe.delete_doc("User Permission", name, ignore_permissions=True)

		# List of user-permission names that should exist
		up_list = [perm["name"] for perm in existing_permissions if perm["for_value"] in new_for_values]

		# Find and delete unallocated permissions
		unallocated_permissions = frappe.get_list(
			"User Permission",
			filters={"name": ["NOT IN", up_list], "user": self.email},
			pluck="name",
			ignore_permissions=True,
		)

		for name in unallocated_permissions:
			frappe.delete_doc("User Permission", name, ignore_permissions=True)

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
	if method == "on_update":
		_doc = frappe.get_doc("SVA User", {"email": doc.user}, ignore_permissions=True)
		# Check if the permission already exists
		new_entry = frappe.get_doc(
			{
				"doctype": "User Data Permissions",
				"parent": _doc.name,
				"parentfield": "table_pdop",
				"parenttype": "SVA User",
				"module": doc.allow,
				"value": doc.for_value,
			}
		)
		new_entry.insert(ignore_permissions=True)
		frappe.db.commit()

	elif method == "on_trash":
		_doc = frappe.get_doc("SVA User", {"email": doc.user}, ignore_permissions=True)

		permissions_to_delete = frappe.get_all(
			"User Data Permissions",
			filters={"parent": _doc.name, "module": doc.allow, "value": doc.for_value},
			pluck="name",  # Get only the document names
		)

		for perm_name in permissions_to_delete:
			frappe.delete_doc("User Data Permissions", perm_name, ignore_permissions=True)
		frappe.db.commit()
