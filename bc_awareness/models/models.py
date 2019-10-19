# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api


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



