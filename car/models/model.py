# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import tools, _
from odoo.modules.module import get_module_resource
import odoo.addons.decimal_precision as dp


class ModelVehicle(models.Model):

    _name = 'car.model'
    _description = 'Vehicle\'s model'

    # _inherit = 'mail.thread'

    @api.model
    def _default_image(self):
        image_path = get_module_resource('car', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    @api.model
    def _default_image_small(self):
        if not self.image:
            return False
        return tools.image_resize_image_small(self.image)

    name = fields.Char(string='Name', size=200, required=True)
    image = fields.Binary(string="Photo")
    image_small = fields.Binary(string="Image Small", attachment=True, default=lambda self: self._default_image_small)
    company_id = fields.Many2one(comodel_name='res.company', string='Company', default=lambda self: self.env.user.company_id.id)
    brand_id = fields.Many2one(comodel_name='car.brand', string='Brand')
    model_year = fields.Char(string='Year', size=4)
    seats = fields.Integer(string='Seats')
    doors = fields.Integer(string='Doors')
    horsepower = fields.Integer(string='Horse Power')
    co2 = fields.Float(string='CO2', digits=dp.get_precision('Account'))
    odometer = fields.Selection([
        ('kilometers', 'Kilometers'),
        ('miles', 'Miles')
    ], string='Odometer')
    transmission = fields.Selection([
        ('manual', 'Manual'),
        ('automatic', 'Automatic')
    ], string='Transmission')
    fuel = fields.Selection([
        ('gasoline', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid')
    ], string='Fuel Type')


class Brand(models.Model):

    _inherit = 'car.brand'

    model_ids = fields.One2many(comodel_name='car.model', inverse_name='brand_id', string='Models')
