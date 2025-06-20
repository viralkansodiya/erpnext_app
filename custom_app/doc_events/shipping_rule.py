
import frappe
from frappe import _, msgprint, throw
from frappe.model.document import Document
from frappe.utils import flt, fmt_money


from erpnext.accounts.doctype.shipping_rule.shipping_rule import ShippingRule


class CustomShippingRule(ShippingRule):
	def apply(self, doc):
		"""Apply shipping rule on given doc. Called from accounts controller"""

		shipping_amount = 0.0
		by_value = False

		if doc.get_shipping_address():
			# validate country only if there is address
			self.validate_countries(doc)

		if self.calculate_based_on == "Net Total":
			value = doc.base_net_total
			by_value = True

		elif self.calculate_based_on == "Net Weight":
			value = doc.total_net_weight
			by_value = True

		elif self.calculate_based_on == "Fixed":
			shipping_amount = self.shipping_amount

		elif self.calculate_based_on == "Percentage":
			excluded_items = [row.items for row in self.custom_items_to_not_include_in_taxes]
			applicable_shipping_amount = 0
			for row in doc.items:
				if row.item_code in excluded_items:
					continue
				applicable_shipping_amount += row.base_amount
			if applicable_shipping_amount:
				shipping_amount = applicable_shipping_amount * self.custom_shipping_percentage / 100			

		# shipping amount by value, apply conditions
		if by_value:
			shipping_amount = self.get_shipping_amount_from_rules(value)

		# convert to order currency
		if doc.currency != doc.company_currency:
			shipping_amount = flt(shipping_amount / doc.conversion_rate, 2)

		self.add_shipping_rule_to_tax_table(doc, shipping_amount)