# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AssignUser(models.TransientModel):

    _name = 'car.vehicle.assign'
    _description = 'Assign vehicle to user'

    def _get_default_vehicle(self):
        return self.env['car.vehicle'].browse(self.env.context.get('active_id'))

    user_id = fields.Many2one(comodel_name='res.users', string='User', required=True)
    vehicle_id = fields.Many2one(comodel_name='car.vehicle', string='Vehicle', required=True, default=_get_default_vehicle)

    def validate(self):
        self.vehicle_id.assigned_id = self.user_id

