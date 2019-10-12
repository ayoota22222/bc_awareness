# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api


class BcAwarenessApi(models.Model):
    _name = 'bc.awareness.api'

    # @api.model
    # def get_no_of_checks(self):
    #     res = []
    #     user_id = self.env.user.id
    #     media = self.env['bc.awareness.self.check'].search([('user', '=', user_id)])
    #     print(len(media))
    #     return len(media)
    #
    # @api.model
    # def get_check_details(self):
    #     res = []
    #     user_id = self.env.user.id
    #     self_checks = self.env['bc.awareness.self.check'].search([('user', '=', user_id)])
    #     for l in self_checks:
    #         res.append({'date': l.date, 'symptoms': l.symptom_ids})
    #     return

    @api.model
    def get_media(self, ):
        res = []
        media = self.env['bc.awareness.media'].search_read([('type', '=',)], fields=['attachment'])
        for s in media:
            res.append(s['attachment'])
        return res

    @api.model
    def signup(self, data):
        print("....................", data)
        values = {
            'name': data['name'],
            'login': data['login'],
            'country_id': data['country_id'],
            'password': data['password'],

        }
        return self.env['res.users'].sudo().signup(values)
