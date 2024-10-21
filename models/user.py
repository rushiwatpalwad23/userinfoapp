from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    @staticmethod
    def add_user(user):
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error adding user: {str(e)}")

    @staticmethod
    def get_user(email, password):
        try:
            return User.query.filter_by(email=email, password=password).first()
        except Exception as e:
            raise Exception(f"Error fetching user: {str(e)}")


# Create a new model to store user information
class UserInfo(db.Model):
    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    resume = db.Column(db.String(200), nullable=True)  # Store the filename or S3 path

    def __init__(self, first_name, last_name, address, company, experience, resume=None):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.company = company
        self.experience = experience
        self.resume = resume

    @staticmethod
    def add_info(info):
        try:
            db.session.add(info)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error adding info: {str(e)}")
