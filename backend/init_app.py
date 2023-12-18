import os, random
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

no_students = 100
no_ctms = 20
no_im = 5

students = [
    ("An Amazing Student", "abc@xyz.com")
] + [(f"Student {i}", f"student{i}@gmail.com") for i in range(no_students)]
admins = [
    ("An XYZ Admin", "admin@xyz.com"),
    ("An XYZ Gmail Admin", "xyz@gmail.com"),
    ("Anhat Singh", "anhatsingh@gmail.com"),
    ("Akhil Aggarwal", "akhil@gmail.com"),
    ("Guramanat Singh", "guramanat@gmail.com"),
    ("Harnoor Kaur", "harnoor@gmail.com"),
]

ctms = [
    ("Jasleen Kaur", "jasleenkaur@gmail.com"),
    ("Anu Sharma", "anu@gmail.com"),
] + [(f"CTM {i}", f"ctm{i}@gmail.com") for i in range(no_ctms)]

ims = [
    ("Oza Jay", "ozajay@gmail.com"),
    ("Abhinoor Singh", "abhinoor@gmail.com"),
    ("A stupid person", "stoopid@gmail.com"),
] + [(f"IM {i}", f"im{i}@gmail.com") for i in range(no_im)]

for i in students:
    x = models.User(name = i[0], email=i[1], role=[stu], pic="abcd.png", max_subjects=random.choice([2,3,4]), curr_deg_level=random.choice(["foundation", "diploma", "degree"]), ds_or_dp=random.choice(["ds", "dp", "both"]))
    x.set_password("abcd")
    x.save()

for i in admins:
    x = models.User(name = i[0], email=i[1], role=[admin])
    x.set_password("abcd")
    x.save()

for i in ctms:
    x = models.User(name = i[0], email=i[1], role=[ctm])
    x.set_password("abcd")
    x.save()

for i in ims:
    x = models.User(name = i[0], email=i[1], role=[im])
    x.set_password("abcd")
    x.save()


allCourses = models.Courses.get_all_courses()
allCtms = models.User.get_all_users_with_role('ctm')

for i in allCourses:
    i.instructors = random.sample(allCtms, random.randint(1, 10))
    i.save()

allStudents = models.User.get_all_users_with_role('student')

for i in allStudents:
    pass

# u1 = models.User(name="A Student", email="abc@xyz.com", role=[stu], pic="abcd.png", max_subjects=2, curr_deg_level="foundation", ds_or_dp="both")
# u1.set_password("abcd")
# u1.save()

# u3 = models.User(name="A CTM", email="ctm@xyz.com", role=[ctm])
# u3.set_password("abcd")
# u3.save()

# u4 = models.User(name="An IM", email="im@xyz.com", role=[im])
# u4.set_password("abcd")
# u4.save()


# c = models.Courses.get_all_courses()[0]
# c.instructors = [u3]
# c.save()

# cc = models.CompletedCourses(user_id = u1.id, course_code ="BSMA1001", completed=True, marks=50)
# cc.save()

# cc2 = models.CompletedCourses(user_id = u1.id, course_code = "BSMA1002", completed=False)
# cc2.save()

# f = models.Feedback(    
#     user = u1.id,
#     course = models.Courses.get_course_by_code("BSCS1001").code,
#     rating = 9.1,
#     description = "Very Difficult Course",
#     likes = 10,
#     dislikes = 1
# )

# f.save()
    

# cc = models.CompletedCourses(user_id = u1.id, course_code ="BSCS1001", completed=False)
# cc.save()

# cc = models.CompletedCourses(user_id = u1.id, course_code ="BSHS1001", completed=False)
# cc.save()