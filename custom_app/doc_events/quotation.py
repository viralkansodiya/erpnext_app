import frappe
import json
from frappe.utils import flt

def before_save(doc, method):
    apply_item_tax_template(doc)
    total_amount = 0
    for row in doc.items:
        if frappe.db.get_value("Item", row.get("item_code"), 'additional_service_item'):
            continue
        total_amount += (row.get("qty") * row.get("price_list_rate")) if row.get("price_list_rate") else (row.get("qty") * row.get("rate"))
    
    for row in doc.items:
        if frappe.db.get_value("Item", row.get("item_code"), 'additional_service_item'):
            row.rate = total_amount * flt(row.percentage) / 100
            row.amount = row.rate * row.qty

def apply_item_tax_template(doc):
    max_tax = 0
    max_tax_template = None
    for row in doc.items:
        if not frappe.db.get_value("Item", row.get("item_code"), 'additional_service_item') and row.item_tax_template:
            applied_tax = row.igst_rate + row.cgst_rate + row.sgst_rate
            if applied_tax > max_tax:
                max_tax = applied_tax
                max_tax_template = row.item_tax_template
        
    if not max_tax_template:
        return
    
    for row in doc.items:
        if frappe.db.get_value("Item", row.get("item_code"), 'additional_service_item'):
            row.item_tax_template = max_tax_template
    
@frappe.whitelist()
def get_service_item_rate(doc, percentage, item_code):
    if not frappe.db.get_value("Item", item_code, 'additional_service_item'):
        return
    doc = frappe._dict(json.loads(doc))
    total_amount = 0
    for row in doc.get("items"):
        if frappe.db.get_value("Item", row.get("item_code"), 'additional_service_item'):
            continue
        total_amount += (row.get("qty") * row.get("price_list_rate")) if row.get("price_list_rate") else (row.get("qty") * row.get("rate"))

    return total_amount * flt(percentage) / 100
    


def before_insert(doc, method):
    max_tax = 0
    max_tax_template = None
    for row in doc.items:
        if not frappe.db.get_value("Item", row.get("item_code"), 'additional_service_item') and row.item_tax_template:
            applied_tax = row.igst_rate + row.cgst_rate + row.sgst_rate
            if applied_tax > max_tax:
                max_tax = applied_tax
                max_tax_template = row.item_tax_template
    if not max_tax_template:
        return
    for row in doc.items:
        if frappe.db.get_value("Item", row.get("item_code"), 'additional_service_item'):
            row.item_tax_template = max_tax_template


    total_amount = 0
    for row in doc.items:
        if frappe.db.get_value("Item", row.get("item_code"), 'additional_service_item'):
            continue
        total_amount += (row.get("qty") * row.get("price_list_rate")) if row.get("price_list_rate") else (row.get("qty") * row.get("rate"))
    
    for row in doc.items:
        if frappe.db.get_value("Item", row.get("item_code"), 'additional_service_item'):
            row.rate = total_amount * flt(row.percentage) / 100
            row.amount = row.rate * row.qty