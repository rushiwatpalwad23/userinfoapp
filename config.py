import os

class Config:
    # Secret key for session management
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')

    # MySQL Database URI (update with your credentials)
    MYSQL_USER = os.getenv('MYSQL_USER', 'admin')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Rutuja*1998')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'database-1.czma46y8s5sd.ap-south-1.rds.amazonaws.com')  # for localhost use 'localhost'
    MYSQL_DB = os.getenv('MYSQL_DB', 'userinfoapp')

    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload folder for user resumes
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
