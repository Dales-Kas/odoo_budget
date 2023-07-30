from odoo import models, fields, _


class BudgetArticle(models.Model):
    """
    Model representing budget articles for managing expenses.

    This model is used to store and manage information about budget articles,
    which represent different categories or items for managing expenses in
    the budget.
    """
    _name = 'budget.article'
    _description = 'accounting article for managing expenses'

    name = fields.Char(
        translate=True
    )
    color = fields.Integer(
        name='Color Index',
        readonly=False
    )
    short_name = fields.Char(
        translate=True
    )
    description = fields.Text(
        translate=True
    )
    accounting_ids = fields.One2many(
        comodel_name='budget.accounting',
        inverse_name='article_id'
    )

    def action_create_operation(self):
        """
        Quick create accounting operation
        """
        self.ensure_one()
        return {
            'name': _('Add accounting operation'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'budget.accounting',
            'target': 'new',
            'context': {
                'default_article_id': self.id,
            },
        }
