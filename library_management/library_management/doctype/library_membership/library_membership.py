from frappe.model.document import Document
from frappe.model.docstatus import DocStatus

import frappe


class LibraryMembership(Document):
    # check before submitting this document
    def before_submit(self):
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                frappe.throw("From Date should be before To Date")
            
        exists = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                "to_date": (">", self.from_date),
            },
        )
        if exists:
            frappe.throw("There is an active membership for this member")

        # get loan period and compute to_date by adding loan_period to from_date
        loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
        self.to_date = frappe.utils.add_days(self.from_date, loan_period or 30)
