from datetime import datetime

from odoo.tests import tagged
from odoo.tests.common import Form
from odoo.addons.dk_personal_budget.tests.common import TestCommon


@tagged('post_install', '-at_install', 'library')
class TestForm(TestCommon):
    def test_accounting_default_get(self):
        new_accounting = self.env['budget.accounting'].with_user(
            self.budget_admin).create({
                'date': datetime.now(),
                'type': 'expense',
                'amount': 100.00,
                'partner_id': self.partner_demo.id,
                'storage_id': self.admin_storage_demo.id,
                'currency_id': self.admin_storage_demo.currency_id.id,
                'article_id': self.article_demo.id,
            })

        self.budget_admin.with_user(
            self.budget_admin).write({'storage_id': self.admin_storage_demo})

        # Create Form:
        fact_form = Form(new_accounting)

        # Checking the default value for the 'type' field has been added:
        self.assertEqual(fact_form.type, 'expense')
        # Checking the default value for the 'storage_id' field has been added:
        self.assertEqual(fact_form.storage_id, self.budget_admin.storage_id)
        # Checking the default value for 'currency_id' field has been added:
        if self.budget_admin.storage_id:
            self.assertEqual(fact_form.currency_id,
                             self.budget_admin.storage_id.currency_id)

    def test_plan_set_date(self):
        # Create Form:
        self.plan_operation._set_date()
        plan_form = Form(self.plan_operation)
        start_day = datetime.today().date().replace(day=1)
        # Checking the date:
        self.assertEqual(plan_form.date, start_day.strftime('%Y-%m-%d'))
