import frappe
from frappe import _
from frappe.utils import cint
from datetime import datetime
from hrms.hr.doctype.employee_checkin.employee_checkin import add_log_based_on_employee_field

@frappe.whitelist(allow_guest=1)
def get_attendance_log():
    integration_request = None
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

        # Create Integration Request with initial status
        integration_request = frappe.get_doc({
            "doctype": "Integration Request",
            "integration_request_service": "Attendance Log",
            "reference_doctype": "Employee Checkin",
            "status": "Queued",
            "output": str(log),
        })
        integration_request.insert(ignore_permissions=True)

        # Fetch auth key securely
        hr_doc = frappe.get_doc("HR Settings")
        auth_key = hr_doc.get_password("auth_key")

        if log.get("AuthToken") != auth_key:
            integration_request.db_set("status", "Failed")
            frappe.throw(_("Invalid authentication token."))

        employee_field_value = punch_log.get("UserId")
        logtime = punch_log.get("LogTime")
        device_id = log.get("SerialNumber")
        action_type = punch_log.get("Type")

        if not (employee_field_value and logtime and device_id and action_type):
            integration_request.db_set("status", "Failed")
            frappe.throw(_("Missing one of the required fields: UserId, LogTime, SerialNumber, Action."))

        # Parse datetime
        try:
            cleaned_str = logtime.replace("GMT ", "")
            dt = datetime.strptime(cleaned_str, "%Y-%m-%d %H:%M:%S %z")
            timestamp = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
        except Exception as e:
            integration_request.db_set("status", "Failed")
            frappe.throw(_("Invalid datetime format for LogTime: {}").format(str(e)))

        log_type = "IN" if action_type == "CheckIn" else "OUT"
        employee_fieldname = "attendance_device_id"

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
            integration_request.db_set("status", "Failed")
            frappe.throw(
                _("No Employee found for the given employee field value. '{}': {}").format(
                    employee_fieldname, employee_field_value
                )
            )

        latitude = punch_log.get("Latitude", None)
        longitude = punch_log.get("Longitude", None)
        skip_auto_attendance = punch_log.get("SkipAutoAttendance", 0)

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

        # Mark Integration Request as Completed
        integration_request.db_set("status", "Completed")
        integration_request.db_set("reference_docname", doc.name)

        return {"success": "done"}

    except Exception as e:
        if integration_request:
            integration_request.db_set("status", "Failed")
        frappe.log_error(frappe.get_traceback(), _("Attendance Log Error"))
        return {
            "status": "error",
            "message": _("An error occurred while logging attendance."),
            "error": str(e),
        }
