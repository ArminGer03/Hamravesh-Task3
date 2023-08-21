from flask import Flask, render_template, request, session, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.secret_key = 'felan-alaki-yechizi-mizaram'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


def check_password_format(password):
    # Check for whitespace
    if ' ' in password:
        return False

    # Check for lowercase, uppercase, and digit
    has_lowercase = False
    has_uppercase = False
    has_digit = False

    for char in password:
        if char.islower():
            has_lowercase = True
        elif char.isupper():
            has_uppercase = True
        elif char.isdigit():
            has_digit = True

    return has_lowercase and has_uppercase and has_digit


def hash_password(password):
    # Create a SHA256 hash object
    sha256_hash = hashlib.sha256()

    # Convert the password string to bytes and hash it
    sha256_hash.update(password.encode('utf-8'))

    # Get the hashed password as a hexadecimal string
    hashed_password = sha256_hash.hexdigest()

    return hashed_password

def check_password(password, username):
    # Hash the entered password
    entered_password_hash = hash_password(password)

    user = User.query.filter_by(username=username).first()
    hashed_password = user.password
    # Compare the hashed passwords
    return entered_password_hash == hashed_password
    


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/styles.css')
def styles():
    return render_template('styles.css')

@app.route('/logo.png')
def load_logo():
    return send_file('images/logo.png', mimetype='image/png')

@app.route('/prof.jpeg')
def load_prof():
    return send_file('images/prof.jpeg', mimetype='image/jpeg')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user != None:
            if check_password(password, username):
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid password. Please try again.'
                return render_template('login.html', error=error)
        else:
            error = 'Username does not exist. Please sign up.'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        user = User.query.filter_by(username=username).first()
        if user is None:
            if len(password) < 6:
                error = 'Password must have atleast 6 characters'
                return render_template('signup.html', error=error)
            elif not check_password_format(password):
                error = 'Invalid password format.'
                return render_template('signup.html', error=error)
            elif confirmPassword != password:
                error = 'Password confirmation dont match.'
                return render_template('signup.html', error=error)
            else:
                hashed_password = hash_password(password)
                new_user = User(username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect(url_for('dashboard'))
        else:
            error = 'Username exist please try another username.'
            return render_template('signup.html', error=error)

    return render_template('signup.html')

@app.route('/home')
def home_page():
    return redirect(url_for('home'))

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/achievements')
def achievements():
    return render_template('achievements.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
