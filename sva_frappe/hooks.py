app_name = "sva_frappe"
app_title = "Sva Frappe"
app_publisher = "suvaidyam"
app_description = "customize frappe app for extra features"
app_email = "tech@suvaidyam.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sva_frappe/css/sva_frappe.css"
app_include_js = "/assets/sva_frappe/js/sva_frappe.js"

# include js, css files in header of web template
# web_include_css = "/assets/sva_frappe/css/sva_frappe.css"
web_include_js = "/assets/sva_frappe/js/sva_frappe.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sva_frappe/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Zone" : "public/js/list_utils.js",
    "State" : "public/js/sva_frappe.js",
    "District" : "public/js/sva_frappe.js",
    "Block" : "public/js/sva_frappe.js",
    "Village" : "public/js/sva_frappe.js"
    }
doctype_list_js = {
    "Zone" : "public/js/list_utils.js",
    "State" : "public/js/list_utils.js",
    "District" : "public/js/list_utils.js",
    "Block" : "public/js/list_utils.js",
    "SVA User" : "public/js/list_utils.js",
    "Village" : "public/js/list_utils.js"
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "sva_frappe/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "sva_frappe.utils.jinja_methods",
# 	"filters": "sva_frappe.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "sva_frappe.install.before_install"
# after_install = "sva_frappe.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "sva_frappe.uninstall.before_uninstall"
# after_uninstall = "sva_frappe.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "sva_frappe.utils.before_app_install"
# after_app_install = "sva_frappe.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "sva_frappe.utils.before_app_uninstall"
# after_app_uninstall = "sva_frappe.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sva_frappe.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"sva_frappe.tasks.all"
# 	],
# 	"daily": [
# 		"sva_frappe.tasks.daily"
# 	],
# 	"hourly": [
# 		"sva_frappe.tasks.hourly"
# 	],
# 	"weekly": [
# 		"sva_frappe.tasks.weekly"
# 	],
# 	"monthly": [
# 		"sva_frappe.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "sva_frappe.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "sva_frappe.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "sva_frappe.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["sva_frappe.utils.before_request"]
# after_request = ["sva_frappe.utils.after_request"]

# Job Events
# ----------
# before_job = ["sva_frappe.utils.before_job"]
# after_job = ["sva_frappe.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"sva_frappe.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

