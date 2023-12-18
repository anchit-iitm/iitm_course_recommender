from flask import current_app as app
from flask import jsonify, request
from common.models import *

from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_expects_json import expects_json

from common.response_codes import *
from common.helpers import role_required

course_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'level': {
            'type': 'string',
            'enum': ['foundation', 'diploma', 'degree']},
        'dp_or_ds': {
            'type': 'string',
            'enum': ['dp', 'ds']},
        'credits': {
            'type': 'number',
            'minimum': 1,
            'maximum': 4},
        'instructors': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'}
                },
                'required': ['email']
            }
        }
    },
    'required': ['name', 'description', 'level', 'dp_or_ds', 'credits', 'instructors']
}

class CourseResource(Resource):
    # GET method for retrieving a single course by ID
    def get(self, id):
        try:
            # Query the database for the course with the specified ID
            course = Courses.get_course_by_code(id)

            if not course:
                return show_404('Course not found')

            return make_response(jsonify(Courses.get_course_by_code_as_dict(id)), 200)

        except Exception as e:
            return show_500()

    # PATCH method for modifying a single course by ID
    @role_required('admin')
    @expects_json(course_schema)
    def patch(self, id):
        try:
            # Query the database for the course with the specified ID
            course = Courses.get_course_by_code(id)

            if not course:
                return show_404('Course not found')

            # Parse the JSON data from the request
            data = request.get_json()

            # Update the course properties based on the received data
            course.name = data.get('name', course.name)
            course.description = data.get('description', course.description)
            course.level = data.get('level', course.level)
            course.dp_or_ds = data.get('dp_or_ds', course.dp_or_ds)
            course.credits = data.get('credits', course.credits)
            new_instructors = data.get('instructors', None)
            if new_instructors:
                course.instructors = []
                for i in new_instructors:
                    ins = User.get_user_by_email(i['email'])
                    course.instructors.append(ins)
            # Update other properties as needed

            # Commit the changes to the database
            db.session.commit()

            return show_200('Course information modified successfully')

        except Exception as e:
            # Rollback changes in case of an exception
            db.session.rollback()
            return show_500()

    # DELETE method for deleting a single course by ID
    @role_required('admin')
    def delete(self, id):
        try:
            # Query the database for the course with the specified ID
            course = Courses.get_course_by_code(id)

            if not course:
                return show_404('Course not found')

            # Delete the course from the database
            db.session.delete(course)
            db.session.commit()

            return show_200('Course deleted successfully')

        except Exception as e:
            # Rollback changes in case of an exception
            db.session.rollback()
            return show_500()

# Resource for handling multiple courses
class CoursesResource(Resource):
    # GET method for retrieving all courses
    def get(self):
        try:
            # Query the database for all courses
            courses = Courses.get_all_courses()
            app.logger.info(courses)

            if not courses:
                return show_404('No courses found')

            # Format courses data for response
            courses_data = [
                {
                    'id': course.code,
                    'name': course.name,
                    'description': course.description,
                    'difficulty_rating': course.difficulty_rating,
                    'level': course.level,
                    'pre_req': [prerequisite.code for prerequisite in course.pre_reqs],
                    'co_req': [corequisite.code for corequisite in course.co_reqs],
                    # 'availability': [availability for availability in course.availability],
                    'instructors': [
                        {'name': instructor.name, 'email': instructor.email}
                        for instructor in course.instructors
                    ]
                }
                for course in courses
            ]

            return make_response(jsonify(courses_data), 200)

        except Exception as e:
            app.logger.exception(e)
            return show_500()

    # POST method for adding a new course
    @role_required('admin')
    @expects_json(course_schema)
    def post(self):
        try:
            # Parse the JSON data from the request
            data = request.get_json()

            # Create a new course object based on the received data
            new_course = Courses(
                code=data.get('code'),
                name=data.get('name'),
                description=data.get('description'),
                difficulty_rating=data.get('difficulty_rating'),
                level=data.get('level'),
                # Add other properties as needed
            )

            # Add the new course to the database
            db.session.add(new_course)
            db.session.commit()

            return show_201('New course added successfully')

        except Exception as e:
            # Rollback changes in case of an exception
            db.session.rollback()
            app.logger.exception(e)
            return show_500()
