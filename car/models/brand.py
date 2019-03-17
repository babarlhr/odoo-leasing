# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Brand(models.Model):
    _name = 'car.brand'
    _description = 'Vehicle\'s brand'

    # _inherit = 'mail.thread'

    name = fields.Char(string='Name', size=200, required=True)
    image = fields.Binary("Photo", attachment=True)
    company_id = fields.Many2one(comodel_name='res.company', string='Company', default=lambda self: self.env.user.company_id.id)
