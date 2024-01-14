from flask import current_app as app
from flask import jsonify, request
from common.models import *

from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_expects_json import expects_json

from common.response_codes import *
from common.helpers import role_required


class AllStudents(Resource):
    
    @jwt_required()
    @role_required('admin')
    def __init__(self):
        super().__init__()
    
    get_marshal =   {
        "name": fields.String,
        "email": fields.String,
        "role": fields.String(attribute=lambda user: "student"),
        "created_at": fields.String
    }
    
    @marshal_with(get_marshal)
    def get(self):
        '''
        GET Endpoint for /api/v1/admins
        Retrieves list of all students
        '''
        try:            
            return User.get_all_users_with_role(('student',))
        except:
            app.logger.exception("API_Student_GET")
            return show_500()