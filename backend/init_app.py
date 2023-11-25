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

u1 = models.User(name="A Student", email="abc@xyz.com", role=[stu], pic="abcd.png", max_subjects=2, curr_deg_level="foundation", ds_or_dp="dp")
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


# cc = models.CompletedCourses(user_id = u1.id, course_code ="BSMA1001", completed=False)
# cc.save()

# cc2 = models.CompletedCourses(user_id = u1.id, course_code = "BSMA1002", marks=100, completed=True)
# cc2.save()

# cc = models.CompletedCourses(user_id = u1.id, course_code ="BSCS1001", completed=False)
# cc.save()

# cc = models.CompletedCourses(user_id = u1.id, course_code ="BSHS1001", completed=False)
# cc.save()