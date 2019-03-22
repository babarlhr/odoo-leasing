# -*- coding -*-
from odoo import models, fields, api
from datetime import timedelta
import odoo.addons.decimal_precision as dp
from weasyprint import HTML
import base64


class Contract(models.Model):
    _name = 'car.contract'
    _inherit = 'mail.thread'

    name = fields.Char(size=200)
    file_validate_name = fields.Char(size=200, compute='_get_filane_name')
    file_name = fields.Char(size=200, compute='_get_filane_name')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')
    contract_file_validate = fields.Binary(string='Signed Contract')
    contract_file = fields.Binary(string='Genrate Contract')
    contract_date = fields.Date(default=fields.Date.today(), string='Signed Date')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    number_depreciation = fields.Integer()
    amount_depreciation = fields.Float(string='Amount to depreciate', digits=dp.get_precision('Account'))
    daily_depreciation = fields.Float(string='Daily Depreciation', digits=dp.get_precision('Account'))
    weekly_depreciation = fields.Float(string='Weekly Depreciation', digits=dp.get_precision('Account'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'In Progress'),
        ('close', 'Close'),
        ('cancel', 'Cancel')
    ], default='draft', string='State')
    company_id = fields.Many2one(comodel_name='res.company', string='Company',
                                 default=lambda self: self.env.user.company_id.id)
    vehicle_id = fields.Many2one(comodel_name='car.vehicle', string='Vehicle')
    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer')
    image = fields.Binary("Photo", attachment=True, related='vehicle_id.image', readonly=True)
    content = fields.Html(string='Contract Document')

    @api.multi
    @api.depends('name')
    def _get_filane_name(self):
        for c in self:
            c.file_validate_name = c.name + ' Signed Contract.pdf'
            c.file_name = c.name + ' Generate Contract.pdf'

    @api.model
    def create(self, vals_list):
        vals_list['name'] = self.env['ir.sequence'].get('car.contract') or '/'
        res = super(Contract, self).create(vals_list)
        res.vehicle_id.state = 'contracted'
        return res

    @api.multi
    def get_contract_content(self):
        self.ensure_one()
        doc = self.env['car.document'].search([('active', '=', True), ('company_id', '=', self.company_id.id)])
        content = doc.content
        content = content.replace('contract_name', self.name)
        content = content.replace('contract_start_date', str(self.start_date))
        content = content.replace('contract_end_date', str(self.end_date))
        content = content.replace('contract_customer', self.customer_id.name)
        content = content.replace('contract_vehicle_name', self.vehicle_id.name)
        content = content.replace('contract_vehicle_vinsn', self.vehicle_id.vin_sn)
        self.content = content
        html = HTML(string=content)
        self.contract_file = base64.encodebytes(html.write_pdf())


