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
    'author': "Cedric FOWOUE",
    'images': ['images/accounts.jpeg'],
    'depends': ['car_contract', 'car_payment'],
    'data': [
        'security/ir.model.access.csv',
        'views/car_report.xml',
    ],
    'qweb': [
        "static/src/xml/car_report.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
