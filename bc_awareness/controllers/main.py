# -*- encoding: utf-8 -*-
import json
from odoo import fields, http, SUPERUSER_ID
import base64
from odoo.http import request




class BcAwarness(http.Controller):
    @http.route(['/rest_api/users/register'],type='http',auth='none',csrf=False,methods=['POST'])
    def save_registration(self, **kw):
        values = {}
        data = {}
        for field_name, field_value in kw.items():
            values[field_name] = field_value
        if values['langauage'] and values['langauage'] == 'en':
            values['lang'] = 'en_US'
        if values['avatar']:
            values['image'] = base64.encodebytes( values['avatar'].read())
        exist = http.request.env['res.partner'].sudo().search([('email','=',values['email'])])
        if not exist:
            partner = http.request.env['res.partner'].sudo().create(values)
            user = http.request.env['res.users'].sudo().create({
                'name': values['name'],
                'login': values['email'],
                'password': values['password'],
                'partner_id': partner.id
            })
            # image_url =
            data = {
                "success":"true",
                "message":"User account has been created successfully, please check you email we sent to you verification link",
                "data":{ "user":{
                    "id":user.id,
                    "name":partner.name,
                    "partner_id":partner.id,
                    "email":partner.email,
                    "country_code":"00249",
                    "weight":partner.weight,
                    "hieght":partner.height,
                    "mobile":partner.mobile,
                    "birth_date":partner.birth_date,
                    "langauage":"en",
                    "is_mobile_verified":"false",
                    # "avatar":"http://localhost:3000/default_image.png"
                }}}
        else:
            data = {"success":"false",
                    "message":"'Your account already exist in the app, please try to login.",
                    "error_code":1110,
                    "data":{ }}

        return json.dumps(data)


    @http.route(['/rest_api/users/login'],type='http',auth='none',csrf=False,methods=['POST'])
    def log_in(self, **kw):
        data = {}
        user = http.request.env['res.users'].sudo().search([('login','=',kw.get('email')),('password','=',kw.get('password'))])
        if user:
            partner = user.partner_id
            data = {
                "success": "true",
                "message": "User account has been created successfully, please check you email we sent to you verification link",
                "data": {"user": {
                    "id": user.id,
                    "name": partner.name,
                    "partner_id": partner.id,
                    "email": partner.email,
                    "country_code": "00249",
                    "weight": partner.weight,
                    "hieght": partner.height,
                    "mobile": partner.mobile,
                    "birth_date": partner.birth_date,
                    "langauage": "en",
                    "is_mobile_verified": "false",
                    # "avatar":"http://localhost:3000/default_image.png"
                }}}
        else:
            data = {
                "success":"false","message":"Invalid Credentials.","error_code":1107,"data":{}
            }
        return json.dumps(data)

    @http.route(['/rest_api/users/reset'],type='http',auth='none',csrf=False,methods=['POST'])
    def reset_email(self,**kw):
        user = http.request.env['res.users'].sudo().search([('login','=',kw.get('email'))])
        if user:
            user.sudo().action_reset_password()
            return json.dumps({"success":"true","message":"A verificaction link has been sent to you email account",
                               "data":{"user":{"id":user.id,}}})
        else:
            return json.dumps({"success": "false","message":"Not Found.","error_code":1105,"data":{} })

    @http.route(['/rest_api/users/<model("res.users"):id'], type='http', auth='none', csrf=False, methods=['PUT'])
    def get_profile(self,id,**kw):
        id = request.env['res.users']
        print("dddddddddddddddddddddd",id)
        user = http.request.env['res.users'].sudo().search([('id','=',kw.get('id'))])
        if user:
            partner = user.partner_id
            values = {}
            for field_name, field_value in kw.items():
                values[field_name] = field_value
            if values['langauage'] and values['langauage'] == 'en':
                values['lang'] = 'en_US'
            record = http.request.env['res.partner'].sudo().search([('id', '=',partner.id)])
            record.sudo().write(values)
            data = {
                "success": "true",
                "message": "User information has been updated successfully",
                "data": {"user": {
                    "id": user.id,
                    "name": partner.name,
                    "country_code": "00249",
                    "weight": partner.weight,
                    "hieght": partner.height,
                    "mobile": partner.mobile,
                    "birth_date": partner.birth_date,
                    "langauage": "en",
                }}}
            return json.dumps(data)
        else:
            return json.dumps({"success": "false", "message": "Not Found.", "error_code": 1105, "data": {}})

    @http.route(['/rest_api/users'], type='http', auth='none', csrf=False, methods=['PUT'])
    def get_profile(self, **kw):
        user = http.request.env['res.users'].sudo().search([('id','=',kw.get('id'))])
        if user:
            partner = user.partner_id
            partner.sudo().write({'image':base64.encodebytes(kw.get('avatar').read())})
            data = {
                "success": "true",
                "message": "User information has been updated successfully",
                "data": {"user": {
                    "id": user.id,
                    # "avatar": partner.name,
                }}}
            return json.dumps(data)
        else:
            return json.dumps({"success": "false", "message": "Invalid image format.", "error_code": 1105, "data": {}})

    http.route(['/rest_api/users/<model("res.users"):id'], type='http', auth='none', csrf=False, methods=['GET'])

    def get_info(self,**kw):
        id = request.env['res.users']
        print("dddddddddddddddddddddd", id)
        user = http.request.env['res.users'].sudo().search([('id', '=', kw.get('id'))])
        if user:
            partner = user.partner_id
            values = {}
            for field_name, field_value in kw.items():
                values[field_name] = field_value
            if values['langauage'] and values['langauage'] == 'en':
                values['lang'] = 'en_US'
            record = http.request.env['res.partner'].sudo().search([('id', '=', partner.id)])
            record.sudo().write(values)
            data = {
                "success": "true",
                "message": "User information has been updated successfully",
                "data": {"user": {
                    "id": user.id,
                    "name": partner.name,
                    "country_code": "00249",
                    "weight": partner.weight,
                    "hieght": partner.height,
                    "mobile": partner.mobile,
                    "birth_date": partner.birth_date,
                    "langauage": "en",
                }}}
            return json.dumps(data)
        else:
            return json.dumps({"success": "false", "message": "Not Found.", "error_code": 1105, "data": {}})

    @http.route(['/rest_api/mammograms'], type='http', auth='none', csrf=False, methods=['GET'])
    def get_mammograms(self, **kw):
        record = http.request.env['bc.mammogram'].sudo().search([('id','!=',False)])
        if record:
            li = []
            for rec in record:
                mono = {
                    "id":rec.id,"name":rec.name,"address":rec.address,"city":rec.city,"state":rec.state,
                    #                 "avatar":""
                }
                li.append(mono)
            return json.dumps({"success":"true",
                               "message":"Data found","data":{"mammograms":li}})

    @http.route(['/rest_api/features'], type='http', auth='none', csrf=False, methods=['GET'])
    def get_mammograms(self, **kw):
        record = http.request.env['bc.awareness.media'].sudo().search([('id', '!=', False)])
        print("dddddddddddddddddddd",record)
        if record:
            li = []
            for rec in record:
                media = {
                    "id":rec.id,
                    "content":rec.content,"title":rec.title,
                    "type":rec.type,
                    "addons":[]
                }
                li.append(media)
            return json.dumps({"success":"true","message":"Data found","data":{"features":li}})












