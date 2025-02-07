import frappe
from frappe.model.document import Document

class SVAUser(Document):
	def before_save(self):
		# Update full name
		if self.last_name:
			self.full_name = self.first_name + ' ' + self.last_name
		else:
			self.full_name = self.first_name


		# existing_permissions = frappe.get_all(
		# 	"User Permission",
		# 	filters={'user': self.email},
		# 	fields=['name', 'for_value']
		# )

		# # Extract existing 'for_value' in User Permission
		# existing_for_values = {perm['for_value']: perm['name'] for perm in existing_permissions}

		# # Extract child table 'for_value' list
		# new_for_values = {table.value for table in self.get("table_pdop", [])}

		# # Delete permissions that are not in the child table
		# for for_value, name in existing_for_values.items():
		# 	if for_value not in new_for_values:
		# 		frappe.delete_doc("User Permission", name, ignore_permissions=True)

		# list of user-permissions
		up_list = []
		# Insert new permissions if they don’t exist
		for table in self.get("table_pdop", []):
			user_permission = None
			up_docs = frappe.db.get_list("User Permission", filters={
				"user": self.email,
				"allow": table.module,
				"for_value": table.value
			},fields=['name'], limit=1)
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
				table.name= new_doc.name
			else:
				user_permission.save(ignore_permissions=True)

			up_list.append(table.name)
		unallocated_permissions = frappe.get_list("User Permission", filters={'name':['NOT IN',up_list]}, pluck='name')
		for name in unallocated_permissions:
			frappe.delete_doc("User Permission", name, ignore_permissions=True)


	def validate(self):
		# Check if password and confirm password match
		if self.password != self.confirm_password:
			frappe.throw("Password and Confirm password do not match")

	def after_insert(self):
		# Create a new User document after SVAUser is inserted
		new_user = frappe.new_doc("User")
		new_user.email = self.email
		new_user.first_name = self.first_name
		new_user.middle_name = self.middle_name
		new_user.last_name = self.last_name
		new_user.username = self.username
		new_user.mobile_no = self.mobile_number
		new_user.role_profile_name = self.role_profile
		new_user.user_image = self.user_image
		new_user.new_password = self.confirm_password
		new_user.insert(ignore_permissions=True)  # Insert to trigger 'before_insert' or 'after_insert' for User

	def on_update(self):
		# Update the existing User document
		if not self.get('localname'):
			user_doc = frappe.get_doc("User", self.email)

			# Get existing roles and role profiles
			roles_profiles = frappe.db.get_list(
				"User Role Profile", filters={'parent': self.email}, fields=['name', 'role_profile'], ignore_permissions=True
			)
			roles = frappe.db.get_list(
				"Has Role", filters={'parent': self.email}, fields=['name', 'role'], ignore_permissions=True
			)

			# Delete roles that do not match the current role profile
			for role in roles:
				if role.role != self.role_profile:
					frappe.delete_doc("Has Role", role.name, ignore_permissions=True)

			for role_pro in roles_profiles:
				if role_pro.role_profile != self.role_profile:
					frappe.delete_doc("User Role Profile", role_pro.name, ignore_permissions=True)

			# Update user status
			user_doc.enabled = self.status == 'Active'

			# Update user details
			user_doc.email = self.email
			user_doc.first_name = self.first_name
			user_doc.middle_name = self.middle_name
			user_doc.last_name = self.last_name
			user_doc.username = self.username
			user_doc.mobile_no = self.mobile_number
			user_doc.role_profile_name = self.role_profile
			user_doc.user_image = self.user_image
			user_doc.new_password = self.confirm_password
			user_doc.save(ignore_permissions=True)  # Save with ignore_permissions

	def on_trash(self):
		# Delete the associated User document if it exists
		if frappe.db.exists("User", self.email):
			frappe.delete_doc("User", self.email, ignore_permissions=True)
			frappe.msgprint(f"The user {self.email} has been deleted.")
		else:
			frappe.msgprint(f"The user {self.email} does not exist.")

@frappe.whitelist()
def on_user_permission_change(doc, method):

	if method == 'on_update':
		_doc = frappe.get_doc("SVA User", {'email': doc.user}, ignore_permissions=True)
		# Check if the permission already exists
		new_entry = frappe.get_doc({
			'doctype': 'User Data Permissions',
			'parent': _doc.name,
			'parentfield': 'table_pdop',
			'parenttype': 'SVA User',
			'module': doc.allow,
			'value': doc.for_value
		})
		new_entry.insert(ignore_permissions=True)
		frappe.db.commit()

	elif method == 'on_trash':
		_doc = frappe.get_doc("SVA User", {'email': doc.user}, ignore_permissions=True)

		permissions_to_delete = frappe.get_all(
			"User Data Permissions",
			filters={'parent': _doc.name, 'module': doc.allow, 'value': doc.for_value},
			pluck='name'  # Get only the document names
		)

		for perm_name in permissions_to_delete:
			frappe.delete_doc("User Data Permissions", perm_name, ignore_permissions=True)
		frappe.db.commit()

