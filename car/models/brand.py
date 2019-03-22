# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import tools


class Brand(models.Model):
    _name = 'car.brand'
    _description = 'Vehicle\'s brand'

    # _inherit = 'mail.thread'

    @api.model
    def _default_image_small(self):
        if not self.image:
            return False
        return tools.image_resize_image_small(self.image)

    name = fields.Char(string='Name', size=200, required=True)
    image = fields.Binary(string="Photo", attachment=True)
    image_small = fields.Binary(string="Image Small", attachment=True, default=lambda self: self._default_image_small)
    company_id = fields.Many2one(comodel_name='res.company', string='Company', default=lambda self: self.env.user.company_id.id)
