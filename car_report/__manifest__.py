# -*- coding: utf-8 -*-
{
    'name': 'Car Report',
    'version': '0.1',
    'summary': 'Show car reports',
    'sequence': 30,
    'description': """
car
====================
The specific and easy-to-use car system in Odoo allows you to keep track of your vehicle.
    """,
    'category': 'car',
    'website': '',
    'images': ['images/accounts.jpeg'],
    'depends': ['car_contract', 'car_payment'],
    'data': [
        # 'security/account_security.xml',
        # 'security/ir.model.access.csv',
        # 'data/brand.xml',
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
