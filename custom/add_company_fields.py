import frappe

def add_company_field_if_missing():
    # List of Doctypes where company field is important
    target_doctypes = [
        "Item", "Warehouse", "Customer", "Supplier", "Employee", "Sales Invoice",
        "Purchase Invoice", "Sales Order", "Purchase Order", "Journal Entry",
        "Delivery Note", "Quotation", "Asset", "Stock Entry"
    ]

    for dt in target_doctypes:
        try:
            meta = frappe.get_meta(dt)

            # Check if 'company' field already exists
            if "company" not in [df.fieldname for df in meta.fields]:
                # Create the custom field
                frappe.get_doc({
                    "doctype": "Custom Field",
                    "dt": dt,
                    "fieldname": "company",
                    "label": "Company",
                    "fieldtype": "Link",
                    "options": "Company",
                    "insert_after": "modified",  # You can change the placement
                    "default": "frappe.defaults.get_user_default('company')",
                    "reqd": 0
                }).insert(ignore_permissions=True)
                print(f"✅ Added 'company' field to {dt}")
            else:
                print(f"✔️ '{dt}' already has 'company' field")

        except Exception as e:
            print(f"⚠️ Failed to process {dt}: {str(e)}")

    frappe.db.commit()