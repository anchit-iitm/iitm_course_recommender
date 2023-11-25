from .database import db
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

roles_users = db.Table('user_roles',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), nullable = False),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
    )

Courses_Instructors = db.Table('courses_intructors',
        db.Column('user', db.Integer, db.ForeignKey('user.id'), nullable=False),
        db.Column('course', db.String(10), db.ForeignKey('courses.code')),
    )

class CompletedCourses(db.Model):
    __tablename__ = 'user_courses'    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    course_code = db.Column(db.String(10), db.ForeignKey('courses.code'), nullable=False, primary_key=True)
    marks = db.Column(db.Float, nullable=True)
    completed = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def has(cls, user_id, course_code):
        return cls.query.filter_by(user_id=user_id, course_code=course_code).first() is not None

    @classmethod
    def get(cls, user_id, course_code):
        return cls.query.filter_by(user_id=user_id, course_code=course_code).first()

Course_Prereqs = db.Table('courses_prereqs', 
        db.Column('course_code', db.String(10), db.ForeignKey('courses.code'), nullable=False, primary_key=True),
        db.Column('prereq_code', db.String(10), db.ForeignKey('courses.code'), primary_key=True)
    )

Course_Coreqs = db.Table('courses_coreqs', 
        db.Column('course_code', db.String(10), db.ForeignKey('courses.code'), nullable=False, primary_key=True),
        db.Column('coreq_code', db.String(10), db.ForeignKey('courses.code'), primary_key=True)
    )

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(55), nullable=False)
    email = db.Column(db.String(55), unique=True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    active = db.Column(db.Boolean(), nullable = False, default=True)

    pic = db.Column(db.String(500), nullable=True)
    max_subjects = db.Column(db.Integer, default=0)
    curr_deg_level = db.Column(db.String(10), nullable=True)
    ds_or_dp = db.Column(db.String(10), nullable=True)

    role = db.relationship('Role', secondary=roles_users, backref=db.backref('user'))
    created_at = db.Column(db.String(), default=func.now())
    completed_courses = db.relationship('CompletedCourses', primaryjoin = id==CompletedCourses.user_id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def has(cls, email):
        return cls.query.filter_by(email=email).first() is not None

    @classmethod
    def get_user_by_jwt(cls, jwt_identity):
        return cls.query.filter_by(id=jwt_identity).first()
    
    @classmethod
    def get_all_users_with_role(cls, roles = ['admin', 'ctm', 'im']):
        return cls.query.filter(cls.role.any(Role.role.in_(roles))).all()

    def __repr__(self):
        return f'{self.email}'

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key = True, autoincrement=True)
    role = db.Column(db.String(55), unique = True, nullable = False)
    description = db.Column(db.String(255), nullable = False)

    @classmethod
    def stu_role(cls):
        return cls.query.filter_by(role='student').first()
    
    @classmethod
    def admin_role(cls):
        return cls.query.filter_by(role='admin').first()
    
    @classmethod
    def get_role(cls, role):
        return cls.query.filter_by(role=role).first()

    def __repr__(self):
        return f'{self.role}'



class Courses(db.Model):
    __tablename__ = 'courses'
    code = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500))
    difficulty_rating = db.Column(db.Float, default=5)
    level = db.Column(db.String(10), nullable=False)
    dp_or_ds = db.Column(db.String(2), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    instructors = db.relationship('User', secondary=Courses_Instructors, backref=db.backref('courses'))

    FOUNDATION = 'foundation'
    DP = 'dp'
    DS = 'ds'
    BSC = 'bsc'
    BS = 'bs'

    pre_reqs = db.relationship('Courses', 
                            secondary = Course_Prereqs, 
                            primaryjoin = (Course_Prereqs.c.prereq_code == code),
                            secondaryjoin = (Course_Prereqs.c.course_code == code)                            
                            )
    
    co_reqs = db.relationship('Courses', 
                            secondary = Course_Coreqs, 
                            primaryjoin = (Course_Coreqs.c.coreq_code == code),
                            secondaryjoin = (Course_Coreqs.c.course_code == code)                            
                            )

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def has(cls, code):
        return cls.query.filter_by(code=code).first() is not None
    
    @classmethod
    def get_course_by_code(cls, code):
        return cls.query.filter_by(code=code).first()


class Recommendations(db.Model):
    __tablename__ = 'recommend'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course = db.Column(db.String(10), db.ForeignKey('courses.code'), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course = db.Column(db.String(10), db.ForeignKey('courses.code'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500))
    time = db.Column(db.String(), default=func.now())
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()