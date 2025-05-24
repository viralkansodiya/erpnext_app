import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def setup_custom_fields():
    """Setup custom fields for Referral Practitioner Integration"""
    custom_fields = {
        "HR Settings": [
            {
                "fieldname": "auth_key",
                "label": "Authentication Key",
                "description" : "For Attendance Mapping",
                "fieldtype": "Password",
                "insert_after" :"retirement_age"
            }
        ],
    }
    create_custom_fields(custom_fields)
    print("Custom Fields for Referral Practitioner Integration created successfully")