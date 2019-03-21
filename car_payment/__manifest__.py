# -*- coding: utf-8 -*-
{
    'name': 'Car Contract Payment',
    'version': '0.1',
    'summary': 'To Manage payment contracts of vehicle',
    'sequence': 30,
    'description': """
car
====================
The specific and easy-to-use car system in Odoo allows you to keep track of your vehicle.
    """,
    'category': 'car',
    'website': '',
    'author': "Cedric FOWOUE",
    'images': ['images/accounts.jpeg'],
    'depends': ['car_contract'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/payment_view.xml',
        'views/payment_depreciation_view.xml',
        'views/depreciation_view.xml',
        'views/contract_view.xml',
        'views/menu.xml',
    ],
    'demo': [
        # 'demo/account_demo.xml',
    ],
    'qweb': [
        # "static/src/xml/account_reconciliation.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
