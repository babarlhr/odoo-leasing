# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request
import datetime


class CarDashboard(models.Model):
    _name = 'car.dashboard'
    _description = 'Car Dashboard'

    name = fields.Char("")

    @api.model
    def get_data_info(self):
        """
        The function which is called from car_report.js.

        :rtype dict
        :return: data
        """
        return []
