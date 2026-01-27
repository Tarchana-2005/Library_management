import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class LibraryTransaction(Document):
    def before_submit(self):
        if self.type == "Issue":
            self.validate_membership()
            self.validate_issue()
            self.validate_maximum_limit()

        elif self.type == "Return":
            self.set_issue_transaction()

    def on_submit(self):
        article = frappe.get_doc("Article", self.article)

        if self.type == "Issue":
            article.issued_qty = (article.issued_qty or 0) + 1

        elif self.type == "Return":
            self.update_issue_transaction()
            article.issued_qty = max((article.issued_qty or 0) - 1, 0)

            # mark linked issue as returned
            frappe.db.set_value(
                "Library Transaction",
                self.issue_transaction,
                "is_returned",
                1
            )

        self.update_article_stock(article)

    # ---------------- ON CANCEL ---------------- #

    def on_cancel(self):
        article = frappe.get_doc("Article", self.article)

        if self.type == "Issue":
            article.issued_qty = max((article.issued_qty or 0) - 1, 0)

        elif self.type == "Return":
            article.issued_qty = (article.issued_qty or 0) + 1

            frappe.db.set_value(
        "Library Transaction",
        self.issue_transaction,
        "issue_transaction",
        None
    )

        self.update_article_stock(article)

    def update_article_stock(self, article):
        total = article.total_qty or 0
        issued = article.issued_qty or 0

        article.available_qty = max(total - issued, 0)
        article.status = "Available" if article.available_qty > 0 else "Issued"
        article.save(ignore_permissions=True)

    def validate_issue(self):
        self.validate_membership()
        article = frappe.get_doc("Article", self.article)

        if article.available_qty <= 0:
            frappe.throw("This Article is Out of Stock")

        already_issued = frappe.db.exists(
        "Library Transaction",
        {
            "library_member": self.library_member,
            "article": self.article,
            "type": "Issue",
            "docstatus": 1,
            "issue_transaction": ["is", "not set"],
        }
        )

        if already_issued:
            frappe.throw(
                "This member already has this book issued. Please return it before issuing again."
            )


    def set_issue_transaction(self):
        issue_doc = frappe.db.get_value(
            "Library Transaction",
            {
                "type": "Issue",
                "library_member": self.library_member,
                "article": self.article,
                "issue_transaction": ["is", "not set"],  
                "docstatus": 1
            },
            "name"
        )

        if not issue_doc:
            frappe.throw("No active Issue record found for this book and member.")

        self.issue_transaction = issue_doc

    def update_issue_transaction(self):

        if not self.issue_transaction:
            frappe.throw("Issue Transaction not found.")

        # Update Issue record with return id
        frappe.db.set_value(
        "Library Transaction",
        self.issue_transaction,
        "issue_transaction",
        self.name
    )

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value(
            "Library Settings", "max_articles"
        )

        active_issues = frappe.db.count(
            "Library Transaction",
            {
                "library_member": self.library_member,
                "type": "Issue",
                "docstatus": DocStatus.submitted(),
                "is_returned": 0,
            },
        )

        if active_issues >= max_articles:
            frappe.throw("Maximum issue limit reached")

    def validate_membership(self):
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                "from_date": ("<", self.date),
                "to_date": (">", self.date),
            },
        )

        if not valid_membership:
            frappe.throw("The member does not have a valid membership")

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_available_articles(doctype, txt, searchfield, start, page_len, filters):

    member = filters.get("member")

    # Get active issues
    active_issues = frappe.get_all(
        "Library Transaction",
        filters={
            "type": "Issue",
            "library_member": member,
            "issue_transaction": ["is", "not set"],
            "docstatus": 1
        },
        pluck="article"
    )

    # No active issues → show all
    if not active_issues:
        return frappe.db.sql("""
            SELECT name, article_name
            FROM `tabArticle`
            WHERE name LIKE %s
            LIMIT %s OFFSET %s
        """, ("%" + txt + "%", page_len, start))

    # Exclude active ones
    return frappe.db.sql("""
        SELECT name, article_name
        FROM `tabArticle`
        WHERE name NOT IN %(articles)s
        AND name LIKE %(txt)s
        LIMIT %(limit)s OFFSET %(start)s
    """, {
        "articles": tuple(active_issues),
        "txt": "%" + txt + "%",
        "limit": page_len,
        "start": start
    })

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_issued_articles(doctype, txt, searchfield, start, page_len, filters):

    member = filters.get("member")

    return frappe.db.sql("""
        SELECT DISTINCT article, article
        FROM `tabLibrary Transaction`
        WHERE
            type = 'Issue'
            AND library_member = %(member)s
            AND issue_transaction IS NULL
            AND docstatus = 1
            AND article LIKE %(txt)s
        LIMIT %(limit)s OFFSET %(start)s
    """, {
        "member": member,
        "txt": "%" + txt + "%",
        "limit": page_len,
        "start": start
    })
