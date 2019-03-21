# -*- coding -*-
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class Contract(models.Model):
    _inherit = 'car.contract'

    payment_ids = fields.One2many(comodel_name='car.payment', inverse_name='contract_id', string='Payments')
    payment_count = fields.Integer(compute='_get_payment_count', string='Payment')
    payment_amount = fields.Float(compute='_get_total_payment', string='Total Payment', digits=dp.get_precision('Account'))
    remain_amount = fields.Float(compute='_get_total_payment', string='Total Remain', digits=dp.get_precision('Account'))
    late_amount = fields.Float(compute='_get_total_payment', string='Total Late', digits=dp.get_precision('Account'))

    @api.multi
    @api.depends('depreciation_ids')
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

    @api.multi
    @api.depends('payment_ids')
    def _get_payment_count(self):
        for c in self:
            c.payment_count = len(c.payment_ids)

    @api.multi
    def show_payment(self):
        self.ensure_one()
        return {
            'name': 'Payments',
            'res_model': 'car.payment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
            'context': "{ 'search_default_contract_id': [%s], 'default_contract_id': '%s'}"  % (self.id, self.id)
        }
