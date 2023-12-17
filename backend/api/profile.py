from flask import current_app as app
from flask import jsonify, request
from common.models import *

from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_expects_json import expects_json

from common.response_codes import *
from common.helpers import role_required

class Student(Resource):

    # does not allow any method in the class to be accessed without login
    @jwt_required()

    # only student role can access this class methods
    @role_required('student')
    def __init__(self):
        super().__init__()

    # THE GET ENDPOINT    
    def get(self):
        '''
        The get endpoint for /api/v1/profile
        Requires user info in the form of JWT Bearer Token, returns JSON Response as per API documentation.
        '''
        # try doing shit, otherwise throw 500 error
        try:
            # get the user details from the jwt
            student = User.get_user_by_jwt(get_jwt_identity())      
            
            # if details found, continue, else throw 404
            if not student:
                return show_404()
            
            # build the return data object
            data = {
                'email': student.email,
                'pic': student.pic,
                'role': student.role[0].role,
                'bio': {
                    "maximum_courses_in_a_term": student.max_subjects,
                    "current_degree_level": student.curr_deg_level,
                    "dp_or_ds": student.ds_or_dp,
                    "current_courses": [i.course_code for i in student.completed_courses if i.completed == False],
                    "completed_courses": [{"id": i.course_code, "marks": i.marks} for i in student.completed_courses if i.completed == True],
                }
            }
            
            # return as json
            return make_response(jsonify(data), 200)
        except:
            app.logger.exception("API_Profile_GET")
            return show_500()
    






    # this schema is verified for the json before adding/updating profile
    profile_add_schema = {
        "type": "object", 
        "properties": {
            "pic": {
                "type": "string"
            },
            "maximum_courses_in_a_term" : {
                "type": "integer",
                "minimum": 2,
                "maximum": 4
            },
            "current_degree_level": {
                "type": "string",
                "enum": ["foundation", "diploma", "degree"]
            },
            "dp_or_ds": {
                "type": "string",
                "enum": ["dp", "ds", "both"]
            },
            "current_courses": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "completed_courses": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "marks": {
                                "type": "number",
                                "minimum": 0,
                                "maxmimum": 100
                            }
                    },
                    "required": ["id", "marks"]
                }
            }
        }            
    }

    @expects_json(profile_add_schema)   
    def post(self, patch=False):
        '''
        The post endpoint for /api/v1/profile
        Requires user info in the form of JWT Bearer Token, returns JSON Response of success.
        '''
        # try doing shit, otherwise throw 500 error
        try:
            # get the user details from the jwt
            student = User.get_user_by_jwt(get_jwt_identity())      
            
            # if details found, continue, else throw 404
            if not student:
                return show_404()
            
            # set each column to what we recieved. if reception is empty, set it to already existing value
            student.pic = request.json.get("pic", student.pic)            
            student.max_subjects = request.json.get("maximum_courses_in_a_term", student.max_subjects)
            student.curr_deg_level = request.json.get("current_degree_level", student.curr_deg_level)
            student.ds_or_dp = request.json.get("dp_or_ds", student.ds_or_dp)

            current_courses = request.json.get("current_courses", None)            
            if current_courses:
                # current_courses is recieved in the API
                for code in current_courses:
                    # Iterate through each course

                    # check if such a course even exists, else throw 400
                    if not Courses.has(code):
                        return show_400(f"The course {code} does not exist")
                    
                    # course exists, check if an entry already exists in completed courses
                    if CompletedCourses.has(student.id, code):
                        # entry exists, update it
                        binding = CompletedCourses.get(student.id, code)
                        binding.completed = False
                        binding.marks = None
                        binding.save()
                    else:
                        # entry does not exist, create it
                        binding = CompletedCourses(user_id = student.id, course_code = code, completed = False)
                        binding.save()
            
            completed_courses = request.json.get("completed_courses", None)
            if completed_courses:
                # completed_courses is recieved in the API
                for course in completed_courses:
                    # Iterate through each course

                    # check if such a course even exists, else throw 400
                    if not Courses.has(course['id']):
                        return show_400(f"The course {course['id']} does not exist")
                    
                    # course exists, check if an entry already exists in completed courses
                    if CompletedCourses.has(student.id, course['id']):
                        # entry exists, update it
                        binding = CompletedCourses.get(student.id, course['id'])
                        binding.completed = True
                        binding.marks = course['marks']
                        binding.save()
                    else:
                        # entry does not exist, create it        
                        binding = CompletedCourses(user_id = student.id, course_code = course['id'], completed = True, marks=course['marks'])
                        binding.save()

            # if endpoint is patch, send Patch response message, else Post response message
            if patch:
                return show_202("Profile Updated!")
            else:
                return show_201("Profile Saved!")
                
        except:
            app.logger.exception("API_Profile_POST")
            return show_500()
    

    @expects_json(profile_add_schema)
    def patch(self):
        '''
        The patch endpoint for /api/v1/profile
        Requires user info in the form of JWT Bearer Token, returns JSON Response of success.
        '''
        # since the steps of patching and posting are same, we call the above method only for the patch
        return self.post(patch=True)