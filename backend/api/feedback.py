from flask_restful import Resource
from flask_login import current_user
from flask import jsonify, request
from common.models import Feedback
from common.database import db
from common.helpers import role_required
from common.response_codes import show_200, show_201, show_400, show_401, show_403, show_404, show_500
from app import api

class CourseFeedbackResource(Resource):
    # GET method for retrieving feedback for a specific course
    def get(self, course_id):
        try:
            feedbacks = Feedback.get_all_feedback()

            if not feedbacks:
                return show_404('No feedbacks found for the course')

            feedbacks_data = [
                {
                    'id': feedback.id,
                    'poster': feedback.user.email,
                    'pic': feedback.user.pic,
                    'rating': feedback.rating,
                    'description': feedback.description,
                    'time': feedback.time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                }
                for feedback in feedbacks
            ]

            return show_200('Feedbacks found', {'feedbacks': feedbacks_data})

        except Exception as e:
            return show_500(str(e))

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
            return show_500(str(e))


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
            return show_500(str(e))

    # DELETE method for deleting feedback
    def delete(self, feedback_id):
        try:
            feedback = Feedback.get_feedback_by_id(feedback_id)

            if not feedback:
                return show_404('Feedback not found')

            # Check if the user has upvoted before deleting
            if current_user.id in [upvote.user.id for upvote in feedback.upvotes]:
                feedback.likes -= 1
                feedback.save()
                return show_200('Upvote deleted successfully')

            return show_403('User has not upvoted')

        except Exception as e:
            # Rollback changes in case of an exception
            db.session.rollback()
            return show_500(str(e))


# Define API routes for CourseFeedbackResource and FeedbackResource

