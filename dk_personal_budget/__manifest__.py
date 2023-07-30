{
    'name': "dk_personal_budget",
    'summary': "My personal budget",
    'author': 'Dales Kas',
    'website': "https://github.com/Dales-Kas",
    'category': 'Extra Tools',
    'version': '16.0.0.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/budget_groups.xml',
        'security/budget_security.xml',
        'security/ir.model.access.csv',
        'views/budget_menus.xml',
        'views/budget_accounting_views.xml',
        'views/budget_article_views.xml',
        'views/budget_plan_views.xml',
        'views/budget_storage_views.xml',
        'views/res_currency_views.xml',
        'views/res_partner_views.xml',
        'views/res_user_views.xml',
        'report/budget_report.xml',
        'wizard/open_budget_report_wizard_views.xml',
        'wizard/budget_plan_wizard_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/budget_article_demo.xml',
        'demo/res_partner_demo.xml',
        'demo/budget_storage_demo.xml',
        'demo/budget_accounting_demo.xml',
        'demo/budget_plan_demo.xml',
    ],
    'price': 10,
    'currency': 'EUR',
    'support': 'dales.p500@gmail.com',
    'images': [
        'static/description/banner.jpg',
        'static/description/icon.png',
    ],
    'application': False,
    'installable': True,
    'auto_install': False
}
