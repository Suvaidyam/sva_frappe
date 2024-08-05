import frappe
from frappe.model.document import Document

class SVAUser(Document):
	def before_save(self):
		if self.last_name:
			self.full_name = self.first_name +' '+self.last_name
		else:
			self.full_name = self.first_name
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
		new_user.username == self.username
		new_user.role_profile_name = self.role_profile
		new_user.user_image = self.user_image
		new_user.new_password = self.confirm_password
		new_user.insert(ignore_permissions=True)  # Use insert to trigger any 'before_insert' or 'after_insert' methods for User
	
	def on_update(self):
		# Update the existing User document
		if self.get('localname'):
			pass
		else:
			user_doc = frappe.get_doc("User", self.email)
			roles_profiles = frappe.db.get_list("User Role Profile",filters={'parent':self.email},fields=['name','role_profile'],ignore_permissions=True)
			roles = frappe.db.get_list("Has Role",filters={'parent':self.email},fields=['name','role'],ignore_permissions=True)
			if len(roles):
				for role in roles:
					if role.role != self.role_profile:
						frappe.delete_doc("Has Role",role.name,ignore_permissions=True)
			if len(roles_profiles):
				for role_pro in roles_profiles:
					if role_pro.role_profile != self.role_profile:
						frappe.delete_doc("User Role Profile",role_pro.name,ignore_permissions=True)
			if (self.status=='Active'):
				user_doc.enabled = True
			else:
				user_doc.enabled = False
			user_doc.email = self.email
			user_doc.first_name = self.first_name
			user_doc.middle_name = self.middle_name
			user_doc.last_name = self.last_name
			user_doc.username = self.username
			user_doc.role_profile_name = self.role_profile
			user_doc.user_image = self.user_image
			user_doc.new_password = self.confirm_password
			user_doc.save(ignore_permissions=True)  # Save with ignore_permissions to ensure it saves even without user permissions
	
	def on_trash(self):
		# Delete the associated User document if it exists
		if frappe.db.exists("User", self.email):
			frappe.delete_doc("User", self.email, ignore_permissions=True)
			frappe.msgprint(f"The user {self.email} has been deleted.")
		else:
			frappe.msgprint(f"The user {self.email} does not exist.")
