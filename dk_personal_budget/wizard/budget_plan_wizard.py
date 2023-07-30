from odoo import models, fields


class BudgetPlanWizard(models.TransientModel):
    _name = 'budget.plan.wizard'
    _description = 'Wizard for creating budget plans'

    date = fields.Date(
        required=True,
        default=fields.Date.today(),
        string='Plan Date (month)',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency'
    )
    planned_amounts = fields.One2many(
        comodel_name='budget.plan.wizard.line',
        inverse_name='wizard_id',
    )

    def create_budget_plans(self):
        budget_plan = self.env['budget.plan']
        for wizard in self:
            for article in wizard.planned_amounts:
                cur_date = budget_plan.get_begin_of_month(wizard.date)
                budget_plan.create({
                    'name': f'{article.article_id.name} ({cur_date})',
                    'date': cur_date,
                    'amount': article.amount,
                    'currency_id': wizard.currency_id.id,
                    'article_id': article.article_id.id,
                })


class BudgetPlanWizardLine(models.TransientModel):
    _name = 'budget.plan.wizard.line'
    _description = 'Wizard Line for planned amounts'

    name = fields.Char()
    wizard_id = fields.Many2one(
        comodel_name='budget.plan.wizard',
        default=lambda self: self.env['budget.plan.wizard'].browse(
            self._context.get('active_id', False)),
    )
    article_id = fields.Many2one(
        comodel_name='budget.article',
    )
    amount = fields.Float(
        string='Planned Amount',
    )
