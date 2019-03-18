# -*- coding: utf-8 -*-
{
    'name': 'Car Management',
    'version': '0.1',
    'summary': 'To Manage vehicles',
    'sequence': 30,
    'author': 'Cedric FOWOUE',
    'description': """
car
====================
The specific and easy-to-use car system in Odoo allows you to keep track of your vehicle.
    """,
    'category': 'car',
    'website': '',
    'images': ['images/accounts.jpeg'],
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/brand_view.xml',
        'views/model_view.xml',
        'views/vehicle_view.xml',
        'views/menu.xml',
        'views/assign_user_view.xml',
    ],
    'demo': [
        # 'demo/account_demo.xml',
    ],
    'qweb': [
        # "static/src/xml/account_reconciliation.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
