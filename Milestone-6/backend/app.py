import os, logging

from flask import Flask, render_template, abort
from logging.config import dictConfig
from flask_restful import Api
from flask_jwt_extended import JWTManager

from common.database import db
from common.config import LocalDev


# set the configurations for the log file
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s | %(module)s >>> %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "logs/flask.log",
                "formatter": "default",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console", "file"]},
    }
)

# set app = None to initialize variable
app = None
api = None
jwt = None

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='assets')
    app.config.from_object(LocalDev)

    db.init_app(app)
    app.app_context().push()
    app.logger.info('Database plugin initialized')

    api = Api(app)
    app.app_context().push()
    app.logger.info('API plugin initialized')

    jwt = JWTManager(app)
    app.app_context().push()
    app.logger.info('JWT Manager initialized')

    app.logger.info('App setup complete.')

    return app, api, jwt


app, api_handler, jwt = create_app()

import api.auth
from api.profile import Student
from api.admin import SuperAdmin
from api.recommender import Recommender
from api.feedback import CourseFeedbackResource, FeedbackResource
from api.student import AllStudents
from api.course import CourseResource, CoursesResource
from api.statistics import GeneralStatistics

api_handler.add_resource(AllStudents, "/api/v1/student/all")
api_handler.add_resource(Student, "/api/v1/profile")
api_handler.add_resource(SuperAdmin, "/api/v1/admin")
api_handler.add_resource(Recommender, "/api/v1/recommender")
api_handler.add_resource(CourseFeedbackResource, '/api/v1/course/<string:course_id>/feedback')
api_handler.add_resource(FeedbackResource, '/api/v1/feedback/<int:feedback_id>')
api_handler.add_resource(CoursesResource, '/api/v1/courses/all')
api_handler.add_resource(CourseResource, '/api/v1/courses/<string:id>')
api_handler.add_resource(GeneralStatistics, '/api/v1/stats/general')

@app.route('/')
def home():
    try:        
        return render_template('index.html')
    except:
        app.logger.exception("error occurred")
        abort(500)

if __name__ == '__main__':
    app.run()