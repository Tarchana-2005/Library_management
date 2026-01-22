import frappe

def get_articles_in_hand(library_member):
    result = frappe.db.sql("""
        SELECT DISTINCT lt.article
        FROM `tabLibrary Transaction` lt
        WHERE
            lt.library_member = %s
            AND lt.type = 'Issue'
            AND lt.docstatus = 1
            AND lt.article NOT IN (
                SELECT article
                FROM `tabLibrary Transaction`
                WHERE
                    library_member = %s
                    AND type = 'Return'
                    AND docstatus = 1
            )
    """, (library_member, library_member), as_list=True)

    return [row[0] for row in result]
