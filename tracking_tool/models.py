from tracking_tool import db, login_manager, app
from flask_login import UserMixin
import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
# check if User authenticated, active, annonymous, get ID
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    # columns for table
    id = db.Column(db.Integer(), primary_key=True, unique=True)  # primary_key indicates unique identifier
    authorization = db.Column(db.Integer(), nullable=False)
    ucsf_da_id = db.Column(db.Integer(), unique=True, nullable=False)
    username = db.Column(db.String(32), unique=True, nullable = False)
    #email = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    # don't expect self as an argument; only token
    def verify_reset_token(token):
        # this is a static method
        s = Serializer(app.config['SECRET_KEY'])
        try:
            id = s.loads(token)['id']
        except:
            return None
        return User.query.get(id)

    def __repr__(self): # how object is printed
        return f"User('{self.username}')"


class Admins(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    first_name = db.Column(db.String(60), nullable=False)
    middle_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60), nullable=False)
    home_address = db.Column(db.String(64), nullable=False)
    home_city = db.Column(db.String(64), nullable=False)
    home_state = db.Column(db.String(32), nullable=False)
    home_zip = db.Column(db.String(8), nullable=False)
    work_address = db.Column(db.String(64))
    work_city = db.Column(db.String(64))
    work_state = db.Column(db.String(32))
    work_zip = db.Column(db.String(8))
    email = db.Column(db.String(128), unique=True, nullable=False)
    cell_phone = db.Column(db.String(10))
    work_phone = db.Column(db.String(10), nullable=False)
    home_phone = db.Column(db.String(10), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    # don't expect self as an argument; only token
    def verify_reset_token(token):
        # this is a static method
        s = Serializer(app.config['SECRET_KEY'])
        try:
            id = s.loads(token)['id']
        except:
            return None
        return Admins.query.get(id)


class Advisors(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(60), nullable=False)
    middle_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60), nullable=False)
    home_address = db.Column(db.String(64), nullable=False)
    home_city = db.Column(db.String(64), nullable=False)
    home_state = db.Column(db.String(32), nullable=False)
    home_zip = db.Column(db.String(8), nullable=False)
    work_address = db.Column(db.String(64))
    work_city = db.Column(db.String(64))
    work_state = db.Column(db.String(32))
    work_zip = db.Column(db.String(8))
    email = db.Column(db.String(128), unique=True, nullable=False)
    cell_phone = db.Column(db.String(10))
    work_phone = db.Column(db.String(10), nullable=False)
    home_phone = db.Column(db.String(10), nullable=False)
    school = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    # don't expect self as an argument; only token
    def verify_reset_token(token):
        # this is a static method
        s = Serializer(app.config['SECRET_KEY'])
        try:
            id = s.loads(token)['id']
        except:
            return None
        return Advisors.query.get(id)

class Parents(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(60), nullable=False)
    middle_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60), nullable=False)
    home_address = db.Column(db.String(64), nullable=False)
    home_city = db.Column(db.String(64), nullable=False)
    home_state = db.Column(db.String(32), nullable=False)
    home_zip = db.Column(db.String(8), nullable=False)
    work_address = db.Column(db.String(64))
    work_city = db.Column(db.String(64))
    work_state = db.Column(db.String(32))
    work_zip = db.Column(db.String(8))
    email = db.Column(db.String(128), nullable=False)
    cell_phone = db.Column(db.String(10))
    work_phone = db.Column(db.String(10))
    home_phone = db.Column(db.String(10), nullable=False)
    student_id = db.Column(db.Integer, nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    # don't expect self as an argument; only token
    def verify_reset_token(token):
        # this is a static method
        s = Serializer(app.config['SECRET_KEY'])
        try:
            id = s.loads(token)['id']
        except:
            return None
        return Parents.query.get(id)

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(60), nullable=False)
    middle_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60), nullable=False)
    home_address = db.Column(db.String(64), nullable=False)
    home_city = db.Column(db.String(64), nullable=False)
    home_state = db.Column(db.String(32), nullable=False)
    home_zip = db.Column(db.String(8), nullable=False)
    work_address = db.Column(db.String(64))
    work_city = db.Column(db.String(64))
    work_state = db.Column(db.String(32))
    work_zip = db.Column(db.String(8))
    email = db.Column(db.String(128), unique=True, nullable=False)
    cell_phone = db.Column(db.String(10))
    work_phone = db.Column(db.String(10))
    home_phone = db.Column(db.String(10), nullable=False)
    school = db.Column(db.String(60), nullable=False)
    grade = db.Column(db.String(16), nullable=False)
    expected_grad = db.Column(db.Integer, nullable=False)
    gpa = db.Column(db.Float, nullable=False)
    program_status = db.Column(db.String(16), nullable=False)
    fmp_id = db.Column(db.Integer, unique=True, nullable=False)
    parent_1_id = db.Column(db.Integer, nullable=False)
    parent_2_id = db.Column(db.Integer, nullable=False)
    advisor_id = db.Column(db.Integer, nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    # don't expect self as an argument; only token
    def verify_reset_token(token):
        # this is a static method
        s = Serializer(app.config['SECRET_KEY'])
        try:
            id = s.loads(token)['id']
        except:
            return None
        return Students.query.get(id)

class Reports(db.Model):
    report_id = db.Column(db.Integer, primary_key=True, unique=True)
    id = db.Column(db.Integer)
    submitter_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    program_status = db.Column(db.String(16), nullable=False)
    gpa = db.Column(db.String(60), nullable=False)
    student_sig = db.Column(db.String(64))
    parent_sig = db.Column(db.String(64))
    notes = db.Column(db.Text(65535))
