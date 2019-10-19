# -*- coding: utf-8 -*-

from odoo import models,fields,api


class BcAwarenessMedia(models.Model):
    _name = 'bc.awareness.media'
    _rec_name = 'title'

    title = fields.Char(string='Title', required=True)
    active = fields.Boolean(string='Active', default=True)
    type = fields.Char(string='Type')
    addons = fields.Binary(string='Addons', required=True)
    content = fields.Text(string="Content")



class BcAwarenessSelf(models.Model):
    _name = 'bc.awareness.self.check.plan'

    user_id = fields.Many2one('res.users', string='User', copy=False)
    date = fields.Date(string='Date')
    time = fields.Float(string="Time")

class Partner(models.Model):
    _inherit = 'res.partner'

    bc_partner = fields.Boolean(string="BC Partner",default=True)
    is_mobile_verified = fields.Boolean(string="Mobile Verified")
    weight = fields.Float(string="Weight")
    height = fields.Float(string="Height")
    birth_date = fields.Date(string="Birth Date")
    password = fields.Char(string="Password")
    url = fields.Char(string="url")

class BcMammogram(models.Model):
    _name = 'bc.mammogram'

    name = fields.Char(string="Name")
    address = fields.Char(string="Address")
    city = fields.Char(string="City")
    state = fields.Char(string="State")
    avatar = fields.Binary(string="Avatar")



