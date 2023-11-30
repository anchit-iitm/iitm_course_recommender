from flask_restful import Resource, reqparse
from flask import jsonify, request
from common.models import Courses, User
from common.database import db
from common.helpers import role_required
from common.response_codes import show_200, show_201, show_400, show_401, show_403, show_404, show_500
from app import api

class CourseResource(Resource):
    # GET method for retrieving a single course by ID
    def get(self, id):
        try:
            # Query the database for the course with the specified ID
            course = Courses.query.get(id)

            if not course:
                return show_404('Course not found')

            # Format course data for response
            course_data = {
                'id': course.code,
                'name': course.name,
                'description': course.description,
                'difficulty_rating': course.difficulty_rating,
                'level': course.level,
                'pre_req': [prerequisite.code for prerequisite in course.pre_requisites],
                'co_req': [corequisite.code for corequisite in course.co_requisites],
                'availability': [availability for availability in course.availability],
                'instructors': [
                    {'name': instructor.name, 'email': instructor.email}
                    for instructor in course.instructors
                ]
            }

            return show_200('Course found', {'course': course_data})

        except Exception as e:
            return show_500(str(e))

    # PATCH method for modifying a single course by ID
    @role_required('admin')
    def patch(self, id):
        try:
            # Query the database for the course with the specified ID
            course = Courses.query.get(id)

            if not course:
                return show_404('Course not found')

            # Parse the JSON data from the request
            data = request.get_json()

            # Update the course properties based on the received data
            course.name = data.get('name', course.name)
            course.description = data.get('description', course.description)
            course.level = data.get('level', course.level)
            # Update other properties as needed

            # Commit the changes to the database
            db.session.commit()

            return show_200('Course information modified successfully')

        except Exception as e:
            # Rollback changes in case of an exception
            db.session.rollback()
            return show_500(str(e))

    # DELETE method for deleting a single course by ID
    @role_required('admin')
    def delete(self, id):
        try:
            # Query the database for the course with the specified ID
            course = Courses.query.get(id)

            if not course:
                return show_404('Course not found')

            # Delete the course from the database
            db.session.delete(course)
            db.session.commit()

            return show_200('Course deleted successfully')

        except Exception as e:
            # Rollback changes in case of an exception
            db.session.rollback()
            return show_500(str(e))

# Resource for handling multiple courses
class CoursesResource(Resource):
    # GET method for retrieving all courses
    def get(self):
        try:
            # Query the database for all courses
            courses = Courses.query.all()

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
                    'pre_req': [prerequisite.code for prerequisite in course.pre_requisites],
                    'co_req': [corequisite.code for corequisite in course.co_requisites],
                    'availability': [availability for availability in course.availability],
                    'instructors': [
                        {'name': instructor.name, 'email': instructor.email}
                        for instructor in course.instructors
                    ]
                }
                for course in courses
            ]

            return show_200('Courses found', {'courses': courses_data})

        except Exception as e:
            return show_500(str(e))

    # POST method for adding a new course
    @role_required('admin')
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
            return show_500(str(e))

# Define API routes for CourseResource and CoursesResource
api.add_resource(CourseResource, '/courses/<int:id>')
api.add_resource(CoursesResource, '/courses')
