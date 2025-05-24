import frappe
from frappe import _
from frappe.utils import cint
from datetime import datetime
from hrms.hr.doctype.employee_checkin.employee_checkin import add_log_based_on_employee_field

# custom_app.attendance.get_attendance_log
@frappe.whitelist(allow_guest=1)
def get_attendance_log():
    try:
        args = frappe.request.json
        if not args:
            frappe.throw(_("Missing request body."))

        log = args.get("RealTime")
        if not log:
            frappe.throw(_("Missing 'RealTime' in request data."))

        punch_log = log.get("PunchLog")
        if not punch_log:
            frappe.throw(_("Missing 'PunchLog' in 'RealTime' data."))

        # Fetch auth key securely
        hr_doc = frappe.get_doc("HR Settings")
        auth_key = hr_doc.get_password("auth_key")

        if log.get("AuthToken") != auth_key:
            frappe.throw(_("Invalid authentication token."))

        # Required values
        employee_field_value = punch_log.get("UserId")
        logtime = punch_log.get("LogTime")
        device_id = log.get("SerialNumber")
        action_type = punch_log.get("Type")  # Assuming 'Action' instead of 'UserId' for type

        if not (employee_field_value and logtime and device_id and action_type):
            frappe.throw(_("Missing one of the required fields: UserId, LogTime, SerialNumber, Action."))

        # Parse datetime
        try:
            cleaned_str = logtime.replace("GMT ", "")
            dt = datetime.strptime(cleaned_str, "%Y-%m-%d %H:%M:%S %z")
            timestamp = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
        except Exception as e:
            frappe.throw(_("Invalid datetime format for LogTime: {}").format(str(e)))

        # Determine IN/OUT
        log_type = "IN" if action_type == "CheckIn" else "OUT"

        # Define employee fieldname
        employee_fieldname = "attendance_device_id"  # Change to your custom link field
        employee = frappe.db.get_value(
            "Employee",
            {employee_fieldname: employee_field_value},
            ["name", "employee_name"],
            as_dict=True,
        )
        if not employee and frappe.db.exists("Employee", employee_field_value):
            frappe.db.set_value("Employee", employee_field_value, "attendance_device_id", employee_field_value)
            frappe.db.commit()

        if not employee:
            frappe.throw(
                _("No Employee found for the given employee field value. '{}': {}").format(
                    employee_fieldname, employee_field_value
                )
            )

        # Optional fields (set to None or default if not present)
        latitude = punch_log.get("Latitude", None)
        longitude = punch_log.get("Longitude", None)
        skip_auto_attendance = punch_log.get("SkipAutoAttendance", 0)

        # Create Employee Checkin
        doc = frappe.new_doc("Employee Checkin")
        doc.employee = employee.name
        doc.employee_name = employee.employee_name
        doc.time = timestamp
        doc.device_id = device_id
        doc.log_type = log_type
        doc.latitude = latitude
        doc.longitude = longitude
        if cint(skip_auto_attendance) == 1:
            doc.skip_auto_attendance = 1

        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        return {"status": "done"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Attendance Log Error"))
        return {
            "status": "error",
            "message": _("An error occurred while logging attendance."),
            "error": str(e),
        }