##############################################################################
#
#    Copyright (C) 2017 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: Emanuel Cino <ecino@compassion.ch>
#
#    The licence is in the file __manifest__.py
#
##############################################################################
from datetime import date, datetime

from babel.dates import format_date

from odoo import _, models


class ResPartner(models.Model):
    """Add fields for retrieving values for communications."""

    _inherit = "res.partner"

    def get_receipt_text(self, year):
        """Formats the donation amount for the tax receipt."""
        return f"{self.get_receipt(year):,.2f}".replace(".00", ".-").replace(",", "'")

    def get_receipt(self, year):
        """
        Return the amount paid from the partner in the given year
        :param year: int: year of selection
        :return: float: total amount
        """
        self.ensure_one()
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        invoice_lines = self.env["account.move.line"].search(
            [
                ("last_payment", ">=", start_date),
                ("last_payment", "<=", end_date),
                ("payment_state", "=", "paid"),
                ("product_id.requires_thankyou", "=", True),
                # invoice from either the partner, the company or the employee
                # to obtain the same results when tax receipt is computed
                # from companies or employees
                "|",
                # invoice from the partner (when self is either an company
                # or an employee)
                ("partner_id", "=", self.id),
                "|",
                # invoice from the company (when self is an employee)
                ("partner_id.parent_id", "=", self.id),
                # invoice from the employees (when self is a company)
                ("partner_id.child_ids", "=", self.id),
            ]
        )
        return sum(invoice_lines.mapped("price_subtotal"))

    def _compute_date_communication(self):
        """City and date displayed in the top right of a letter for Yverdon"""
        today = datetime.today()
        city = _("Yverdon-les-Bains")
        for partner in self:
            date = format_date(today, format="long", locale=partner.lang)
            formatted_date = f"le {date}" if "fr" in partner.lang else date
            partner.date_communication = f"{city}, {formatted_date}"
