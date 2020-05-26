# -*- encoding: utf-8 -*-

import json
from odoo import fields, http, SUPERUSER_ID
import base64
from odoo.http import request
from odoo.addons.auth_signup.models.res_users import SignupError


class BcAwarness(http.Controller):

    @http.route(['/rest_api/users/register'],type='http',auth='none',csrf=False,methods=['POST'])
    def save_registration(self, **kw):
        values = {}
        data = {}
        for field_name, field_value in kw.items():
            values[field_name] = field_value
        exist = http.request.env['res.partner'].sudo().search([('email','=',values['email'])])
        if not exist:
            partner = http.request.env['res.partner'].sudo().create(values)
            user = http.request.env['res.users'].sudo().create({
                'name': values['name'],
                'login': values['email'],
                'password': values['password'],
                'partner_id': partner.id
            })
            data = {
                "success":"true",
                "message":"User account has been created successfully, please check you email we sent to you verification link",
                "data":{}}
        else:
            data = {"success":"false",
                    "message":"'Your account already exist in the app, please try to login.",
                    "error_code":1110,
                    "data":{ }}

        return json.dumps(data)

    @http.route(['/rest_api/users/login'],type='http',auth='none',csrf=False,methods=['POST'])
    def log_in(self, **kw):
        data = {}
        db = http.request.env.cr.dbname
        email = kw.get('email')
        password = kw.get('password')
        # try:
        uid = request.session.authenticate(db, email, password)
        if not  uid:
            data = {
                "success": "false", "message": "Invalid Credentials.", "error_code": 1107, "data": {}
            }
        else:
            user = http.request.env['res.users'].sudo().search([('id', '=', uid)])
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
                        "height": partner.height,
                        "mobile": partner.mobile,
                        "birth_date": partner.birth_date,
                        "lang": partner.lang,
                        "avatar":partner.url,
                        "has_family_history":partner.has_family_history
                    }}}
        # except:

        return json.dumps(data)

    @http.route(['/rest_api/users/password'],type='http',auth='none',csrf=False,methods=['POST'])
    def reset_password(self,**kw):
        db = http.request.env.cr.dbname
        email = kw.get('email')
        password = kw.get('oldPassword')
        try:
            uid = request.session.authenticate(db, email, password)
            if uid:
                user = http.request.env['res.users'].sudo().search([('id', '=', uid)])
                if user:
                    user.sudo().write({'password': kw.get('newPassword')})
                    return json.dumps({"success": "true", "message": "Your password have been updated",
                                       "data": {"user": {"id": user.id, }}})
        except:
            return json.dumps({"success": "false", "message": "Not Found.", "error_code": 1105, "data": {}})



    @http.route(['/rest_api/users/reset'],type='http',auth='none',csrf=False,methods=['POST'])
    def reset_email(self,**kw):
        user = http.request.env['res.users'].sudo().search([('login','=',kw.get('email'))])
        if user:
            user.sudo().action_reset_password()
            return json.dumps({"success":"true","message":"A verificaction link has been sent to you email account",
                               "data":{"user":{"id":user.id,}}})
        else:
            return json.dumps({"success": "false","message":"Not Found.","error_code":1105,"data":{} })

    @http.route(['/rest_api/users/<string:id>'], type='http', auth='none', csrf=False, methods=['PUT'])
    def get_profiles_data(self,id,**kw):
        user = http.request.env['res.users'].sudo().search([('id','=',id)])
        if user:
            partner = user.partner_id
            values = {}
            for field_name, field_value in kw.items():
                values[field_name] = field_value
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
                    "height": partner.height,
                    "mobile": partner.mobile,
                    "birth_date": partner.birth_date,
                    "lang":partner.lang ,
                }}}
            return json.dumps(data)
        else:
            return json.dumps({"success": "false", "message": "Not Found.", "error_code": 1105, "data": {}})

    @http.route(['/rest_api/users/<string:id>/image'], type='http', auth='none', csrf=False, methods=['PUT'])
    def get_profile(self, id,**kw):
        user = http.request.env['res.users'].sudo().search([('id','=',id)])
        if user:
            partner = user.partner_id
            partner.sudo().write({'image':base64.encodebytes(kw.get('image').read())})
            data = {
                "success": "true",
                "message": "User information has been updated successfully",
                "data": {"user": {
                    "id": user.id,
                    "avatar": partner.url,
                }}}
            return json.dumps(data)
        else:
            return json.dumps({"success": "false", "message": "Invalid image format.", "error_code": 1105, "data": {}})

    @http.route(['/rest_api/users/<string:id>'], type='http', auth='none', csrf=False, methods=['GET'])
    def get_info(self,id,**kw):
        user = http.request.env['res.users'].sudo().search([('id', '=', id)])
        if user:
            partner = user.partner_id
            data = {
                "success": "true",
                "message": "User information has been updated successfully",
                "data": {"user": {
                    "id": user.id,
                    "name": partner.name,
                    "country_code": "00249",
                    "weight": partner.weight,
                    "height": partner.height,
                    "mobile": partner.mobile,
                    "birth_date": partner.birth_date,
                    "has_family_history": partner.has_family_history,
                    "langauage": partner.lang,
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
                    "id":rec.id,"name":rec.name,"address":rec.address,"city":rec.city,"state":rec.state,"avatar":rec.url
                }
                li.append(mono)
            return json.dumps({"success":"true",
                               "message":"Data found","data":{"mammograms":li}})
        data = {
                "success": "false",
                "message": "Data not found",
                "error_code": 1105,
                "data": {}
        }
        return json.dumps(data)

    @http.route(['/rest_api/features'], type='http', auth='none', csrf=False, methods=['GET'])
    def get_features(self, **kw):
        record = http.request.env['bc.awareness.media'].sudo().search([('id', '!=', False)])
        #print("dddddddddddddddddddd",record)
        if record:
            li = []
            for rec in record:
                media = {
                    "id":rec.id,
                    "content":rec.content,"title":rec.title,
                    "type":rec.type,
                    "url":rec.url,
                }
                li.append(media)
            return json.dumps({"success":"true","message":"Data found","data":{"features":li}})
        data = {
                "success": "false",
                "message": "Data not found",
                "error_code": 1105,
                "data": {}
        }
        return json.dumps(data)


    @http.route(['/rest_api/users/<string:user_id>/reminders'], type='http', auth='none', csrf=False, methods=['POST'])
    def set_check_plan(self, **kw):
        """Function TO Add User Self Check Plan"""
        is_check = kw.get('is_self_check', 'false')

        check_plan = http.request.env['bc.self.check.plan'].sudo().create(
            {
                'user_id': int(kw['user_id']),
                'date': kw['date'],
                'time': kw['time'],
                'duration': float(kw['duration']),
                'period': int(kw['period']),
                'cycle': int(kw['cycle']),
                'is_self_check': False if is_check == 'false' else True,
                'uuid': kw['uuid'],
            })
        if check_plan:
            data = {
                "success": "true",
                "message": "Scheduler created successfully",

                "data": {
                    "scheduler": {
                        'id': check_plan.id,
                        'date': check_plan.date,
                        'time': check_plan.time,
                        'duration': check_plan.duration,
                        'period': check_plan.period,
                        'cycle': check_plan.cycle,
                        'uuid': check_plan.uuid,
                        'is_self_check': check_plan.is_self_check,
                    }
                }
            }
            return json.dumps(data)
        data = {
                "success": "false",
                "message": "Data not found",
                "error_code": 1105,
                "data": {}
        }
        return json.dumps(data)

    @http.route(['/rest_api/users/<string:user_id>/shedulers'], type='http', auth='none', csrf=False, methods=['GET'])
    def get_check_plan(self, **kw):
        """Function TO Return User Self Check Plans"""

        plans = http.request.env['bc.self.check.plan'].sudo().search([('user_id', '=', int(kw['user_id']))])
        if plans:
            plns = []
            for plan in plans:
                plns.append(
                    {
                        'id': plan.id,
                        'date': plan.date,
                        'time': plan.time,
                        'duration': plan.duration,
                        'period': plan.period,
                        'cycle': plan.cycle,
                        'uuid': plan.uuid,
                        'ClientLastUpdate': fields.Date.to_string(plan.write_date),
                    }
                )
            data = {
                "success": "true",
                "message": "Data found",
                "data": {
                    "schedulers": plns,
                }
            }
        else:
            data = {
                "success": "false",
                "message": "Data not found",
                "error_code": 1105,
                "data": {}
            }
        return json.dumps(data)

    @http.route(['/rest_api/users/<string:user_id>/reminders/<string:plan_id>'], type='http', auth='none', csrf=False, methods=['PUT'])
    def update_check_plan(self, **kw):
        """Function TO Write User Self Check Plan"""

        plan = http.request.env['bc.self.check.plan'].sudo().search([('user_id', '=', int(kw['user_id'])),
                                                                     ('id', '=', int(kw['plan_id']))])
        if plan:
            plan.sudo().write({
                'date': kw['date'],
                'time': kw['time'],
                'duration': float(kw['duration']),
                'period': int(kw['period']),
                'cycle': int(kw['cycle']),
            })
            data = {
                "success": "true",
                "message": "Scheduler updated successfully",
                "data": {
                    "scheduler": {
                        'id': plan.id,
                        'date': plan.date,
                        'time': plan.time,
                        'duration': plan.duration,
                        'period': plan.period,
                        'cycle': plan.cycle,
                    }
                }
            }
            return json.dumps(data)
        data = {
                "success": "false",
                "message": "Data not found",
                "error_code": 1105,
                "data": {}
        }
        return json.dumps(data)

    @http.route(['/rest_api/users/<string:user_id>/reminders/<string:plan_id>'], type='http', auth='none', csrf=False, methods=['DELETE'])
    def unlink_check_plan(self, **kw):
        """Function TO Delete User Self Check Plan"""
        plan = http.request.env['bc.self.check.plan'].sudo().search([('user_id', '=', int(kw['user_id'])),
                                                                     ('id', '=', int(kw['plan_id']))])
        if plan:
            plan.sudo().unlink()
            data = {
                "success": "true",
                "message": "Scheduler deleted successfully",
                "data": {}
                }
            return json.dumps(data)
        data = {
                "success": "false",
                "message": "Data not found",
                "error_code": 1105,
                "data": {}
        }
        return json.dumps(data)

    @http.route(['/rest_api/questions/'], type='http', auth='none', csrf=False, methods=['GET'])
    def get_questions(self, **kw):
        """Function TO Return questions"""

        questions = http.request.env['bc.questions'].sudo().search([('id', '!=', False)])
        if questions:
            quest = []
            for question in questions:
                quest.append(
                    {
                        'id': question.id,
                        'text': question.text,
                        'key': question.key,
                        'ar_text':question.text_arb,
                    }
                )
            data = {
                "success": "true",
                "message": "Data found",
                "data": {
                    "questions": quest,
                }
            }
        else:
            data = {
                "success": "false",
                "message": "Data not found",
                "error_code": 1105,
                "data": {}
            }
        return json.dumps(data)

    @http.route(['/rest_api/parameters/'], type='http', auth='none', csrf=False, methods=['GET'])
    def get_parameters(self, **kw):
        """Function TO Return Parameters"""

        parameters = http.request.env['bc.parameters'].sudo().search([('id', '!=', False)])
        if parameters:
            parg = []
            for parameter in parameters:
                parg.append(
                    {
                        'id': parameter.id,
                        'key': parameter.key,
                        'description': parameter.description,
                        'value': parameter.value,
                    }
                )
            data = {
                "success": "true",
                "message": "Data found",
                "data": {
                    "Parameters": parg,
                }
            }
        else:
            data = {
                "success": "false",
                "message": "App Server Error, please contact the admin.",
                "error_code": 1000,
                "data": {}
            }
        return json.dumps(data)

    @http.route(['/rest_api/users/<string:user_id>/results'], type='http', auth='none', csrf=False, methods=['GET'])
    def get_result(self, user_id,**kw):
        """Function TO Return User Self result"""
        quest = []
        user = http.request.env['res.users'].sudo().search([('id', '=', user_id)])
        results = http.request.env['bc.results'].sudo().search([('user_id', '=', user.id)])
        if results:
            for res in results:
                for question in res.questions:
                    quest.append(
                        question.id
                    )
            reslt = []
            for result in results:
                reslt.append(
                    {
                        'id': result.id,
                        'userId': result.user_id.id,
                        'date': result.date,
                        'time': result.time,
                        'questions': quest,
                    }
                )
            data = {
                "success": "true",
                "message": "Data found",
                "data": {
                    "results": reslt,
                }
            }
        else:
            data = {
                "success": "false",
                "message": "Data not found",
                "error_code": 1105,
                "data": {}
            }
        return json.dumps(data)

    @http.route(['/rest_api/users/<string:user_id>/results'],type='http',auth='none',csrf=False,methods=['POST'])
    def save_result(self, **kw):
        list_ids = list(kw.get('questions').split(","))
        list_ids = http.request.env['bc.questions'].sudo().search([('id', 'in', list_ids)]).ids
        create_result = http.request.env['bc.results'].sudo().create(
            {
                'user_id': kw.get('user_id'),
                'date': kw.get('date'),
                'time': kw.get('time'),
                'questions': [(6, 0, list_ids)],
            })
        if create_result:
            data = {
                "success": "true",
                "message": "result created successfully",
                "data": {
                    "check": {
                        'id': create_result.id,
                        'userId': create_result.user_id.id,
                        'date': create_result.date,
                        'time': create_result.time,
                        'questions': [re.id for re in create_result.questions],
                    }
                }
            }
            return json.dumps(data)
        data = {
                "success": "false",
                "message": "Data not found",
                "error_code": 1105,
                "data": {}
        }
        return json.dumps(data)

    @http.route(['/rest_api/users/<string:user_id>/results/<string:result_id>'], type='http', auth='none', csrf=False, methods=['PUT'])
    def update_result(self,**kw):
        """Function TO Write User Self result"""
        result = http.request.env['bc.results'].sudo().search([('id', '=', kw.get('result_id'))])
        if result:
            list_ids = list(kw.get('questions').split(","))
            list_ids = http.request.env['bc.questions'].sudo().search([('id', 'in', list_ids)]).ids
            result.sudo().write({
                'date': kw.get('date'),
                'time': kw.get('time'),
                'questions': [(6, 0, list_ids)],
            })
            data = {
                "success": "true",
                "message": "Result updated successfully",
                "data": {
                    "check": {
                        'id': result.id,
                        'userId': result.user_id.id,
                        'date': result.date,
                        'time': result.time,
                        'questions':  [re.id for re in result.questions],
                    }
                }
            }
            return json.dumps(data)
        data = {
                "success": "false",
                "message": "Data not found",
                "error_code": 1105,
                "data": {}
        }
        return json.dumps(data)

    @http.route(['/rest_api/users/<string:user_id>/results/<string:result_id>'], type='http', auth='none', csrf=False, methods=['DELETE'])
    def unlink_result(self,**kw):
        """Function TO Delete User result"""
        user = http.request.env['res.users'].sudo().search([('id', '=', kw.get('user_id'))])
        result = http.request.env['bc.results'].sudo().search([('user_id', '=', user.id),
                                                                     ('id', '=', kw.get('result_id'))])
        if result:
            result.sudo().unlink()
            data = {
                "success": "true",
                "message": "Result deleted successfully",
                "data": {}
                }
            return json.dumps(data)
        else:
            data = {
                "success": "false",
                "message": "Result Not deleted",
                "data": {}
            }
            return json.dumps(data)
        data = {
                "success": "false",
                "message": "Data not found",
                "error_code": 1105,
                "data": {}
        }
        return json.dumps(data)