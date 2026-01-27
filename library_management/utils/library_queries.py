import frappe


def get_articles_in_hand(library_member):
    """
    Returns list of article names currently issued to THIS member
    """
    if not library_member:
        return []

    issued = frappe.db.sql("""
        SELECT lt.article
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

    return [row[0] for row in issued]


def get_member_active_issue_count(library_member):
    """
    Returns how many articles are currently issued to this member
    """
    return frappe.db.count(
        "Library Transaction",
        {
            "library_member": library_member,
            "type": "Issue",
            "docstatus": 1,
        },
    )


def has_valid_membership(library_member, date):
    """
    Checks if member has valid membership on given date
    """
    return frappe.db.exists(
        "Library Membership",
        {
            "library_member": library_member,
            "docstatus": 1,
            "from_date": ("<=", date),
            "to_date": (">=", date),
        },
    )
