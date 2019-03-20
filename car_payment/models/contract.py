# -*- coding -*-
from odoo import models, fields, api


class Contract(models.Model):
    _inherit = 'car.contract'

    payment_ids = fields.One2many(comodel_name='car.payment', inverse_name='contract_id', string='Payments')
    payment_amount = fields.Float(compute='_get_total_payment', string='Total Payment')

    @api.multi
    @api.depends('payment_ids')
    def _get_total_payment(self):
        for c in self:
            amount = 0.0
            # for p in c.payment_ids:
            #     amount += p.collect_amount
            # c.payment_count = amount
            for d in c.depreciation_ids:
                amount += d.collect_amount
            c.payment_amount = amount
