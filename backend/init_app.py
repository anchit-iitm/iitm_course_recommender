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
allCtms = models.User.get_all_users_with_role(['ctm'])

for i in allCourses:
    i.instructors = random.sample(allCtms, random.randint(1, 10))
    i.save()

allStudents = models.User.get_all_users_with_role(['student'])


feedbacks = [
    "I really enjoyed using this application. It was easy to navigate, fast, and responsive. The design was sleek and modern, and the features were useful and intuitive. I especially liked the option to customize the settings and the notifications. The application met all my expectations and I would recommend it to anyone looking for a similar service.",
    "This application was disappointing and frustrating. It was slow, buggy, and crashed often. The design was outdated and cluttered, and the features were limited and confusing. I had trouble finding what I needed and the application did not offer any help or guidance. The application did not meet my needs and I would not use it again.",
    "This application was decent and satisfactory. It was not very impressive, but it did the job. The design was simple and plain, and the features were basic and standard. I did not encounter any major problems, but I also did not find anything remarkable. The application was average and I would use it if I had no other options.",
    "This application was amazing and impressive. It was fast, smooth, and reliable. The design was elegant and beautiful, and the features were innovative and smart. I loved the way the application adapted to my preferences and the situation. The application exceeded my expectations and I would use it all the time.",
    "This application was terrible and annoying. It was full of ads, pop-ups, and spam. The design was ugly and annoying, and the features were irrelevant and intrusive. I hated the way the application tried to force me to buy things or sign up for things. The application was a waste of time and I would uninstall it immediately.",
    "This application was good and helpful. It was not very exciting, but it was practical and useful. The design was clear and functional, and the features were relevant and helpful. I appreciated the way the application helped me with my tasks and goals. The application was reliable and I would use it regularly.",
    "This application was bad and useless. It was not what I expected or wanted. The design was misleading and deceptive, and the features were nonexistent or broken. I felt like the application was a scam or a joke. The application was a disappointment and I would ask for a refund.",
    "This application was great and fun. It was not very serious, but it was entertaining and enjoyable. The design was colorful and cheerful, and the features were amusing and creative. I liked the way the application made me laugh and smile. The application was a delight and I would use it for fun.",
    "This application was mediocre and boring. It was not very bad, but it was not very good either. The design was bland and generic, and the features were common and dull. I did not feel any emotion or interest while using the application. The application was forgettable and I would not use it much.",
    "This application was excellent and professional. It was not very flashy, but it was polished and refined. The design was sophisticated and classy, and the features were efficient and effective. I respected the way the application delivered high-quality results and performance. The application was outstanding and I would use it for work."
]

for i in allStudents:
    for j in random.sample(allCourses, random.randint(5,len(allCourses))):
        if len(j.pre_reqs) == 0 and len(j.co_reqs) == 0:
            isCompleted = random.choice([True, False])
            cc = models.CompletedCourses(user_id = i.id, course_code =j.code, completed=random.choice([True, False]), marks= random.randint(1,99) if isCompleted else None)
            cc.save()
    
            f = models.Feedback(    
                user = i.id,
                course = models.Courses.get_course_by_code(j.code).code,
                rating = random.randint(1,10),
                description = random.choice(feedbacks),
                likes = random.randint(1,100),
                dislikes = random.randint(1,25)
            )
            f.save()



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