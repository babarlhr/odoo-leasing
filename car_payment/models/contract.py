# -*- coding -*-
from odoo import models, fields, api


class Contract(models.Model):
    _inherit = 'car.contract'

    payment_ids = fields.One2many(comodel_name='car.payment', inverse_name='contract_id', string='Payments')
    payment_amount = fields.Float(compute='_get_total_payment', string='Total Payment')
    remain_amount = fields.Float(compute='_get_total_payment', string='Total Remain')
    late_amount = fields.Float(compute='_get_total_payment', string='Total Late')

    @api.multi
    @api.depends('payment_ids')
    def _get_total_payment(self):
        moment = fields.date.today()
        for c in self:
            amount = 0.0
            waiting = 0.0
            collect = 0.0
            for d in c.depreciation_ids:
                amount += d.collect_amount
                if moment >= d.waiting_at:
                    waiting += d.waiting_amount
                    collect += d.collect_amount
            c.late_amount = collect - waiting
            c.payment_amount = amount
            c.remain_amount = c.amount_depreciation - amount

