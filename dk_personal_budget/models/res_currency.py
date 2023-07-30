from odoo import models


class Currency(models.Model):
    """
    Currencies, inherit from base module
    """
    _inherit = "res.currency"
