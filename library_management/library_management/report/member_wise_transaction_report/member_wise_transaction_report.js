frappe.query_reports["Member-wise Transaction Report"] = {
    filters: [
        {
            fieldname: "library_member",
            label: "Library Member",
            fieldtype: "Link",
            options: "Library Member"
        },
        {
            fieldname: "article",
            label: "Article",
            fieldtype: "Link",
            options: "Article"
        },
        {
            fieldname: "type",
            label: "Transaction Type",
            fieldtype: "Select",
            options: ["", "Issued", "Return"]
        }
    ]
};
