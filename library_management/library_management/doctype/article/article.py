import frappe
from frappe.model.document import Document
from datetime import date

class Article(Document):
    def before_save(self):
        self.total_qty = self.total_qty or 0
        self.issued_qty = self.issued_qty or 0
        self.available_qty = self.total_qty - self.issued_qty

        if self.available_qty > 0:
            self.status = "Available"
        else:
            self.status = "Issued"

    def validate(self):
        today = date.today().isoformat()  # 'YYYY-MM-DD'

        # New Article
        if self.is_new():
            self._validate_creation_date(today)

        # Edit Article (only if changed)
        elif self.has_value_changed("creation_date"):
            self._validate_creation_date(today)

    def _validate_creation_date(self, today):
        if self.creation_date < today:
            frappe.throw("Creation Date must be today or a future date")

    def before_save(self):
        if self.isbn:
            if not self.isbn.isdigit() or len(self.isbn) != 10:
                frappe.throw("ISBN should be with 10 characters")



