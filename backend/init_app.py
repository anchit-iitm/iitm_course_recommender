import os
# creates log directory if not present
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)

from app import create_app
from common.database import db
from common import models
from common.helpers import add_bulk_from_csv

db.session.commit()
db.drop_all()
db.create_all()

admin = models.Role(role="admin", description="superadmin of the app")
ctm = models.Role(role="ctm", description="Course Team Member")
im = models.Role(role="im", description="Management")
stu = models.Role(role="student", description="Student")

db.session.add(admin)
db.session.add(ctm)
db.session.add(im)
db.session.add(stu)
db.session.commit()

add_bulk_from_csv("./db_raw/courses.csv")

users = [
    ("Anhat Singh", "anhatsingh@gmail.com", admin),
    ("Jasleen Kaur", "jasleenkaur@gmail.com", ctm),
    ("Oza Jay", "ozajay@gmail.com", im),
    ("Anchit Mandal", "anchitmandal@gmail.com", stu),
    ("Rohit Londhe", "rohitlondhe@gmail.com", stu),
    
    ("Akhil Aggarwal", "akhil@gmail.com", admin),
    ("Anu Sharma", "anu@gmail.com", ctm),
    ("Abhinoor Singh", "abhinoor@gmail.com", im),
    ("Harnoor Kaur", "harnoor@gmail.com", stu),
    ("Guramanat Singh", "guramanat@gmail.com", admin),
    ("PPD", "ppd@gmail.com", ctm),
    ("A stupid person", "stoopid@gmail.com", im),
]

for i in users:
    x = models.User(name = i[0], email=i[1], role=[i[2]])
    x.set_password("abcd")
    x.save()

u1 = models.User(name="A Student", email="abc@xyz.com", role=[stu], pic="abcd.png", max_subjects=2, curr_deg_level="foundation", ds_or_dp="both")
u1.set_password("abcd")
u1.save()

u2 = models.User(name="An Admin", email="admin@xyz.com", role=[admin])
u2.set_password("abcd")
u2.save()

u3 = models.User(name="A CTM", email="ctm@xyz.com", role=[ctm])
u3.set_password("abcd")
u3.save()

u4 = models.User(name="An IM", email="im@xyz.com", role=[im])
u4.set_password("abcd")
u4.save()


c = models.Courses.get_all_courses()[0]
c.instructors = [u3]
c.save()

cc = models.CompletedCourses(user_id = u1.id, course_code ="BSMA1001", completed=True, marks=50)
cc.save()

cc2 = models.CompletedCourses(user_id = u1.id, course_code = "BSMA1002", completed=False)
cc2.save()

f = models.Feedback(    
    user = u1.id,
    course = models.Courses.get_course_by_code("BSCS1001").code,
    rating = 9.1,
    description = "Very Difficult Course",
    likes = 10,
    dislikes = 1
)

f.save()
    

# cc = models.CompletedCourses(user_id = u1.id, course_code ="BSCS1001", completed=False)
# cc.save()

# cc = models.CompletedCourses(user_id = u1.id, course_code ="BSHS1001", completed=False)
# cc.save()