from odoo import models, fields


class BudgetStorage(models.Model):
    """
    Model representing locations for managing money storage.

    This model is used to store and manage information about budget storage
    locations, which represent physical or virtual places where money is stored
    or managed. Each entry in this model corresponds to a specific location
    for managing money.
    """
    _name = 'budget.storage'
    _description = 'money storage location'

    name = fields.Char(
        required=True,
        translate=True,
    )
    user_id = fields.Many2one(
        comodel_name='res.users'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
    )
    accounting_ids = fields.One2many(
        comodel_name='budget.accounting',
        inverse_name='storage_id',
    )
