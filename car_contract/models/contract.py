# -*- coding -*-
from odoo import models, fields, api
from datetime import timedelta


class Contract(models.Model):
    _name = 'car.contract'
    _inherit = 'mail.thread'

    name = fields.Char(size=200)
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')
    contract_file = fields.Binary()
    contract_date = fields.Date()
    start_date = fields.Date()
    end_date = fields.Date()
    number_depreciation = fields.Integer()
    amount_depreciation = fields.Float()
    daily_depreciation = fields.Float()
    weekly_depreciation = fields.Float()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('close', 'Close'),
        ('cancel', 'Cancel')
    ], default='draft', string='State')
    company_id = fields.Many2one(comodel_name='res.company', string='Company',
                                 default=lambda self: self.env.user.company_id.id)
    vehicle_id = fields.Many2one(comodel_name='car.vehicle', string='Vehicle')
    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer')
    image = fields.Binary("Photo", attachment=True, related='vehicle_id.image', readonly=True)
    flag = fields.Boolean(string='Flag')

    @api.model
    def create(self, vals_list):
        vals_list['name'] = self.env['ir.sequence'].get('car.contract') or '/'
        return super(Contract, self).create(vals_list)
