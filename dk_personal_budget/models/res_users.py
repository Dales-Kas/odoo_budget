from odoo import models, fields


class ResUsers(models.Model):
    """
    Users, inherit from base module
    """
    _inherit = 'res.users'

    storage_id = fields.Many2one(
        comodel_name='budget.storage',
        string='Budget Storage',
    )
