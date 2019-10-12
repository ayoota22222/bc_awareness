# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api


class BcAwarenessMedia(models.Model):
    _name = 'bc.awareness.media'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    type = fields.Char(string='Type')
    attachment = fields.Binary(string='Attachment', required=True)


class BcAwarenessSelf(models.Model):
    _name = 'bc.awareness.self.check.plan'

    user_id = fields.Many2one('res.users', string='User', copy=False)
    date = fields.Date(string='Date')
    time = fields.Float(string="Time")



