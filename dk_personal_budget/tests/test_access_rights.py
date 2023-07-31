from datetime import datetime

from odoo.addons.dk_personal_budget.tests.common import TestCommon
from odoo.tests import tagged
from odoo.exceptions import AccessError


@tagged('post_install', '-at_install', 'library', 'access')
class TestAccessRights(TestCommon):

    def test_storage_budget_user_access_rights(self):
        # A budget user can't create a storage:
        with self.assertRaises(AccessError):
            self.env['budget.storage'].with_user(self.budget_user).create(
                {'name': 'Test storage',
                 'user_id': self.budget_user.id})
        # A budget user can't unlink a storage:
        with self.assertRaises(AccessError):
            self.admin_storage_demo.with_user(self.budget_user).unlink()
        # A budget user can't read a storage of others users
        with self.assertRaises(AccessError):
            self.admin_storage_demo.with_user(self.budget_user).read()

    def test_article_budget_user_access_rights(self):
        # A budget user can't create the article
        with self.assertRaises(AccessError):
            self.env['budget.article'].with_user(self.budget_user).create(
                {'name': 'Test article'})
        # A budget user can't unlink the article
        with self.assertRaises(AccessError):
            self.article_demo.with_user(self.budget_user).unlink()

    def test_storage_budget_admin_access_rights(self):
        storage = self.env['budget.storage'].with_user(
            self.budget_admin).create(
            {'name': 'Test storage'})
        storage.with_user(self.budget_admin).read()
        storage.with_user(self.budget_admin).write({'name': 'Test storage'})
        storage.with_user(self.budget_admin).unlink()

    def test_accounting_budget_user_access_rights(self):
        # A budget user can create the accounting operation:
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
        new_accounting.with_user(self.budget_admin).read()

    def test_create_budget_plan(self):
        # Create a new budget plan
        plan_data = {
            'date': datetime.today(),
            'amount': 1000.0,
            'currency_id': self.env.ref('base.EUR').id,
            'article_id': self.article_demo.id,
        }
        # A budget user can't create plan operation:
        with self.assertRaises(AccessError):
            self.env['budget.plan'].with_user(self.budget_user)\
                .create(plan_data)

        # But admin can:
        self.env['budget.plan'].with_user(self.budget_admin).create(plan_data)
