from flask import current_app as app
from flask import jsonify, request
from common.models import *

from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_expects_json import expects_json

from common.response_codes import *
from common.helpers import role_required



class GeneralStatistics(Resource):

    @role_required('admin')
    def get(self):

        try:
            data = {
                "students": {
                    "total": User.get_count_of_users_with_role(['student']),
                    "foundation": User.get_count_of_student_in_level(['foundation']),
                    "diploma": User.get_count_of_student_in_level(['diploma']),
                    "bsc": User.get_count_of_student_in_level(['bsc']),
                    "bs": User.get_count_of_student_in_level(['bs']),
                },
                "courses": {
                    "total": Courses.get_count_of_courses_in_level(),
                    "foundation": Courses.get_count_of_courses_in_level(['foundation']),
                    "diploma": Courses.get_count_of_courses_in_level(['diploma']),
                    "degree": Courses.get_count_of_courses_in_level(['degree'])
                },
                "admins": {
                    "superadmins": User.get_count_of_users_with_role(['admin']),
                    "ctm": User.get_count_of_users_with_role(['ctm']),
                    "management": User.get_count_of_users_with_role(['im']),
                },
            }

            return make_response(jsonify(data), 200)
        
        except Exception as e:
            app.logger.exception(e)
            return show_500()