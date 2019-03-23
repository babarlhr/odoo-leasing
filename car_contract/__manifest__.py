# -*- coding: utf-8 -*-
{
    'name': 'Car Contract',
    'version': '0.1',
    'summary': 'To Manage contract vehicles',
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
    'depends': ['car'],
    'external_dependencies': {
        'python': ['weasyprint', 'pdfkit'],
    },
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/contract_view.xml',
        'views/depreciation_view.xml',
        'views/vehicle_view.xml',
        'views/document_view.xml',
        'views/menu.xml',
        'sequence/contract_sequence.xml',
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
