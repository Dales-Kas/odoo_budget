from odoo.addons.school_lesson_6_4.tests.common import TestCommon
from odoo.tests import tagged
from odoo.exceptions import AccessError


@tagged('post_install', '-at_install', 'library', 'access')
class TestAccessRights(TestCommon):

    def test_storage_budget_user_access_rights(self):
        # A budget user can't write a storage of others users
        with self.assertRaises(AccessError):
            self.env['budget.storage'].with_user(self.budget_user).write(
                {'name': 'Test Book'})
        # A budget user can't unlink a storage of others users
        with self.assertRaises(AccessError):
            self.admin_storage_demo.with_user(self.budget_user).unlink()
        # A budget user can't read a storage of others users
        with self.assertRaises(AccessError):
            self.admin_storage_demo.with_user(self.budget_user).read()

    def test_article_budget_user_access_rights(self):
        # A budget user can't write the article
        with self.assertRaises(AccessError):
            self.env['budget.article'].with_user(self.budget_user).write(
                {'name': 'Test article'})
        # A budget user can't unlink the article
        with self.assertRaises(AccessError):
            self.article_demo.with_user(self.budget_user).unlink()

    def test_storage_budget_admin_access_rights(self):
        storage = self.env['budget.storage'].with_user(
            self.budget_admin).create(
            {'name': 'Test storage'})
        storage.with_user(self.budget_admin).read()
        storage.with_user(self.budget_admin).write({'name': 'Test Book II'})
        storage.with_user(self.budget_admin).unlink()

    def test_accounting_budget_user_access_rights(self):
        with self.assertRaises(AccessError):
            self.env['budget.storage'].with_user(
                self.budget_user).create(
                {'name': 'Test storage'})
