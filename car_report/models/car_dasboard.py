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
        return [{'vehicle': v, 'partner': p, 'payment': pay, 'contract': c}]

    @api.model
    def get_vehicles_info(self):
        vehicles = self.env['car.vehicle'].search(['|',
            ('company_id', '=', self.env.user.company_id.id),
            ('company_id', 'in', self.env.user.company_id.child_ids.ids)
        ])
        return len(vehicles)

    @api.model
    def get_partners_info(self):
        partners = self.env['res.partner'].search(['|',
            ('company_id', '=', self.env.user.company_id.id),
            ('company_id', 'in', self.env.user.company_id.child_ids.ids)
        ])
        return len(partners)

    @api.model
    def get_payments_info(self):
        payments = self.env['car.payment'].search(['|',
            ('company_id', '=', self.env.user.company_id.id),
            ('company_id', 'in', self.env.user.company_id.child_ids.ids)
        ])
        return len(payments)

    @api.model
    def get_contracts_info(self):
        contracts = self.env['car.contract'].search(['|',
            ('company_id', '=', self.env.user.company_id.id),
            ('company_id', 'in', self.env.user.company_id.child_ids.ids)
        ])
        return len(contracts)

    @api.model
    def get_contracts_total_amount(self):
        contracts = self.env['car.contract'].search(['|',
            ('company_id', '=', self.env.user.company_id.id),
            ('company_id', 'in', self.env.user.company_id.child_ids.ids)
        ])
        return len(contracts)
