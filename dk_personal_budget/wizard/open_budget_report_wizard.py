from odoo import fields, models, _


class OpenBudgetReportWizard(models.TransientModel):
    _name = 'open.budget.report.wizard'
    _description = 'Open budget report'

    start_date = fields.Date(
        required=True,
        default=lambda self: fields.Date.today().replace(day=1),
    )
    end_date = fields.Date(
        required=True,
        default=lambda self: fields.Date.today(),
    )

    def generate_report(self):
        return {
            'name': _('Budget Report'),
            'type': 'ir.actions.report',
            'report_type': 'qweb-pdf',
            'report_name': 'dk_personal_budget.budget_report',
        }
