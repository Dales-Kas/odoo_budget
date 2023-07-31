from datetime import datetime

from odoo.addons.dk_personal_budget.tests.common import TestCommon
from odoo.tests import tagged
from odoo.exceptions import UserError


@tagged('post_install', '-at_install', 'library')
class TestAccessRights(TestCommon):
    def tests_action_create_operation(self):
        # A user can create accounting operation from article:
        self.article_demo.with_user(self.budget_user)\
            .action_create_operation()

    def tests_compute_fact_amount(self):
        # A user can't create plan operation:
        with self.assertRaises(UserError):
            self.plan_operation.with_user(self.budget_user)\
                ._compute_fact_amount()

    def tests_get_begin_of_month(self):
        # Create a new budget plan
        plan_data = {
            'date': datetime.today(),
            'amount': 1000.0,
            'currency_id': self.env.ref('base.UAH').id,
            'article_id': self.article_demo.id,
        }
        budget_plan = self.env['budget.plan'].with_user(self.budget_admin) \
            .create(plan_data)

        budget_plan.write({'date': datetime.today()})

        start_day = datetime.today().date().replace(day=1)

        # Check if the budget plan is created correctly, check date:
        self.assertEqual(budget_plan.date, start_day)
