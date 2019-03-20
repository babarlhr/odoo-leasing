# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Vehicle(models.Model):

    _inherit = 'car.vehicle'

    contract_ids = fields.One2many(comodel_name='car.contract', inverse_name='vehicle_id', string='Contracts')
    contract_count = fields.Integer(compute='_get_contract_count', string='Contract')

    @api.multi
    @api.depends('contract_ids')
    def _get_contract_count(self):
        for c in self:
            c.contract_count = len(c.contract_ids)

    @api.multi
    def show_contract(self):
        self.ensure_one()
        return {
            'name': 'Contracts',
            'res_model': 'car.contract',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
            'context': "{ 'search_default_vehicle_id': [%s], 'default_vehicle_id': '%s'}"  % (self.id, self.id)
        }

