from flask_restful import Resource, abort
from flask import current_app as app
from flask import jsonify, request
from common.models import *
import math

from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_expects_json import expects_json

from common.response_codes import *
from common.helpers import role_required
from datetime import datetime

class CourseFeedbackResource(Resource):
    # GET method for retrieving feedback for a specific course
    def get(self, course_id):
        try:
            feedbacks = Feedback.get_feedback_by_course(course_id)

            if not feedbacks:                
                return make_response(jsonify([]), 200)
            
            feedbacks_data = [
                {
                    'id': feedback.id,
                    'poster': User.get_user_by_jwt(feedback.user).email,
                    # 'pic': feedback.user.pic,
                    'rating': feedback.rating,
                    'description': feedback.description,
                    'likes': feedback.likes,
                    'dislikes': feedback.dislikes,
                    'time': datetime.strptime(feedback.time, "%Y-%m-%d %H:%M:%S").strftime('%H:%M, %B %d, %Y')
                }
                for feedback in feedbacks
            ]

            return make_response(jsonify(feedbacks_data), 200)

        except Exception as e:
            app.logger.exception(e)
            return show_500()

    # POST method for adding feedback to a specific course
    @jwt_required()
    def post(self, course_id):
        try:
            current_user = get_jwt_identity()
            data = request.get_json()

            new_feedback = Feedback(
                user=current_user,
                course=course_id,
                rating=round(data.get('rating'), 1),
                description=data.get('description')
            )

            new_feedback.save()
            return show_201('New feedback added successfully')

        except Exception as e:
            # Rollback changes in case of an exception
            app.logger.exception(e)            
            return show_500()


class FeedbackResource(Resource):
    # GET method for adding upvote to a feedback
    @jwt_required()
    def get(self, feedback_id):
        try:
            current_user = get_jwt_identity()
            feedback = Feedback.get_feedback_by_id(feedback_id)

            if not feedback:
                return show_404('Feedback not found')
            
            # Check if the user has already upvoted
            if current_user.id not in [upvote.user.id for upvote in feedback.upvotes]:
                feedback.likes += 1
                feedback.save()
                return show_200('Upvote added successfully')

            return show_400('User has already upvoted')

        except Exception as e:
            return show_500()

    # DELETE method for deleting feedback
    @jwt_required()
    def delete(self, feedback_id):
        try:
            feedback = Feedback.get_feedback_by_id(feedback_id)

            if not feedback:
                return show_404("Feedback not found")
            
            # Check if the user has upvoted before deleting
            if feedback.user == get_jwt_identity():
                feedback.delete()                
                return show_200()
            else:
                return show_403("Not your feedback")

        except Exception as e:
            # Rollback changes in case of an exception
            db.session.rollback()
            return show_500()