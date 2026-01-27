# Copyright (c) 2026, Tarchana and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryMember(Document):
	def before_validate(self):
		self.full_name = f'{self.first_name} {self.last_name or ""}'
		
	def validate(self):
		if self.phone:
			if frappe.db.exists("Library Member",{"phone" : self.phone,"name" : ("!=", self.name)}):
				frappe.throw("Phone number already exists for another member")

		if self.email_address:
			if frappe.db.exists("Library Member", {
				"email_address" : self.email_address,
				"name" : ("!=",self.name)
				}):
				frappe.throw("Email already exists for another person")




				
	
