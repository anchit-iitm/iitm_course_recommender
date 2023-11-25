from flask import current_app as app
from flask import jsonify, request
from common.models import *

from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_expects_json import expects_json

from common.response_codes import *
from common.helpers import role_required

import numpy as np

class Recommender(Resource):

    def __init__(self):
        super().__init__()

        self.completed_courses = []
        self.current_courses = []
        self.pending_courses = []
        self.level = ""
        self.dp_or_ds = ""
        self.max_subjects = 0
        self.matrix = []
        self.capability_score = 0

    def recommend_course(self):
        if len(self.pending_courses) == 0:
            return self.matrix
    

    def populate_fields(self, user):
        total = 0
        for seenCourse in user.completed_courses:
            if seenCourse.completed:
                rating = Courses.get_course_by_code(seenCourse.course_code).difficulty_rating                
                total += (rating/10) * (seenCourse.marks/100)

                self.completed_courses.append(seenCourse.course_code)
            
            else:
                self.current_courses.append(seenCourse.course_code)
        
        self.capability_score = total / len(self.completed_courses)

        self.level = user.curr_deg_level
        self.dp_or_ds = user.ds_or_dp
        self.max_subjects = user.max_subjects
    
    @jwt_required()
    def get(self):
        self.populate_fields(User.get_user_by_jwt(get_jwt_identity()))

    
