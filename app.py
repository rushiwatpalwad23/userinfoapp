from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

# Import models and config
from models.user import db, User, UserInfo
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the SQLAlchemy object with the Flask app
db.init_app(app)

# Create database tables (make sure this only runs once, like when setting up)
with app.app_context():
    db.create_all()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = User(email, password)
            User.add_user(user)
            return redirect(url_for('signin'))
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.get_user(email, password)
        if user:
            session['user'] = email
            return redirect(url_for('user_info_form'))
        else:
            return "Invalid credentials"
    return render_template('signin.html')

# This route should only be accessible if the user is signed in
@app.route('/user_info_form', methods=['GET'])
def user_info_form():
    if 'user' in session:
        return render_template('user_form.html')
    else:
        # Redirect to sign-in page if the user is not logged in
        return redirect(url_for('signin'))

@app.route('/submit_info', methods=['POST'])
def submit_info():
    if 'user' in session:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        company = request.form['company']
        experience = request.form['experience']

        # File upload handling
        resume = request.files['resume']
        resume_filename = None
        if resume:
            filename = secure_filename(resume.filename)
            resume.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            resume_filename = filename  # Or store S3 path if using S3

        # Store user information in the database
        try:
            user_info = UserInfo(
                first_name=first_name,
                last_name=last_name,
                address=address,
                company=company,
                experience=experience,
                resume=resume_filename  # Add resume filename (or path if using S3)
            )
            UserInfo.add_info(user_info)
            return "Information submitted successfully!"
        except Exception as e:
            return f"Error storing information: {str(e)}"
    else:
        return redirect(url_for('signin'))


# Home route
@app.route('/')
def home():
    # Redirect to the user info form if logged in, else redirect to sign-in page
    if 'user' in session:
        return redirect(url_for('user_info_form'))
    else:
        return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)


