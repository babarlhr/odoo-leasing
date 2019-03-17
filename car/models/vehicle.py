# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import tools, _
from odoo.modules.module import get_module_resource


class Vehicle(models.Model):

    _name = 'car.vehicle'
    _description = 'Vehicles'
    # _inherit = 'mail.thread'

    @api.model
    def _default_image(self):
        image_path = get_module_resource('car', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    name = fields.Char(string='Name', size=200, required=True)
    license_plate = fields.Char(size=200)
    image = fields.Binary("Photo", attachment=True)
    vin_sn = fields.Char(string='Vin SN', size=200, required=True)
    model_id = fields.Many2one(comodel_name='car.model', string='Model')
    acquisition_date = fields.Date()
    color = fields.Char(string='Color', size=10)
    cost = fields.Float(string='Cost')
    odometer_start = fields.Integer(string='Start Odometer')
    year = fields.Char(string='Year', size=4, required=True, related='model_id.year', store=True)
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


class Model(models.Model):

    _inherit = 'car.model'

    vehicle_ids = fields.One2many(comodel_name='car.vehicle', inverse_name='model_id', string='Vehicles')
