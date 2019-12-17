# -*- coding: utf-8 -*-

from odoo import models,fields,api
import base64


class BcAwarenessMedia(models.Model):
    _name = 'bc.awareness.media'
    _rec_name = 'title'

    title = fields.Char(string='Title', required=True)
    active = fields.Boolean(string='Active', default=True)
    type = fields.Char(string='Type')
    addons = fields.Binary(string='Addons', required=True)
    addons_attache = fields.Many2one('ir.attachment',string='Addons Attache')
    content = fields.Text(string="Content")
    url = fields.Char(string="url")

    @api.model
    def create(self,vals):
        res = super(BcAwarenessMedia,self).create(vals)
        res.create_attache()
        return res

    def create_attache(self):
        url_base = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        new_attachment = self.env['ir.attachment'].create({
            'name': self.title,
            'res_name':self.title,
            'datas': self.addons
        })
        self.addons_attache = new_attachment.id
        self.url = url_base+"/web/content/%s"%(self.addons_attache.id)

class BcSelfCheckPlan(models.Model):
    _name = 'bc.self.check.plan'

    user_id = fields.Many2one('res.users', string='User', copy=False)
    date = fields.Char(string = 'Date')
    time = fields.Char(string = 'Time')
    duration = fields.Float(string = 'Duration')
    period = fields.Integer(string = 'Period')
    cycle = fields.Integer(string = 'Cycle')
    guid = fields.Char(string = 'GUID')

class Partner(models.Model):
    _inherit = 'res.partner'

    bc_partner = fields.Boolean(string="BC Partner")
    is_mobile_verified = fields.Boolean(string="Mobile Verified")
    weight = fields.Float(string="Weight")
    height = fields.Float(string="Height")
    birth_date = fields.Date(string="Birth Date")
    password = fields.Char(string="Password")
    addons_attache = fields.Many2one('ir.attachment',string='Addons Attache')
    url = fields.Char(string="url")

    @api.model
    def create(self, vals):
        res = super(Partner, self).create(vals)
        res.create_attache()
        return res

    def create_attache(self):
        url_base = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        new_attachment = self.env['ir.attachment'].create({
            'name': self.name,
            'res_name': self.name,
            'datas': self.image
        })
        self.addons_attache = new_attachment.id
        self.url = url_base + "/web/content/%s" % (self.addons_attache.id)


class BcMammogram(models.Model):
    _name = 'bc.mammogram'

    name = fields.Char(string="Name")
    address = fields.Char(string="Address")
    city = fields.Char(string="City")
    state = fields.Char(string="State")
    avatar = fields.Binary(string="Avatar")
    addons_attache = fields.Many2one('ir.attachment',string='Addons Attache')
    url = fields.Char(string="url")

    @api.model
    def create(self, vals):
        res = super(BcMammogram, self).create(vals)
        res.create_attache()
        return res

    def create_attache(self):
        url_base = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        new_attachment = self.env['ir.attachment'].create({
            'name': self.name,
            'res_name': self.name,
            'datas': self.avatar
        })
        self.addons_attache = new_attachment.id
        self.url = url_base + "/web/content/%s" % (self.addons_attache.id)


class BcParameters(models.Model):
    _name = 'bc.parameters'

    key = fields.Char(string="Key")
    description = fields.Char(string="Description")
    value = fields.Char(string="Value")


class BcQuestions(models.Model):
    _name = 'bc.questions'

    key = fields.Char(string="Key")
    text = fields.Char(string="Text")


class BcResults(models.Model):
    _name = 'bc.results'

    user_id = fields.Many2one('res.users', string="User")
    date = fields.Date(string='Date')
    time = fields.Char(string="Time")
    questions = fields.Many2many('bc.questions', string='Questions')
