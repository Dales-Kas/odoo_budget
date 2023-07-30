from odoo import models, fields, api, _


class BudgetAccounting(models.Model):
    """
    Model representing budget accounting for tracking expenses and incomes.

    This model is used to store and manage information about budget accounting,
    which represents the tracking of expenses and incomes in the budget.
    Each entry in this model corresponds to a specific transaction involving
    an amount, a date, a type (expense or income), a partner, a currency,
    an article, and a storage location.
    """
    _name = 'budget.accounting'
    _description = 'accounting article for tracking expenses and incomes'

    name = fields.Char(
        copy=False,
        index=True,
        compute='_compute_name',
    )
    date = fields.Date(
        copy=False,
        default=fields.datetime.today(),
        required=True,
    )
    type = fields.Selection(
        selection=[
            ('income', _('Income')),
            ('expense', _('Expense')),
        ],
        required=True,
        default='expense',
    )
    amount = fields.Monetary(
        currency_field='currency_id',
        required=True,
    )
    amount_in = fields.Monetary(
        currency_field='currency_id',
        compute='_compute_in_out_amount',
        store=True,
    )
    amount_out = fields.Monetary(
        currency_field='currency_id',
        compute='_compute_in_out_amount',
        store=True,
    )
    amount_total = fields.Monetary(
        currency_field='currency_id',
        compute='_compute_total_amount',
        store=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        required=True,
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        required=True,
    )
    article_id = fields.Many2one(
        comodel_name='budget.article'
    )
    storage_id = fields.Many2one(
        comodel_name='budget.storage',
        required=True,
    )
    description = fields.Text(
        translate=True,
    )
    budget_plan_id = fields.Many2one(
        comodel_name='budget.plan',
        string='Budget Plan',
    )

    @api.model
    def default_get(self, default_fields):
        """
        Add default
        - 'storage_id' from current user
        - 'currency_id' from storage_id
        """
        res = super(BudgetAccounting, self).default_get(
            default_fields)
        current_user = self.env.user
        res['storage_id'] = current_user.storage_id.id
        if current_user.storage_id:
            res['currency_id'] = current_user.storage_id.currency_id.id
        return res

    @api.depends('amount')
    def _compute_in_out_amount(self):
        """
        Calculating 'in' and 'out' values
        We need that for sum all
        income & expense values
        (we can use that in reports, etc.)
        """
        for item in self:
            if item.type == 'income':
                item.amount_in = item.amount
                item.amount_out = 0
            else:
                item.amount_in = 0
                item.amount_out = -item.amount

    @api.depends('amount')
    def _compute_total_amount(self):
        """
        Calculating total amount
        We need that for get:
        income - expense value
        (we can use that in reports, etc.)
        """
        for item in self:
            item.amount_total = item.amount if item.type == 'income' else - \
                item.amount

    @api.onchange('partner_id')
    def _on_partner_change(self):
        """
        Set default article from partner, if article is empty
        """
        for item in self:
            if item.partner_id and not item.article_id:
                item.article_id = item.partner_id.article_id

    @api.depends('partner_id', 'date')
    def _compute_name(self):
        for rec in self:
            rec.name = f"№{rec.id}/{rec.date} ({rec.partner_id.name})"
