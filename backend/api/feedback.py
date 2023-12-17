from flask_restful import Resource, abort
from flask import current_app as app
from flask import jsonify, request
from common.models import *

from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_expects_json import expects_json

from common.response_codes import *
from common.helpers import role_required

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
                    'dislikes': feedback.dislikes
                    # 'time': feedback.time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                }
                for feedback in feedbacks
            ]

            return make_response(jsonify(feedbacks_data), 200)

        except Exception as e:
            app.logger.exception(e)
            return show_500()

    # POST method for adding feedback to a specific course
    def post(self, course_id):
        try:
            data = request.get_json()

            new_feedback = Feedback(
                user=current_user,
                course_id=course_id,
                rating=data.get('rating'),
                description=data.get('description')
            )

            db.session.add(new_feedback)
            db.session.commit()

            return show_201('New feedback added successfully')

        except Exception as e:
            # Rollback changes in case of an exception
            db.session.rollback()
            return show_500()


class FeedbackResource(Resource):
    # GET method for adding upvote to a feedback
    def get(self, feedback_id):
        try:
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
    def delete(self, feedback_id):
        try:
            feedback = Feedback.get_feedback_by_id(feedback_id)

            if not feedback:
                abort(404, 'Feedback not found')

            # Check if the user has upvoted before deleting
            if current_user.id in [upvote.user.id for upvote in feedback.upvotes]:
                feedback.likes -= 1
                feedback.save()
                return show_200('Upvote deleted successfully')

            return show_403('User has not upvoted')

        except Exception as e:
            # Rollback changes in case of an exception
            db.session.rollback()
            return show_500()