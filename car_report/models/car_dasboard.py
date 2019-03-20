# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request
import datetime


class CarDashboard(models.Model):
    _name = 'car.dashboard'
    _description = 'Car Dashboard'

    name = fields.Char("")

    @api.model
    def get_data_info(self):
        """
        The function which is called from car_report.js.

        :rtype dict
        :return: data
        """
        v = self.get_vehicles_info()
        p = self.get_partners_info()
        pay = self.get_payments_info()
        c = self.get_contracts_info()
        a = self.get_contracts_amount()
        currency = self.env.user.company_id.currency_id.name
        a.update({'vehicle': v, 'partner': p, 'payment': pay, 'contract': c, 'currency': currency})
        return [a]

    def get_vehicles_info(self):
        vehicles = self.env['car.vehicle'].search(['|',
            ('company_id', '=', self.env.user.company_id.id),
            ('company_id', 'in', self.env.user.company_id.child_ids.ids)
        ])
        return len(vehicles)

    def get_partners_info(self):
        partners = self.env['res.partner'].search(['|',
            ('company_id', '=', self.env.user.company_id.id),
            ('company_id', 'in', self.env.user.company_id.child_ids.ids)
        ])
        return len(partners)

    def get_payments_info(self):
        payments = self.env['car.payment'].search(['|',
            ('company_id', '=', self.env.user.company_id.id),
            ('company_id', 'in', self.env.user.company_id.child_ids.ids)
        ])
        return len(payments)

    def get_contracts_info(self):
        contracts = self.env['car.contract'].search(['|',
            ('company_id', '=', self.env.user.company_id.id),
            ('company_id', 'in', self.env.user.company_id.child_ids.ids)
        ])
        return len(contracts)

    def get_contracts_amount(self):
        contracts = self.env['car.contract'].search(['|',
            ('company_id', '=', self.env.user.company_id.id),
            ('company_id', 'in', self.env.user.company_id.child_ids.ids)
        ])
        company_currency = self.env.user.company_id.currency_id
        remain = 0.0
        collect = 0.0
        amount = 0.0
        late = 0.0
        for c in contracts:
            currency = c.currency_id
            remain += currency.compute(c.remain_amount, company_currency)
            collect += currency.compute(c.payment_amount, company_currency)
            amount += currency.compute(c.amount_depreciation, company_currency)
            late += currency.compute(c.late_amount, company_currency)
        return {'remain': remain, 'collect': collect, 'amount': amount, 'late': late}
