# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Vehicle(models.Model):

    _inherit = 'car.vehicle'

    contract_ids = fields.One2many(comodel_name='car.contract', inverse_name='vehicle_id', string='Contracts')
    contract_count = fields.Float(compute='_get_contract_count', string='Contract')

    @api.multi
    @api.depends('contract_ids')
    def _get_contract_count(self):
        for c in self:
            c.contract_count = len(c.contract_ids)
