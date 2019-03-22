# -*- coding -*-
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class Payment(models.Model):

    _name = 'car.payment'
    _description = 'Contract\'s payment'
    # _inherit = 'mail.thread'
    
    contract_id = fields.Many2one(comodel_name='car.contract', string='Contract')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', related='contract_id.company_id', store=True)
    collect_amount = fields.Float(string='Collect Amount', digits=dp.get_precision('Account'))
    collect_at = fields.Date()
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', related='contract_id.currency_id')
    name = fields.Char(string='Reference', size=200)
    image = fields.Binary("Photo", attachment=True, related='contract_id.image', readonly=True)

    @api.model
    def create(self, values):
        res = super(Payment, self).create(values)
        if not res.contract_id.remain_amount:
            res.contract_id.state = 'close'
        return res

