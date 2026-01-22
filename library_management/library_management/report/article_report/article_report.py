import frappe
def execute(filters=None):
    if not filters:
        filters = {}
    conditions = []
    values = {}
    if filters.get("status"):
        conditions.append("status = %(status)s")
        values["status"] = filters.get("status")
    if filters.get("isbn"):
        conditions.append("isbn = %(isbn)s")
        values["isbn"] = filters.get("isbn")
    if filters.get("creation_date"):
        conditions.append("DATE(creation) = %(creation_date)s")
        values["creation_date"] = filters.get("creation_date")
    where = ""
    if conditions:
        where = "WHERE " + " AND ".join(conditions)
    query = f"""
        SELECT
            article_name,
            author,
            isbn,
            publisher,
            status,
            creation
        FROM tabArticle
        {where}
    """

    columns = [
        {"label": "Article Name", "fieldname": "article_name", "fieldtype": "Data", "width": 180},
        {"label": "Author", "fieldname": "author", "fieldtype": "Data", "width": 140},
        {"label": "ISBN", "fieldname": "isbn", "fieldtype": "Barcode", "width": 120},
        {"label": "Publisher", "fieldname": "publisher", "fieldtype": "Data", "width": 140},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": "Creation Date", "fieldname": "creation", "fieldtype": "Date", "width": 120},
    ]

    data = frappe.db.sql(query, values, as_dict=True)
    return columns, data