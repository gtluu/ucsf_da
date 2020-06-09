from tracking_tool import db, app, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
# check if User authenticated, active, annonymous, get ID
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    # columns for table

    id = db.Column(db.Integer, primary_key=True, unique=True)  # primary_key indicates unique identifier
    authorization = db.Column(db.Integer, nullable=False)
    ucsf_da_id = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(45), unique=True, nullable = False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

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
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(60), nullable=False)
    middle_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    cell_phone = db.Column(db.String(10))
    work_phone = db.Column(db.String(10), nullable=False)
    home_phone = db.Column(db.String(10), nullable=False)

class Advisors(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(60), nullable=False)
    middle_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    cell_phone = db.Column(db.String(10))
    work_phone = db.Column(db.String(10), nullable=False)
    home_phone = db.Column(db.String(10), nullable=False)
    school = db.Column(db.String(60), nullable=False)

class Parents(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(60), nullable=False)
    middle_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    cell_phone = db.Column(db.String(10))
    work_phone = db.Column(db.String(10))
    home_phone = db.Column(db.String(10), nullable=False)
    student_id = db.Column(db.Integer, nullable=False)

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(60), nullable=False)
    middle_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    cell_phone = db.Column(db.String(10))
    work_phone = db.Column(db.String(10))
    home_phone = db.Column(db.String(10), nullable=False)
    school = db.Column(db.String(60), nullable=False)
    grade = db.Column(db.String(16), nullable=False)
    expected_grad = db.Column(db.Integer, nullable=False)
    gpa = db.Column(db.String(60), nullable=False)
    program_status = db.Column(db.String(16), nullable=False)
    fmp_id = db.Column(db.Integer, unique=True, nullable=False)
    parent_1_id = db.Column(db.Integer, nullable=False)
    parent_2_id = db.Column(db.Integer, nullable=False)
    advisor_id = db.Column(db.Integer, nullable=False)

