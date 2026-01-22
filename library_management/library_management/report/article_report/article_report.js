frappe.query_reports["Article Report"] = {
    filters: [
        {
            fieldname: "status",
            label: "Status",
            fieldtype: "Select",
            options: ["", "Available", "Issued"]
        },{
            fieldname: "isbn",
            label: "ISBN",
            fieldtype: "Barcode"
        },{
            fieldname: "creation_date",
            label: "Creation Date",
            fieldtype: "Date"
        }
    ]
};