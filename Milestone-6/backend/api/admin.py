from flask import current_app as app
from flask import jsonify, request
from common.models import *

from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_expects_json import expects_json

from common.response_codes import *
from common.helpers import role_required


class SuperAdmin(Resource):
    
    @jwt_required()
    @role_required('admin')
    def __init__(self):
        super().__init__()
    
    get_marshal =   {
        "name": fields.String,
        "email": fields.String,
        "role": fields.String(attribute=lambda user: user.role[0]),
        "created_at": fields.String
    }
    
    @marshal_with(get_marshal)
    def get(self):
        '''
        GET Endpoint for /api/v1/admins
        Retrieves list of all admin users including SuperAdmins,
        Course Team Members, IITM Management
        '''
        try:            
            return User.get_all_users_with_role(('admin', 'im', 'ctm'))
        except:
            app.logger.exception("API_Admin_GET")
            return show_500()
    

    postpatch_admin_schema = {
        "type": "object", 
        "properties": {
            "email": {
                "type": "string",
                "minLength": 3
            },
            "role": {
                "type": "string",
                "enum": ["admin", "im", "ctm"]
            }
        },
        "required": ["email", "role"]
    }

    def _update_role(self, user, newRole):
        user = User.get_user_by_email(user)
        if not user:
            return False
        
        role = Role.get_role(newRole)
        user.role = [role]
        user.save()
        return True

    @expects_json(postpatch_admin_schema)
    def post(self):
        try:
            if self._update_role(request.json.get('email', None), request.json.get('role')):
                return show_201("Admin Added")
            else:
                return show_400("Email does not exist")
        except:
            app.logger.exception("API_Admin_POST")
            return show_500()
    
    @expects_json(postpatch_admin_schema)
    def patch(self):
        try:
            if self._update_role(request.json.get('email', None), request.json.get('role')):
                return show_200("Admin Role updated")
            else:
                return show_400("Email does not exist")
        except:
            app.logger.exception("API_Admin_POST")
            return show_500()
    

    delete_schema = {
        "type": "object", 
        "properties": {
            "email": {
                "type": "string",
                "minLength": 3
            }
        },
        "required": ["email"]
    }

    @expects_json(delete_schema)
    def delete(self):
        try:
            if self._update_role(request.json.get('email', None), 'student'):
                return show_200("Admin Deleted")
            else:
                return show_400("Email does not exist")
        except:
            app.logger.exception("API_Admin_POST")
            return show_500()