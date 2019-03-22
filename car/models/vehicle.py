# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import tools, _
from odoo.modules.module import get_module_resource
import odoo.addons.decimal_precision as dp


class Vehicle(models.Model):

    _name = 'car.vehicle'
    _description = 'Vehicles'
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
    license_plate = fields.Char(size=200)
    image = fields.Binary("Photo", attachment=True)
    image_small = fields.Binary(string="Image Small", attachment=True, default=lambda self: self._default_image_small)
    vin_sn = fields.Char(string='Vin SN', size=200, required=True)
    model_id = fields.Many2one(comodel_name='car.model', string='Model')
    acquisition_date = fields.Date()
    arrival_date = fields.Date(string="Arrival Date")
    color = fields.Char(string='Color', size=10)
    cost = fields.Float(string='Cost', digits=dp.get_precision('Account'))
    odometer_start = fields.Integer(string='Start Odometer')
    model_year = fields.Char(string='Year', size=4, related='model_id.model_year', store=True)
    seats = fields.Integer(string='Seats', related='model_id.seats', store=True)
    doors = fields.Integer(string='Doors', related='model_id.doors', store=True)
    horsepower = fields.Integer(string='Horse Power', related='model_id.horsepower', store=True)
    co2 = fields.Float(string='CO2', related='model_id.co2', store=True)
    odometer = fields.Selection([
        ('kilometers', 'Kilometers'),
        ('miles', 'Miles')
    ], string='Odometer', related='model_id.odometer', store=True)
    transmission = fields.Selection([
        ('manual', 'Manual'),
        ('automatic', 'Automatic')
    ], string='Transmission', related='model_id.transmission', store=True)
    fuel = fields.Selection([
        ('gasoline', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid')
    ], string='Fuel Type', related='model_id.fuel', store=True)
    state = fields.Selection([
        ('created', 'Created'),
        ('validate', 'Validate'),
        ('assigned', 'Assigned'),
        ('contracted', 'Contracted')
    ], default='created', string='State')
    note = fields.Text()
    buy_place = fields.Char(string='Buy Place', size=200)
    company_id = fields.Many2one(comodel_name='res.company', string='Company', default=lambda self: self.env.user.company_id.id)
    assigned_id = fields.Many2one(comodel_name='res.users', string='Users')
    is_create = fields.Boolean(string='Is Created?', default=False)

    @api.multi
    def set_validate(self):
        self.state = 'validate'

    @api.multi
    def set_assigned(self):
        action = self.env.ref('car.assign_user_action').read()[0]
        return action

    @api.multi
    def set_contracted(self):
        self.state = 'contracted'

    @api.model
    def create(self, vals_list):
        vals_list['name'] = self.env['ir.sequence'].get('car.vehicle') or '/'
        res = super(Vehicle, self).create(vals_list)
        res.is_create = True
        return res


class Model(models.Model):

    _inherit = 'car.model'

    vehicle_ids = fields.One2many(comodel_name='car.vehicle', inverse_name='model_id', string='Vehicles')
