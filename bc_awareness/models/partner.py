# -*- coding: utf-8 -*-

from odoo import models,fields,api

class Partner(models.Model):
    _inherit = 'res.partner'

    bc_partner = fields.Boolean(string="BC Partner",default=True)
    is_mobile_verified = fields.Boolean(string="Mobile Verified")
    weight = fields.Float(string="Weight")
    height = fields.Float(string="Height")
    birth_date = fields.Date(string="Birth Date")
    password = fields.Char(string="Password")
