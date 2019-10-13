# -*- encoding: utf-8 -*-
import json
from odoo import fields, http, SUPERUSER_ID


class BcAwarness(http.Controller):
    @http.route(['/rest_api/users/register'],type='http',auth='none',csrf=False,methods=['POST'])
    def save_registration(self, **kw):
        values = {}
        data = {}
        for field_name, field_value in kw.items():
            values[field_name] = field_value
        if values['langauage'] == 'en':
            values['lang'] = 'en_US'
            # if values['avatar']:
            #     values['image'] = values['avatar']
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
        partner = user.partner_id
        if user:
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




