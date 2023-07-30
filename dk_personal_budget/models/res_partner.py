from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    """
    Partners, inherit from base module
    Added article_id and email check
    """
    _inherit = 'res.partner'

    email = fields.Char(
        index=True,
    )

    article_id = fields.Many2one(
        comodel_name='budget.article',
        name='default article'
    )

    accounting_ids = fields.One2many(
        comodel_name='budget.accounting',
        inverse_name='partner_id'
    )

    @api.constrains('email')
    def _check_unique_email(self):
        for partner in self:
            if partner.email:
                partner_with_same_email = self.search([
                    ('email', '=', partner.email),
                    ('id', '!=', partner.id),
                ], limit=1)
                if partner_with_same_email:
                    raise ValidationError(_("Email must be unique for"
                                          " each partner."))
