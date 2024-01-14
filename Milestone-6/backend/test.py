import pytest
import requests

BASE_URL = "http://localhost/api/v1"
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'

# Test Case 1
def test_1():
  #Auth token missing
  response = requests.get(f"{BASE_URL}/profile", headers={'Accept': 'application/json'})
  assert response.status_code == 401

# Test Case 2
def test_2():
  #All information required correct and present
  response = requests.get(f"{BASE_URL}/profile", headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 200

# Test Case 3
def test_3():
  #Profile
  #Post
  # All details required match and present
  input_dict={
  "pic": "ABCD.png",
  "maximum_courses_in_a_term": 3,
  "current_degree_level": "diploma",
  "dp_or_ds": "both",
  "current_courses": [
    "BSHS1001"
  ],
  "completed_courses": [
    {
      "id": "BSC2001",
      "marks": 87.9
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/profile", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 201

# Test Case 4
def test_4():
  #Profile
  #Get
  #User details do not exist
  response = requests.get(f"{BASE_URL}/profile",headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 404

def test_5():
  #profile
  # Get 
  #Get Wrong type of user logged in
  response = requests.get(f"{BASE_URL}/profile",headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 403

def test_6():
  #profile
  #post
  #Auth token missing
  input_dict={
  "pic": "ABCDE.png",
  "maximum_courses_in_a_term": 4,
  "current_degree_level": "diploma",
  "dp_or_ds": "both",
  "current_courses": [
    "BSHS1001"
  ],
  "completed_courses": [
    {
      "id": "BSC2001",
      "marks": 92
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/profile", data=data, headers={'Accept': 'application/json'})
  assert response.status_code == 401

def test_7():
    #profile
    #post
    #Wrong type of user logged in
  input_dict={
  "pic": "ABCD.png",
  "maximum_courses_in_a_term": 4,
  "current_degree_level": "diploma",
  "dp_or_ds": "both",
  "current_courses": [
    "BSHS1001"
  ],
  "completed_courses": [
    {
      "id": "BSC2001",
      "marks": 90
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/profile", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 403

def test_8():
    #profile
    #post
    #user auth does not exist
  input_dict={
  "pic": "ABCDE.png",
  "maximum_courses_in_a_term": 2,
  "current_degree_level": "diploma",
  "dp_or_ds": "both",
  "current_courses": [
    "BSHS1001"
  ],
  "completed_courses": [
    {
      "id": "BSC2001",
      "marks": 90
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/profile", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 404

def test_9():
    #profile
    #post
    #Course code uploaded in the 'current\_course' field does not exist in database
  input_dict={
  "pic": "ABCDE.png",
  "maximum_courses_in_a_term": 2,
  "current_degree_level": "diploma",
  "dp_or_ds": "both",
  "current_courses": [
    "BSHS1004"
  ],
  "completed_courses": [
    {
      "id": "BSC2001",
      "marks": 90
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/profile", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_10():
    #profile
    #post
    #Course code uploaded in the 'completed\_course' field does not exist in database
  input_dict={
  "pic": "ABCD.png",
  "maximum_courses_in_a_term": 3,
  "current_degree_level": "diploma",
  "dp_or_ds": "both",
  "current_courses": [
    "BSHS1001"
  ],
  "completed_courses": [
    {
      "id": "BSC2006",
      "marks": 87.9
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/profile", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_11():
    #profile
    #post
    #value in the 'maximum\_courses\_in\_a\_term' field less than 2
  input_dict={
  "pic": "ABCD.png",
  "maximum_courses_in_a_term": 1,
  "current_degree_level": "diploma",
  "dp_or_ds": "both",
  "current_courses": [
    "BSHS1001"
  ],
  "completed_courses": [
    {
      "id": "BSC2001",
      "marks": 87.9
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/profile", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_12():
    #profile
    #post
    #value in the 'maximum_courses_in_a_term' field greater than 4
  input_dict={
  "pic": "ABCD.png",
  "maximum_courses_in_a_term": 5,
  "current_degree_level": "diploma",
  "dp_or_ds": "both",
  "current_courses": [
    "BSHS1001"
  ],
  "completed_courses": [
    {
      "id": "BSC2001",
      "marks": 87.9
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/profile", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_13():
    #profile 
    #post
    #Invalid value in 'current_degree_level'
  input_dict={
  "pic": "ABCD.png",
  "maximum_courses_in_a_term": 3,
  "current_degree_level": "graduated",
  "dp_or_ds": "both",
  "current_courses": [
    "BSHS1001"
  ],
  "completed_courses": [
    {
      "id": "BSC2001",
      "marks": 87.9
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/profile", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_14():
    #profile
    #post
    #Invalid value in 'dp_or_ds'
  input_dict={
  "pic": "ABCD.png",
  "maximum_courses_in_a_term": 3,
  "current_degree_level": "diploma",
  "dp_or_ds": "dk",
  "current_courses": [
    "BSHS1001"
  ],
  "completed_courses": [
    {
      "id": "BSC2001",
      "marks": 87.9
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/profile", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_15():
    #profile
    #post
    #Course uploaded in the 'completed_course' field has marks less than 0
  input_dict={
  "pic": "ABCD.png",
  "maximum_courses_in_a_term": 3,
  "current_degree_level": "diploma",
  "dp_or_ds": "both",
  "current_courses": [
    "BSHS1001"
  ],
  "completed_courses": [
    {
      "id": "BSC2001",
      "marks": -9
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/profile", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_16():
    #profile
    #post
    #Course uploaded in the 'completed_course' field has marks more than 100
  input_dict={
  "pic": "ABCD.png",
  "maximum_courses_in_a_term": 3,
  "current_degree_level": "diploma",
  "dp_or_ds": "both",
  "current_courses": [
    "BSHS1001"
  ],
  "completed_courses": [
    {
      "id": "BSC2001",
      "marks": 130
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/profile", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_17():
    #profile
    #post
    #Course uploaded in the 'completed_course' field has marks missing
  input_dict={
  "pic": "ABCD.png",
  "maximum_courses_in_a_term": 3,
  "current_degree_level": "diploma",
  "dp_or_ds": "both",
  "current_courses": [
    "BSHS1001"
  ],
  "completed_courses": [
    {
      "id": "BSC2001"
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/profile", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_18():
    #profile
    #patch
    #All details required match and present
  input_dict={
  "maximum_courses_in_a_term": 4,
  "current_degree_level": "diploma",
  "dp_or_ds": "both",
  "current_courses": [
    "BSHS1001"
  ],
  "completed_courses": [
    {
      "id": "BSC2001",
      "marks": 99
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.patch(f"{BASE_URL}/profile", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 202

def test_19():
    #profile
    #patch
    #Auth token missing
  input_dict={
  "maximum_courses_in_a_term": 4,
  "current_degree_level": "diploma",
  "dp_or_ds": "both",
  "current_courses": [
    "BSHS1001"
  ],
  "completed_courses": [
    {
      "id": "BSC2001",
      "marks": 99
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.patch(f"{BASE_URL}/profile", data=data, headers={'Accept': 'application/json'})
  assert response.status_code == 401

def test_20():
    #profile
    #patch
    #Wrong type of user logged in
  input_dict={
  "maximum_courses_in_a_term": 4,
  "current_degree_level": "diploma",
  "dp_or_ds": "both",
  "current_courses": [
    "BSHS1001"
  ],
  "completed_courses": [
    {
      "id": "BSC2001",
      "marks": 99
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.patch(f"{BASE_URL}/profile", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 403

def test_21():
    #profile
    #patch
    #User Auth does not exist
  input_dict={
  "maximum_courses_in_a_term": 4,
  "current_degree_level": "diploma",
  "dp_or_ds": "both",
  "current_courses": [
    "BSHS1001"
  ],
  "completed_courses": [
    {
      "id": "BSC2001",
      "marks": 99
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.patch(f"{BASE_URL}/profile", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 404

def test_22():
    #admins
    #get
    #All required information correct and present
  response = requests.get(f"{BASE_URL}/admins",headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 200

def test_23():
    #admin
    #get
    #Auth token absent or invalid
  response = requests.get(f"{BASE_URL}/admins", headers={'Accept': 'application/json'})
  assert response.status_code == 401

def test_24():
    #admins
    #get
    #Auth token for wrong user type used
  response = requests.get(f"{BASE_URL}/admins", headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 403

def test_25():
    #admin
    #post
    #All information present and correct
  input_dict={
  "email": "IJKL@EFGH.com",
  "role": "im"
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/admins", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 201

def test_26():
    #admin
    #post
    #Syntax error in request
  input_dict={
  "emal": "IJKL@EFGH.com",
  "role": "im"
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/admins", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_27():
    #admin
    #post
    #Auth token missing or invalid
  input_dict={
  "email": "IJKL@EFGH.com",
  "role": "im"
    }
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/admins", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 401

def test_28():
    #admin
    #post
    #Auth token for worng user used
  input_dict={
  "email": "IJKL@EFGH.com",
  "role": "im"
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/admins", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 403

def test_29():
    #admin
    #post
    #Email in request not in database
  input_dict={
  "email": "abc@def.com",
  "role": "im"
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/admins", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_30():
    #admin
    #post
    #Email in request smaller than 3 characters
  input_dict={
  "email": "a@b",
  "role": "im"
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/admins", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_31():
    #admin
    #post
    #role in request invalid
  input_dict={
  "email": "IJKL@EFGH.com",
  "role": "stu"
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/admins", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_32():
    #admin
    #post
    # role or email field in request missing
  input_dict={
  "email": "IJKL@EFGH.com"
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/admins", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_33():
    #admin
    #patch
    #Syntax error in request
  input_dict={
  "eml": "IJKL@EFGH.com",
  "role": "im"
}
  data = json.dumps(input_dict)
  response = requests.patch(f"{BASE_URL}/admins", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_34():
    #admin
    #patch
    # Auth token missing or invalid
  input_dict={
  "email": "IJKL@EFGH.com",
  "role": "im"
}
  data = json.dumps(input_dict)
  response = requests.patch(f"{BASE_URL}/admins", data=data, headers={'Accept': 'application/json'})
  assert response.status_code == 401

def test_35():
    #admin
    #patch
    #Auth token for wrong type of user used
  input_dict={
  "email": "IJKL@EFGH.com",
  "role": "im"
}
  data = json.dumps(input_dict)
  response = requests.patch(f"{BASE_URL}/admins", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 403

def test_36():
    #admin
    #patch
    #email for which data is being patched does not exist
  input_dict={
  "email": "abc@def.com",
  "role": "im"
}
  data = json.dumps(input_dict)
  response = requests.patch(f"{BASE_URL}/admins", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_37():
    #admin
    #patch
    #role in request invalid
  input_dict={
  "email": "IJKL@EFGH.com",
  "role": "i"
}
  data = json.dumps(input_dict)
  response = requests.patch(f"{BASE_URL}/admins", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_38():
    #admin
    #patch
    #role or email field in request missing
  input_dict={
  "email": "IJKL@EFGH.com",
}
  data = json.dumps(input_dict)
  response = requests.patch(f"{BASE_URL}/admins", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_39():
  #admin
  #delete
  #All fields present and correct
  response = requests.delete(f"{BASE_URL}/admins?email=IJKL%40EFGH.com",headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 200

def test_40():
  #admin
  #delete
  #Syntax error in request
  response = requests.delete(f"{BASE_URL}/admins?emai=IJKL%40EFGH.com", headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_41():
  #admin
  #delete
  # Auth token missing or invalid
  response = requests.delete(f"{BASE_URL}/admins?email=IJKL%40EFGH.com", headers={'Accept': 'application/json'})
  assert response.status_code == 401

def test_42():
  #admin
  #delete
  #Auth token for wrong type of user used
  response = requests.delete(f"{BASE_URL}/admins?email=IJKL%40EFGH.com",headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 403

def test_43():
  #admin
  #delete
  #email for which data is being deleted does not exist
  response = requests.delete(f"{BASE_URL}/admins?email=abc%40def.com",headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_44():
  #admin
  #delete
  #email field in request missing
  response = requests.delete(f"{BASE_URL}/admins", headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_45():
  #admin
  #delete
  #email field in request has less than 3 characters
  response = requests.delete(f"{BASE_URL}/admins?email=IJK", headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_46():
  #auth
  #post
  #All required inputs present and valid
  input_dict={
  "email": "abc@xyz.com",
  "password": "abcdef",
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/user/auth", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 200

def test_47():
  #auth
  #post
  #Invalid email
  input_dict={
  "email": "abc@def.com",
  "password": "abcdef",
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/user/auth", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_48():
  #auth
  #post
  #Wrong password
  input_dict={
  "email": "abc@xyz.com",
  "password": "wrong",
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/user/auth", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_49():
  #auth
  #post
  #Wrong request syntax
  input_dict={
  "ema": "abc@xyz.com",
  "password": "abcdef",
  }
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/user/auth", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_50():
  #register
  #post
  #All fields present and correct
  input_dict={
  "name": "New Student",
  "email": "new@stu.com",
  "password": "newstu"
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/user/auth/register", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 201

def test_51():
  #register
  #post
  #Invalid request syntax
  input_dict={
  "n": "New Student",
  "email": "new@stu.com",
  "password": "newstu"
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/user/auth/register", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_52():
  #register
  #post
  #Email already exists in database
  input_dict={
  "name": "New Student",
  "email": "abc@xyz.com",
  "password": "newstu"
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/user/auth/register", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_53():
  #register
  #post
  #Name smaller than 5 letters in request
  input_dict={
  "name": "New",
  "email": "new@stu.com",
  "password": "newstu"
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/user/auth/register", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_54():
  #register
  #post
  #Name larger than 55 letters in request
  long_name='*****'
  input_dict={
  "name": f"{long_name}",
  "email": "new@stu.com",
  "password": "newstu"
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/user/auth/register", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_55():
  #register
  #post
  #Email larger than 55 letters in request
  long_mail='*****'
  input_dict={
  "name": "New Student",
  "email": f"{long_mail}",
  "password": "newstu"
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/user/auth/register", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_56():
  #register
  #post
  #Password smaller than 5 letters in request
  input_dict={
  "name": "New Student",
  "email": "abc@xyz.com",
  "password": "n"
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/user/auth/register", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_57():
  #recommender
  #get
  #All inputs present and valid
  response = requests.get(f"{BASE_URL}/recommendation",headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 200

def test_58():
  #recommender
  #get
  #Invalid or missing auth token
  response = requests.get(f"{BASE_URL}/recommendation", headers={'Accept': 'application/json'})
  assert response.status_code == 401

def test_59():
  #Recommender
  #get
  #Wrong type of user auth sent
  response = requests.get(f"{BASE_URL}/recommender", headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 403

def test_60():
  #Courses
  #get
  #All required fields present and correct
  response = requests.get(f"{BASE_URL}/course/BSC2001", headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 200

def test_61():
  #courses
  #get
  #Syntax error in request
  response = requests.get(f"{BASE_URL}/cours/BSC2001", headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_62():
  #courses
  #get
  #Auth token missing or invalid
  response = requests.get(f"{BASE_URL}/course/BSC2001",headers={'Accept': 'application/json'})
  assert response.status_code == 401

def test_63():
  #courses
  #get
  #ID in request does not exist
  response = requests.get(f"{BASE_URL}/course/BSC20", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 404

def test_64():
  #courses
  #patch
  # All required fields present and correct
  input_dict={
  "name": "Course 1",
  "description": "This is course 1",
  "level": "Degree",
  "dp_or_ds": "dp",
  "credits": 3,
  "pre_req": [
    "BSC2001",
    "BSC2002"
  ],
  "co_req": [
    "BSC2001",
    "BSC2002"
  ],
  "availability": [
    "Sept2022",
    "March2002"
  ],
  "instructors": [
    {
      "name": "ABCD",
      "email": "ABCD@efgh.com"
    },
    {
      "name": "EFGH",
      "email": "ijkl@efgh.com"
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.patch(f"{BASE_URL}/course/BSC2002", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 201

def test_65():
  #course
  #patch
  #Syntax error in request
  input_dict={
  "na": "Course 1",
  "description": "This is course 1",
  "level": "Degree",
  "dp_or_ds": "dp",
  "credits": 3,
  "pre_req": [
    "BSC2001",
    "BSC2002"
  ],
  "co_req": [
    "BSC2001",
    "BSC2002"
  ],
  "availability": [
    "Sept2022",
    "March2002"
  ],
  "instructors": [
    {
      "name": "ABCD",
      "email": "ABCD@efgh.com"
    },
    {
      "name": "EFGH",
      "email": "ijkl@efgh.com"
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.patch(f"{BASE_URL}/course/BSC2002", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_66():
  #courses
  #patch
  #Auth token missing or invalid
  input_dict={
  "name": "Course 1",
  "description": "This is course 1",
  "level": "Degree",
  "dp_or_ds": "dp",
  "credits": 3,
  "pre_req": [
    "BSC2001",
    "BSC2002"
  ],
  "co_req": [
    "BSC2001",
    "BSC2002"
  ],
  "availability": [
    "Sept2022",
    "March2002"
  ],
  "instructors": [
    {
      "name": "ABCD",
      "email": "ABCD@efgh.com"
    },
    {
      "name": "EFGH",
      "email": "ijkl@efgh.com"
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.patch(f"{BASE_URL}/course/BSC2002", data=data, headers={'Accept': 'application/json'})
  assert response.status_code == 401

def test_67():
  #courses
  #patch
  #Sent Auth of wrong user type
  input_dict={
  "name": "Course 1",
  "description": "This is course 1",
  "level": "Degree",
  "dp_or_ds": "dp",
  "credits": 3,
  "pre_req": [
    "BSC2001",
    "BSC2002"
  ],
  "co_req": [
    "BSC2001",
    "BSC2002"
  ],
  "availability": [
    "Sept2022",
    "March2002"
  ],
  "instructors": [
    {
      "name": "ABCD",
      "email": "ABCD@efgh.com"
    },
    {
      "name": "EFGH",
      "email": "ijkl@efgh.com"
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.patch(f"{BASE_URL}/course/BSC2002", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 403

def test_68():
  #courses
  #patch
  #Course Id does not exist in system
  input_dict={
  "name": "Course 1",
  "description": "This is course 1",
  "level": "Degree",
  "dp_or_ds": "dp",
  "credits": 3,
  "pre_req": [
    "BSC2001",
    "BSC2002"
  ],
  "co_req": [
    "BSC2001",
    "BSC2002"
  ],
  "availability": [
    "Sept2022",
    "March2002"
  ],
  "instructors": [
    {
      "name": "ABCD",
      "email": "ABCD@efgh.com"
    },
    {
      "name": "EFGH",
      "email": "ijkl@efgh.com"
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.patch(f"{BASE_URL}/course/BSC20", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 404

def test_69():
  #course
  #delete
  #All required fields present and correct
  response = requests.delete(f"{BASE_URL}/course/BSC2001",headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 200

def test_70():
  #course
  #delete
  #Syntax error in request
  response = requests.delete(f"{BASE_URL}/coure/BSC2001",headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_71():
  #course
  #delete
  #Auth token missing or invalid
  response = requests.delete(f"{BASE_URL}/course/BSC2001",headers={'Accept': 'application/json'})
  assert response.status_code == 401

def test_72():
  #course
  #delete
  #Sent Auth of wrong user type
  response = requests.delete(f"{BASE_URL}/course/BSC2001",headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 403

def test_73():
  #course
  #delete
  #Course Id does not exist in system
  response = requests.delete(f"{BASE_URL}/course/BSC20",headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 201

def test_74():
  #course
  #get all
  #All required fields present and correct
  response = requests.get(f"{BASE_URL}/courses",headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 200

def test_75():
  #courses
  #get all
  #Auth token missing or invalid
  response = requests.get(f"{BASE_URL}/courses",headers={'Accept': 'application/json'})
  assert response.status_code == 401

def test_76():
  #courses
  #get all
  #Sent Auth of wrong user type
  response = requests.get(f"{BASE_URL}/courses",headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 403

def test_77():
  #courses
  #get all
  #No courses in the system
  response = requests.get(f"{BASE_URL}/courses", headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 404

def test_78():
  #courses 
  #post
  #All required fields present and correct
  input_dict={
  "code": "BSC2001",
  "name": "Course 1",
  "description": "This is course 1",
  "level": "Degree",
  "dp_or_ds": "dp",
  "credits": 4,
  "pre_req": [
    "BSC2001",
    "BSC2002"
  ],
  "co_req": [
    "BSC2001",
    "BSC2002"
  ],
  "availability": [
    "Sept2022",
    "March2002"
  ],
  "instructors": [
    {
      "name": "ABCD",
      "email": "ABCD@efgh.com"
    },
    {
      "name": "EFGH",
      "email": "ijkl@efgh.com"
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/courses", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 201

def test_79():
  #courses
  #post
  #Auth token missing or invalid
  input_dict={
  "code": "BSC2001",
  "name": "Course 1",
  "description": "This is course 1",
  "level": "Degree",
  "dp_or_ds": "dp",
  "credits": 4,
  "pre_req": [
    "BSC2001",
    "BSC2002"
  ],
  "co_req": [
    "BSC2001",
    "BSC2002"
  ],
  "availability": [
    "Sept2022",
    "March2002"
  ],
  "instructors": [
    {
      "name": "ABCD",
      "email": "ABCD@efgh.com"
    },
    {
      "name": "EFGH",
      "email": "ijkl@efgh.com"
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/courses", data=data, headers={'Accept': 'application/json'})
  assert response.status_code == 401

def test_80():
  #course
  #post
  #Sent Auth of wrong user type
  input_dict={
  "code": "BSC2001",
  "name": "Course 1",
  "description": "This is course 1",
  "level": "Degree",
  "dp_or_ds": "dp",
  "credits": 4,
  "pre_req": [
    "BSC2001",
    "BSC2002"
  ],
  "co_req": [
    "BSC2001",
    "BSC2002"
  ],
  "availability": [
    "Sept2022",
    "March2002"
  ],
  "instructors": [
    {
      "name": "ABCD",
      "email": "ABCD@efgh.com"
    },
    {
      "name": "EFGH",
      "email": "ijkl@efgh.com"
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/courses", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 403

def test_81():
  #course
  #post
  #Syntax error in request
  input_dict={
  "coe": "BSC2001",
  "name": "Course 1",
  "description": "This is course 1",
  "level": "Degree",
  "dp_or_ds": "dp",
  "credits": 4,
  "pre_req": [
    "BSC2001",
    "BSC2002"
  ],
  "co_req": [
    "BSC2001",
    "BSC2002"
  ],
  "availability": [
    "Sept2022",
    "March2002"
  ],
  "instructors": [
    {
      "name": "ABCD",
      "email": "ABCD@efgh.com"
    },
    {
      "name": "EFGH",
      "email": "ijkl@efgh.com"
    }
  ]
}
  data = json.dumps(input_dict)
  response = requests.post(f"{BASE_URL}/courses", data=data, headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 400

def test_82():
  #Feedback
  #get
  #All required fields present and correct
  response = requests.get(f"{BASE_URL}/course/BSC2001/feedback",headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 200

def test_83():
  #Feedback
  #get
  #Sent Auth token of wrong user type
  response = requests.get(f"{BASE_URL}/course/BSC2001/feedback",headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 403

def test_84():
  #Feedback
  #get
  #Auth token missing or invalid
  response = requests.get(f"{BASE_URL}/course/BSC2001/feedback", headers={'Accept': 'application/json'})
  assert response.status_code == 401

def test_85():
  #feedback
  #get
  #Id in request does not exist
  response = requests.get(f"{BASE_URL}/course/BSC2006/feedback",headers={'Accept': 'application/json', 'Authorization': f"Bearer {token}"})
  assert response.status_code == 404



