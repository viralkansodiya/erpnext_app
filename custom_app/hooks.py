app_name = "custom_app"
app_title = "Rejith"
app_publisher = "rejith"
app_description = "Naming App"
app_email = "rejithr1995@gmail.com"
app_license = "agpl-3.0"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "custom_app",
# 		"logo": "/assets/custom_app/logo.png",
# 		"title": "naming",
# 		"route": "/custom_app",
# 		"has_permission": "custom_app.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/custom_app/css/custom_app.css"
# app_include_js = "/assets/custom_app/js/custom_app.js"

# include js, css files in header of web template
# web_include_css = "/assets/custom_app/css/custom_app.css"
# web_include_js = "/assets/custom_app/js/custom_app.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "custom_app/public/scss/website"
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            ["module", "=", "Elina"]
        ]
    },
    {
        "dt": "Property Setter",
        "filters": [
            ["module", "=", "Elina"]
        ]
    }
]
# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}
after_migrate = "custom_app.custom_field.setup_custom_fields"
# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Quotation" : "public/js/quotation.js"
    }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "custom_app/public/icons.svg"

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
# 	"methods": "custom_app.utils.jinja_methods",
# 	"filters": "custom_app.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "custom_app.install.before_install"
# after_install = "custom_app.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "custom_app.uninstall.before_uninstall"
# after_uninstall = "custom_app.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "custom_app.utils.before_app_install"
# after_app_install = "custom_app.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "custom_app.utils.before_app_uninstall"
# after_app_uninstall = "custom_app.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "custom_app.notifications.get_notification_config"

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

override_doctype_class = {
	"Shipping Rule": "custom_app.doc_events.shipping_rule.CustomShippingRule"
}

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
doc_events = {
    "Item": {
        "before_insert": "custom_app.custom_script.autoname"
    },
    "Quotation": {
        "before_save": "custom_app.doc_events.quotation.before_save",
        "before_insert" : "custom_app.doc_events.quotation.before_insert"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"custom_app.tasks.all"
# 	],
# 	"daily": [
# 		"custom_app.tasks.daily"
# 	],
# 	"hourly": [
# 		"custom_app.tasks.hourly"
# 	],
# 	"weekly": [
# 		"custom_app.tasks.weekly"
# 	],
# 	"monthly": [
# 		"custom_app.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "custom_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "custom_app.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "custom_app.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["custom_app.utils.before_request"]
# after_request = ["custom_app.utils.after_request"]

# Job Events
# ----------
# before_job = ["custom_app.utils.before_job"]
# after_job = ["custom_app.utils.after_job"]

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
# 	"custom_app.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
