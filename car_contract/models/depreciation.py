# -*- coding -*-
from odoo import models, fields, api
from datetime import timedelta, datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class Depreciation(models.Model):

    _name = 'car.depreciation'
    _description = 'contract\'s depreciation'
    # _inherit = 'mail.thread'

    contract_id = fields.Many2one(comodel_name='car.contract', string='Contract')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', related='contract_id.company_id', store=True)
    waiting_at = fields.Date()
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', related='contract_id.currency_id')
    waiting_amount = fields.Float(string='Waiting Amount', related='contract_id.weekly_depreciation')
    flag = fields.Boolean()
    state = fields.Selection([
        ('waiting', 'Waiting'),
        ('paid', 'Paid')
    ], default='waiting', string='State')
    vehicle_id = fields.Many2one(comodel_name='car.vehicle', string='Vehicle', related='contract_id.vehicle_id')
    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer', related='contract_id.customer_id')


class Contract(models.Model):
    _inherit = 'car.contract'

    depreciation_ids = fields.One2many(comodel_name='car.depreciation', inverse_name='contract_id', string='Depreciations')

    @api.multi
    def generate_depreciation(self):
        self.ensure_one()
        start_date = self.start_date
        dep_env = self.env['car.depreciation']
        for i in range(1, self.number_depreciation + 1):
            waiting_date = start_date + timedelta(weeks=i)
            data = {
                'contract_id': self.id,
                'state': 'waiting',
                'waiting_at': waiting_date
            }
            dep_env.create(data)
        self.write({'state': 'pending'})

    @api.onchange('number_depreciation', 'amount_depreciation', 'start_date', 'weekly_depreciation')
    def compute_depreciation(self):
        if self.number_depreciation and self.amount_depreciation:
            if self.number_depreciation == 0:
                ValueError('set number of depreciation')
            else:
                self.weekly_depreciation = self.amount_depreciation / self.number_depreciation
                self.daily_depreciation = self.weekly_depreciation / 6
                self.compute_last_date()
        else:
            if self.weekly_depreciation and self.amount_depreciation:
                if self.weekly_depreciation == 0:
                    ValueError('set weekly of depreciation')
                else:
                    self.number_depreciation = self.amount_depreciation / self.weekly_depreciation
                    self.daily_depreciation = self.weekly_depreciation / 6
                    self.compute_last_date()

    def compute_last_date(self):
        if self.start_date and self.number_depreciation:
            if self.number_depreciation == 0 or not self.number_depreciation:
                ValueError('set number of depreciation')
            else:
                self.end_date = self.start_date + timedelta(weeks=self.number_depreciation)
        else:
            if not self.number_depreciation or self.number_depreciation == 0:
                ValueError('set number of depreciation')

    @api.multi
    def set_draft(self):
        for r in self:
            if r.depreciation_ids:
                for dep in r.depreciation_ids:
                    if dep.collect_amount > 0:
                        raise ValueError('cannot delete because some payment is related')
                r.write({'depreciation_ids': [(2, r.depreciation_ids.ids)]})
        self.state = 'draft'

    @api.multi
    def set_cancel(self):
        self.state = 'cancel'

    @api.multi
    def set_close(self):
        self.state = 'close'
