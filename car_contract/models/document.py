# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Document(models.Model):

    _name = 'car.document'
    _description = 'Template of contract document'

    name = fields.Char(size=200, string='Name')
    active = fields.Boolean(string='Active', default=False)
    content = fields.Html(string='Document')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', default=lambda self: self.env.user.company_id.id)
