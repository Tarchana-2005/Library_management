import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class LibraryTransaction(Document):

    def before_submit(self):
        if self.type == "Issue":
            self.validate_issue()
            self.validate_maximum_limit()

        elif self.type == "Return":
            self.validate_return()

    def on_submit(self):
        article = frappe.get_doc("Article", self.article)

        if self.type == "Issue":
            if article.available_qty <= 0:
                frappe.throw("No stock available for this Article")

            article.issued_qty = (article.issued_qty or 0) + 1
            article.total_sold = (article.total_sold or 0) + 1

        elif self.type == "Return":
            if article.issued_qty <= 0:
                frappe.throw("Invalid Return: No issued stock exists")

            article.issued_qty = article.issued_qty - 1

        # Recalculate available quantity
        article.available_qty = (article.total_qty or 0) - article.issued_qty

        # Update status
        if article.available_qty > 0:
            article.status = "Available"
        else:
            article.status = "Issued"

        article.save(ignore_permissions=True)

    def on_cancel(self):
        article = frappe.get_doc("Article", self.article)

        if self.type == "Issue":
            article.issued_qty = article.issued_qty - 1

        elif self.type == "Return":
            article.issued_qty = article.issued_qty + 1

        article.available_qty = (article.total_qty or 0) - article.issued_qty

        if article.available_qty > 0:
            article.status = "Available"
        else:
            article.status = "Issued"

        article.save(ignore_permissions=True)

    def validate_issue(self):
        self.validate_membership()
        article = frappe.get_doc("Article", self.article)

        if article.available_qty <= 0:
            frappe.throw("This Article is Out of Stock")

    def validate_return(self):
        article = frappe.get_doc("Article", self.article)

        if article.issued_qty <= 0:
            frappe.throw("This Article is not currently issued")

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")

        count = frappe.db.count(
            "Library Transaction",
            {
                "library_member": self.library_member,
                "type": "Issue",
                "docstatus": DocStatus.submitted(),
            },
        )

        if count >= max_articles:
            frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                "from_date": ("<=", self.date),
                "to_date": (">=", self.date),
            },
        )

        if not valid_membership:
            frappe.throw("The member does not have a valid membership")
