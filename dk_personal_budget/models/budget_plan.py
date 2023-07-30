from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _

from odoo.exceptions import ValidationError


class BudgetPlan(models.Model):
    """
    Model representing monthly budget plans.

    This model is used to store and manage information about budget plans,
    which represent monthly financial plans or targets. Each entry in this
    model corresponds to a specific budget plan for a particular month,
    specifying the budgeted amount for expenses.
    """
    _name = 'budget.plan'
    _description = 'accounting monthly plan cost'

    name = fields.Char(
        compute='_compute_name',
    )
    date = fields.Date(
        required=True,
        default=fields.datetime.today(),
        copy=False,
    )
    amount = fields.Float()
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        required=True,
    )
    article_id = fields.Many2one(
        comodel_name='budget.article'
    )
    fact_amount = fields.Float(
        compute='_compute_fact_amount',
    )
    balance_amount = fields.Float(
        compute='_compute_balance_amount',
    )
    accounting_ids = fields.One2many(
        comodel_name='budget.accounting',
        inverse_name='budget_plan_id',
    )

    def write(self, vals):
        """
        Date must be the 1st day of the month, planing is monthly
        """
        if 'date' in vals:
            vals['date'] = self.get_begin_of_month(vals['date'])
        return super(BudgetPlan, self).write(vals)

    @api.onchange('date')
    def _set_date(self):
        """
        I need that only at form
        """
        for item in self:
            if item.date:
                item.date = self.get_begin_of_month(item.date)

    @staticmethod
    def get_begin_of_month(cur_date: date) -> date:
        if isinstance(cur_date, str):
            cur_date = datetime.strptime(cur_date, '%Y-%m-%d')
        return cur_date.replace(day=1)

    @api.constrains('date', 'currency_id', 'article_id')
    def check_existing_plan(self):
        """
        Checking a record with the same currency_id and article_id and date
        """
        for item in self:
            existing_plan = self.search([
                ('date', '=', item.date),
                ('currency_id', '=', item.currency_id.id),
                ('article_id', '=', item.article_id.id),
                ('id', '!=', item.id),
            ], limit=1)

            if existing_plan:
                raise ValidationError(
                    _(f"A budget plan with the same currency "
                      f"({item.currency_id.name}) "
                      f"and article ({item.article_id.name}) already exists "
                      f"for this period ({item.date})."))

    @api.model
    def _get_fact_amount(self, article_id, currency_id, start_date, end_date):
        """
        Calculating fact amount
        """
        accounting_model = self.env['budget.accounting']
        domain = [
            ('article_id', '=', article_id),
            ('currency_id', '=', currency_id),
            ('date', '>=', start_date),
            ('date', '<=', end_date),
        ]
        fact_amount = accounting_model.search(domain).mapped('amount')
        return sum(fact_amount)

    def _compute_fact_amount(self):
        """
        Set fact amount
        """
        for plan in self:
            start_date = plan.date.replace(day=1)
            end_date = start_date + relativedelta(months=1, days=-1)
            plan.fact_amount = self._get_fact_amount(
                plan.article_id.id,
                plan.currency_id.id,
                start_date,
                end_date
            )

    def _compute_balance_amount(self):
        """
        Set difference between amount and amount fact
        """
        for plan in self:
            plan.balance_amount = plan.amount - plan.fact_amount

    @api.depends('article_id', 'date')
    def _compute_name(self):
        for plan in self:
            article_name = plan.article_id.name
            date = plan.date.strftime('%Y-%m')
            plan.name = f'{article_name} ({date})'
