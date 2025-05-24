import frappe

def autoname(doc, method):
    def fetch_parents(group_name, abbr_list):
        parent_group = frappe.get_value(
            "Item Group", 
            group_name, 
            ["parent_item_group", "custom_abbreviation"], 
            as_dict=True
        )
        # If we found a group and it has an abbreviation
        if parent_group and parent_group.get("custom_abbreviation"):
            abbr_list.insert(0, parent_group["custom_abbreviation"])
            # Recursively fetch the next parent
            if parent_group.get("parent_item_group"):
                abbr_list = fetch_parents(parent_group["parent_item_group"], abbr_list)
        return abbr_list

    # 1. Initialize abbreviation list
    abbr_list = []

    # 2. Get the current item's group info
    item_group_info = frappe.get_value(
        "Item Group", 
        doc.item_group, 
        ["parent_item_group", "custom_abbreviation"], 
        as_dict=True
    )

    # 3. Add the current group’s abbreviation (if any)
    if item_group_info and item_group_info.get("custom_abbreviation"):
        abbr_list.insert(0, item_group_info["custom_abbreviation"])

    # 4. If there’s a parent, recursively fetch parent groups
    if item_group_info and item_group_info.get("parent_item_group"):
        abbr_list = fetch_parents(item_group_info["parent_item_group"], abbr_list)

    # 5. Build naming series (e.g., PARENT-CHILD-.#####)
    naming_series = "-".join(abbr_list) + "-.####"
    doc.naming_series = naming_series
    if doc.variant_of:
        variant_atr = []
        for row in doc.attributes:
            if frappe.db.get_value("Item Attribute", row.attribute, "numeric_values" ):
                variant_atr.append(str(row.attribute_value))
            else:
                attr_doc = frappe.db.sql(f""" Select abbr From `tabItem Attribute Value` where parent = '{row.attribute}' and attribute_value = '{row.attribute_value}' """, as_dict=1)
                if attr_doc[0].get("abbr"):
                    variant_atr.append(str(attr_doc[0].get("abbr")))
                else:
                    variant_atr.append(str(row.attribute_value))
        variant_name = "-".join(variant_atr)
        doc.item_code = doc.variant_of + "-" + variant_name
        doc.name = doc.variant_of + "-" + variant_name
    else:
        # 6. Generate the actual doc.name
        doc.item_code = frappe.model.naming.make_autoname(naming_series)
