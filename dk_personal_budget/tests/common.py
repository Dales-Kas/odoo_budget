from datetime import datetime

from odoo.tests.common import TransactionCase


class TestCommon(TransactionCase):

    def setUp(self):
        super(TestCommon, self).setUp()
        self.group_budget_user = self.env.ref(
            'dk_personal_budget.group_budget_user')
        self.group_budget_admin = self.env.ref(
            'dk_personal_budget.group_budget_admin')
        self.budget_user = self.env['res.users'].create({
            'name': 'Budget User',
            'login': 'Budget_user',
            'groups_id': [(4, self.env.ref('base.group_user').id),
                          (4, self.group_budget_user.id)],
        })
        self.budget_admin = self.env['res.users'].create({
            'name': 'Budget Admin',
            'login': 'Budget_admin',
            'groups_id': [(4, self.env.ref('base.group_user').id),
                          (4, self.group_budget_admin.id)],
        })
        self.partner_demo = self.env['res.partner'].create(
            {'name': 'Demo partner'})
        self.article_demo = self.env['budget.article'].create({
            'name': 'Demo Article'})
        self.user_storage_demo = self.env['budget.storage'].create({
            'name': 'user storage',
            'user_id': self.budget_user.id
        })
        self.admin_storage_demo = self.env['budget.storage'].create({
            'name': 'admin storage',
            'user_id': self.budget_admin.id,
            'currency_id': self.env.ref('base.USD').id,
        })

        self.plan_operation = self.env['budget.plan'].create({
            'date': datetime.now(),
            'amount': 1000.0,
            'currency_id': self.env.ref('base.USD').id,
            'article_id': self.article_demo.id,
        })
