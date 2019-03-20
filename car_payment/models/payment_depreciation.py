# -*- coding -*-
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class PaymentDepreciation(models.Model):

    _name = 'car.payment.depreciation'
    _description = 'payment and depreciation evaluation'

    contract_id = fields.Many2one(comodel_name='car.contract', string='Contract', related='payment_id.contract_id')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', related='payment_id.company_id')
    depreciation_id = fields.Many2one(comodel_name='car.depreciation', string='Depreciation')
    payment_id = fields.Many2one(comodel_name='car.payment', string='Payment')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', related='payment_id.currency_id')
    collect_amount = fields.Float(string='Collect Amount', digits=dp.get_precision('Account'))
    collect_at = fields.Date(string='Collect At', related='payment_id.collect_at')


class Payment(models.Model):
    _inherit = 'car.payment'

    payment_depreciation_ids = fields.One2many(comodel_name='car.payment.depreciation', inverse_name='payment_id', string='Payment and depreciation')

    @api.model
    def create(self, vals_list):
        res = super(Payment, self).create(vals_list)
        depreciations = self.env['car.depreciation'].search([
            ('contract_id', '=', res.contract_id.id),
            ('state', '!=', 'paid')], order='waiting_at')
        cumul = 0.0
        data_list = list()
        for dep in depreciations:
            cumul += dep.remain_amount
            if cumul <= res.collect_amount:
                pdep = (0, 0, {'depreciation_id': dep.id, 'collect_amount': dep.remain_amount, 'payment_id': res.id})
                dep.state = 'paid'
                data_list.append(pdep)
            elif cumul > res.collect_amount:
                gap = cumul - res.collect_amount
                amount = dep.remain_amount - gap
                pdep = (0, 0, {'depreciation_id': dep.id, 'collect_amount': amount, 'payment_id': res.id})
                data_list.append(pdep)
                break
        res.write({'payment_depreciation_ids': data_list})
        return res


class Depreciation(models.Model):

    _inherit = 'car.depreciation'

    collect_at = fields.Date(compute='_get_collect_at', string='Collect At')
    collect_amount = fields.Float(compute='_get_collect_amount', string='Collect Amount', digits=dp.get_precision('Account'))
    remain_amount = fields.Float(compute='_get_remain_amount', string='Remain Amount', digits=dp.get_precision('Account'))

    @api.multi
    def _get_collect_at(self):
        pay_env = self.env['car.payment.depreciation']
        for r in self:
            item = pay_env.search([('depreciation_id', '=', r.id)], order='collect_at desc')
            if item:
                r.collect_at = item.collect_at

    @api.depends('waiting_amount')
    def _get_collect_amount(self):
        pay_env = self.env['car.payment.depreciation']
        for r in self:
            already_paid = pay_env.search([('depreciation_id', '=', r.id)])
            amount = 0.0
            for payment in already_paid:
                amount += payment.collect_amount
            r.collect_amount = amount

    @api.depends('waiting_amount', 'collect_amount')
    def _get_remain_amount(self):
        for r in self:
            if r.waiting_amount:
                r.remain_amount = r.waiting_amount - r.collect_amount
            else:
                r.remain_amount = 0.0

