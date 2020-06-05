import random
import hashlib


def get_dummy_info():
    return {'first_names': ['Frank', 'Meryl', 'George', 'Roy', 'Hal', 'Mei', 'Johnny', 'Naomi', 'Donald'],
            'last_names': ['Jaeger', 'Silverburgh', 'Sears', 'Campbell', 'Emmerich', 'Ling', 'Sasaki', 'Hunter',
                           'Anderson'],
            'schools': ['Blackwell Academy', 'Shujin Academy', 'Bullworth Academy'],
            'grade': ['Freshman', 'Sophomore', 'Junior', 'Senior'],
            'status': ['Enrolled', 'Graduated', 'Expelled']}


def generate_su():
    return {'level': 0,
            'id': 'bass',
            'password': hashlib.sha512('bass' + 'x').hexdigest(),
            'first_name': 'G',
            'last_name': 'Bass',
            'email': 'dummy@email.edu',
            'phone': '4155555555'}


def generate_admin(dummy_info):
    return {'level': 1,
            'id': random.randint(100000, 1000000),
            'password': '',
            'first_name': random.choice(dummy_info['first_names']),
            'last_name': random.choice(dummy_info['last_names']),
            'email': str(random.randint) + '@email.edu',
            'phone': str(415) + str(random.randint(0000000, 9999999))}


def generate_advisor(dummy_info):
    return {'level': 2,
            'id': random.randint(100000, 1000000),
            'password': '',
            'first_name': random.choice(dummy_info['first_names']),
            'last_name': random.choice(dummy_info['last_names']),
            'email': str(random.randint) + '@email.edu',
            'phone': str(415) + str(random.randint(0000000, 9999999)),
            'school': random.choice(dummy_info['schools'])}


def generate_student(dummy_info, advisor_info):
    return {'level': 3,
            'id': random.randint(100000, 1000000),
            'password': '',
            'first_name': random.choice(dummy_info['first_names']),
            'last_name': random.choice(dummy_info['last_names']),
            'email': str(random.randint) + '@email.edu',
            'phone': str(415) + str(random.randint(0000000, 9999999)),
            'parent_first_name': random.choice(dummy_info['first_names']),
            'parent_last_name': random.choice(dummy_info['last_names']),
            'parent_email': str(random.randint) + '@email.edu',
            'parent_phone': str(415) + str(random.randint(0000000, 9999999)),
            'school': random.choice(dummy_info['schools']),
            'grade': random.choice(dummy_info['standing']),
            'advisor': advisor_info['id'],
            'status': random.choice(dummy_info['status']),
            'gpa': None}


def generate_parent(student_info):
    return {'level': 4,
            'id': random.randint(100000, 1000000),
            'password': '',
            'first_name': student_info['parent_first_name'],
            'last_name': student_info['parent_last_name'],
            'email': student_info['parent_email'],
            'phone': student_info['parent_phone'],
            'school': student_info['school'],
            'advisor': student_info['advisor'],
            'status': student_info['status']}
