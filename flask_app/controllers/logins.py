from flask import Flask, render_template, redirect, request, session, flash
import re
from flask_app.config import mysqlconnection
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "itslogintime"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

# Import Your Models as Classes into the Controller to use their Classmethods

# from flask_app.models.table_model import classname
from flask_app.models.login import validate


# ====================================
#    Create Routes
#    Show Form Route, Submit Form Route
# ====================================
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if not validate.validate(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    validate.save(data)
    return redirect('/')


# ====================================
# Log In Validations Route
# ====================================


# ====================================
#    Read Routes
#    Show Routes (Get All and Get One)
# ====================================


# ====================================
#    Update Routes
#    Update Form Route, Submit Update Form Route
# ====================================


# ====================================
#    Delete Routes
# ====================================
