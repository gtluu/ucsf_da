import random
import string
import hashlib
import flask
from flaskext.mysql import MySQL


def get_dummy_info():
    return {'first_names': ['Frank', 'Meryl', 'George', 'Roy', 'Hal', 'Mei', 'Johnny', 'Naomi', 'Donald'],
            'last_names': ['Jaeger', 'Silverburgh', 'Sears', 'Campbell', 'Emmerich', 'Ling', 'Sasaki', 'Hunter',
                           'Anderson'],
            'schools': ['Blackwell Academy', 'Shujin Academy', 'Bullworth Academy'],
            'grade': ['Freshman', 'Sophomore', 'Junior', 'Senior'],
            'status': ['Enrolled', 'Graduated', 'Expelled']}


def generate_su():
    pass


def generate_admin(mysql, dummy_info):
    con = mysql.connect()
    cur = con.cursor()

    cur.execute('SELECT id FROM admins UNION SELECT id FROM advisors UNION SELECT id FROM students UNION SELECT id FROM parents;')
    id_list = cur.fetchall()
    id_list = [int(i[0]) for i in id_list]

    id = str(random.randint(100000, 1000000))
    while id in id_list:
        id = str(random.randint(100000, 1000000))
    first_name = '"' + random.choice(dummy_info['first_names']) + '"'
    middle_name = '"' + random.choice(string.ascii_letters[26:]) + '"'
    last_name = '"' + random.choice(dummy_info['last_names']) + '"'
    email = '"' + str(random.randint(100000, 1000000)) + '@email.edu' + '"'
    cell_phone = '"' + str(415) + str(random.randint(0000000, 9999999)) + '"'
    work_phone = '"' + str(415) + str(random.randint(0000000, 9999999)) + '"'
    home_phone = '"' + str(415) + str(random.randint(0000000, 9999999)) + '"'
    values = (id, first_name, middle_name, last_name, email, cell_phone, work_phone, home_phone)

    query = 'INSERT INTO admins '
    columns = '(id, first_name, middle_name, last_name, email, cell_phone, work_phone, home_phone)'
    query += columns + ' VALUES (' + ', '.join(values) + ');'

    cur.execute(query)
    con.commit()
    cur.close()


def generate_advisor(mysql, dummy_info):
    con = mysql.connect()
    cur = con.cursor()

    cur.execute('SELECT id FROM admins UNION SELECT id FROM advisors UNION SELECT id FROM students UNION SELECT id FROM parents;')
    id_list = cur.fetchall()
    id_list = [int(i[0]) for i in id_list]

    id = str(random.randint(100000, 1000000))
    while id in id_list:
        id = str(random.randint(100000, 1000000))
    first_name = '"' + random.choice(dummy_info['first_names']) + '"'
    middle_name = '"' + random.choice(string.ascii_letters[26:]) + '"'
    last_name = '"' + random.choice(dummy_info['last_names']) + '"'
    email = '"' + str(random.randint(100000, 1000000)) + '@email.edu' + '"'
    cell_phone = '"' + str(415) + str(random.randint(0000000, 9999999)) + '"'
    work_phone = '"' + str(415) + str(random.randint(0000000, 9999999)) + '"'
    home_phone = '"' + str(415) + str(random.randint(0000000, 9999999)) + '"'
    school = '"' + random.choice(dummy_info['schools']) + '"'
    values = (id, first_name, middle_name, last_name, email, cell_phone, work_phone, home_phone, school)

    query = 'INSERT INTO advisors '
    columns = '(id, first_name, middle_name, last_name, email, cell_phone, work_phone, home_phone, school)'
    query += columns + ' VALUES (' + ', '.join(values) + ');'

    cur.execute(query)
    con.commit()
    cur.close()


def generate_parent(mysql, dummy_info, student_id, parent_id):
    first_name = '"' + random.choice(dummy_info['first_names']) + '"'
    middle_name = '"' + random.choice(string.ascii_letters[26:]) + '"'
    last_name = '"' + random.choice(dummy_info['last_names']) + '"'
    email = '"' + str(random.randint(100000, 1000000)) + '@email.edu' + '"'
    cell_phone = '"' + str(415) + str(random.randint(0000000, 9999999)) + '"'
    work_phone = '"' + str(415) + str(random.randint(0000000, 9999999)) + '"'
    home_phone = '"' + str(415) + str(random.randint(0000000, 9999999)) + '"'

    values = (parent_id, first_name, middle_name, last_name, email, cell_phone, work_phone, home_phone, student_id)

    con = mysql.connect()
    cur = con.cursor()

    query = 'INSERT INTO parents '
    columns = '(id, first_name, middle_name, last_name, email, cell_phone, work_phone, home_phone, student_id)'
    query += columns + ' VALUES (' + ', '.join(values) + ');'

    cur.execute(query)
    con.commit()
    cur.close()


def generate_student_parents(mysql, dummy_info):
    con = mysql.connect()
    cur = con.cursor()

    cur.execute('SELECT id FROM admins UNION SELECT id FROM advisors UNION SELECT id FROM students UNION SELECT id FROM parents;')
    id_list = cur.fetchall()
    id_list = [int(i[0]) for i in id_list]

    id = str(random.randint(100000, 1000000))
    while id in id_list:
        id = str(random.randint(100000, 1000000))
    first_name = '"' + random.choice(dummy_info['first_names']) + '"'
    middle_name = '"' + random.choice(string.ascii_letters[26:]) + '"'
    last_name = '"' + random.choice(dummy_info['last_names']) + '"'
    email = '"' + str(random.randint(100000, 1000000)) + '@email.edu' + '"'
    cell_phone = '"' + str(415) + str(random.randint(0000000, 9999999)) + '"'
    work_phone = '"' + str(415) + str(random.randint(0000000, 9999999)) + '"'
    home_phone = '"' + str(415) + str(random.randint(0000000, 9999999)) + '"'
    school = '"' + random.choice(dummy_info['schools']) + '"'
    grade = '"' + random.choice(dummy_info['grade']) + '"'
    expected_grad = '"' + random.choice(['2021', '2022', '2023', '2024']) + '"'
    gpa = str(random.randint(0, 5)) + '.' + str(random.randint(0, 100))
    program_status = '"' + random.choice(dummy_info['status']) + '"'
    fmp_id = str(random.randint(100000, 1000000))
    parent_1_id = id + '01'
    parent_2_id = id + '02'

    con = mysql.connect()
    cur = con.cursor()

    cur.execute('SELECT id FROM advisors;')
    advisor_id_list = cur.fetchall()
    advisor_id_list = [int(i[0]) for i in advisor_id_list]
    advisor_id = str(random.choice(advisor_id_list))

    values = (id, first_name, middle_name, last_name, email, cell_phone, work_phone, home_phone, school, grade,
              expected_grad, gpa, program_status, fmp_id, parent_1_id, parent_2_id, advisor_id)

    query = 'INSERT INTO students '
    columns = '(id, first_name, middle_name, last_name, email, cell_phone, work_phone, home_phone, school, grade, ' +\
              'expected_grad, gpa, program_status, fmp_id, parent_1_id, parent_2_id, advisor_id)'
    query += columns + ' VALUES (' + ', '.join(values) + ');'

    cur.execute(query)
    con.commit()
    cur.close()

    generate_parent(mysql, dummy_info, id, parent_1_id)
    generate_parent(mysql, dummy_info, id, parent_2_id)


def main(mysql):
    dummy_info = get_dummy_info()

    for i in range(0, 3):
        generate_admin(mysql, dummy_info)

    for i in range(0, 20):
        generate_advisor(mysql, dummy_info)

    for i in range(0, 100):
        generate_student_parents(mysql, dummy_info)

    '''
    message = 'Enter "1" to generate admin, "2" to generate advisor, "3" to generate student and parents, or "0" to quit: '
    user_input = input(message)

    while user_input != 0:
        if int(user_input) == 1:
            generate_admin(mysql, dummy_info)
            user_input = input(message)
        elif int(user_input) == 2:
            generate_advisor(mysql, dummy_info)
            user_input = input(message)
        elif int(user_input) == 3:
            generate_student_parents(mysql, dummy_info)
            user_input = input(message)
    '''


if __name__ == '__main__':
    app = flask.Flask(__name__)
    app.secret_key = 'fuzzybuddy'

    mysql = MySQL()
    mysql.init_app(app)

    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = input('MySQL Password: ')
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_DB'] = 'ucsfda'

    main(mysql)
