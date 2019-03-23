# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Currency Exchange Rate',
    'version': '1.0',
    'category': 'Accounting',
    'author': 'Cedric FOWOUE',
    'description': """Import exchange rates from the Internet.
""",
    'depends': [
        'account',
    ],
    'data': [
        'security/security.xml',
        'views/company_view.xml',
        'views/config_setting_view.xml',
        'views/service_cron_data.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': '',
}
