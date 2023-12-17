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
from itertools import combinations
import random

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
        self.prereqs = dict()
        self.coreqs = dict()

    def __filter_prereqs(self):
        possible_next_courses = []
        for pendingCourse in self.pending_courses:
            keep = True
            if pendingCourse.code in self.prereqs:
                for prereqs in self.prereqs[pendingCourse.code]:
                    if prereqs not in self.completed_courses:
                        keep = False
            
            if self.level != pendingCourse.level:                
                keep = False

            if keep:                
                if (self.dp_or_ds == 'both') or (pendingCourse.dp_or_ds == self.dp_or_ds):
                    possible_next_courses.append(pendingCourse)
        
        return possible_next_courses
    
    def __filter_level_dp_or_ds(self, possible_next_courses):        
        if len(possible_next_courses) == 0:
            old_dp_or_ds = self.dp_or_ds
            self.dp_or_ds = 'both'
            possible_next_courses = self.__filter_prereqs()
        
        if len(possible_next_courses) == 0:                
            self.dp_or_ds = old_dp_or_ds
            self.level = 'diploma' if self.level == 'foundation' else 'degree'
            possible_next_courses = self.__filter_prereqs()
            if len(possible_next_courses) == 0:            
                self.dp_or_ds = 'both'
                possible_next_courses = self.__filter_prereqs()
        
        return possible_next_courses

    def __make_combinations(self, possible_next_courses):
        final_combinations = []
        possible_combinations = combinations(possible_next_courses, self.max_subjects)
        
        for aCombination in possible_combinations:
            accepted = True
            for aCourse in aCombination:
                if len(self.coreqs[aCourse.code]) > 0:                    
                    for aCoreq in self.coreqs[aCourse.code]:
                        if aCoreq not in aCombination:
                            accepted = False
            
            if accepted:
                final_combinations.append(aCombination)
        
        return final_combinations

    def __recommend_course(self):        
        possible_next_courses = self.__filter_level_dp_or_ds(self.__filter_prereqs())
        #app.logger.info(possible_next_courses)
        if len(possible_next_courses) <= self.max_subjects:
            return possible_next_courses
        
        combs = self.__make_combinations(possible_next_courses)
        if len(combs) == 1:
            return combs[0]
        
        # more than 1 combinations exist. Check difficulty score vs capability score next.        
        return random.choice(combs) if len(combs) > 0 else []

    def __populate_fields(self, user):
        total = 0
        allCourses = Courses.get_all_courses()
        for aCourse_object in allCourses:
            self.prereqs[aCourse_object.code] = aCourse_object.pre_reqs
            self.coreqs[aCourse_object.code] = aCourse_object.co_reqs
            self.pending_courses.append(aCourse_object)
        
        for seenCourse in user.completed_courses:
            courses_object = Courses.get_course_by_code(seenCourse.course_code)
            self.pending_courses.remove(courses_object)
            if seenCourse.completed:
                rating = courses_object.difficulty_rating                
                total += (rating/10) * (seenCourse.marks/100)
                self.completed_courses.append(courses_object)            
            else:
                self.current_courses.append(courses_object)
                self.completed_courses.append(courses_object)

        self.capability_score = total / len(self.completed_courses) if len(self.completed_courses) > 0 else 1
        self.level = user.curr_deg_level
        self.dp_or_ds = user.ds_or_dp
        self.max_subjects = user.max_subjects        
    
    @jwt_required()
    def get(self):
        user = User.get_user_by_jwt(get_jwt_identity())
        
        self.__populate_fields(user)
        r = self.__recommend_course()

        return_object = {
            "no_courses": self.max_subjects,
            "upcoming_term": [i.code for i in r],
            "matrix_order": []
        }
        while(len(r) > 0):
            return_object["matrix_order"].append([{"id": i.code, "name":i.name} for i in r])
            for i in r:
                self.completed_courses.append(i)
                self.pending_courses.remove(i)

            r = self.__recommend_course()
        
        return make_response(jsonify(return_object), 200)

                
    
