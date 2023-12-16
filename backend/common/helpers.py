from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request
from common.response_codes import *
from common.models import Courses


# Here is a custom decorator that verifies the JWT is present in the request,
# as well as insuring that the JWT has a claim indicating that this user is
# an administrator
def role_required(role):
    def wrapper(fn):
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] == role:
                return fn(*args, **kwargs)
            else:
                return show_403()
        return decorator
    return wrapper


import pandas as pd

def add_bulk_from_csv(csv_file_abs_path):
    df = pd.read_csv(csv_file_abs_path)

    for index, row in df.iterrows():
        cx = Courses(
            code = row['code'],
            name = row['name'],
            description = row['description'],
            level = row['level'],
            dp_or_ds = row['dp_or_ds'],
            credits = row['credits']
        )
        prereq_codes_list = map(str.strip, row['prereqs'].split(',')) if row['prereqs'].strip() != "-" else None
        coreq_codes_list = map(str.strip, row['coreqs'].split(',')) if row['coreqs'].strip() != "-" else None

        if prereq_codes_list:
            for a_prereq_code in prereq_codes_list:
                c = Courses.get_course_by_code(a_prereq_code)
                cx.pre_reqs.append(c)
        
        if coreq_codes_list:
            for a_coreq_code in coreq_codes_list:
                c = Courses.get_course_by_code(a_coreq_code)
                cx.co_reqs.append(c)

        cx.save()