from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
app = Flask(__name__)
Bcrypt = Bcrypt(app)

# Have import from mysqlconnection on every model for DB interactions
# Import the model's python file as a module, not the class directly so you avoid circular import errors!
# For example: from flask_app.models import table2_model

'''
! Note: If you are working with tables that are related to each other,
!       you'll want to import the other table's class here for when you need to create objects with that class.

! Example: importing pets so we can make pet objects for our users that own them.

Class should match the data table exactly that's in your DB.

REMEMBER TO PARSE DATA INTO OBJECTS BEFORE SENDING TO PAGES!

'''


class validate:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (name, email, password, created_at, updated_at) VALUES (%(name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('users').query_db(query, data)


def validation():
    error = False
    mysql = connectToMySQL('login_register')
    query = "SELECT * FROM users WHERE email = %(e_mail)s "
    data = {
        "e_mail": request.form['email']
    }
    check = mysql.query_db(query, data)

    if len(request.form["first_name"]) == 0 or len(request.form["last_name"]) == 0 or len(request.form["email"]) == 0 or len(request.form["password"]) == 0 or len(request.form["confirm_password"]) == 0:
        flash("All input fileds are required", 'top')
        error = True
    else:
        if not NAME_REGEX.match(request.form["first_name"]):
            flash("First Name field can not contain numbers", 'frname')
            error = True

        if len(request.form['first_name']) < 2:
            flash('Invalid name length: First Name', 'frname')

        if not NAME_REGEX.match(request.form["last_name"]):
            flash("Last Name field can not contain numbers", 'last_name')
            error = True

        if len(request.form['last_name']) < 2:
            flash('Invalid name length: Last Name', 'last_name')

        if len(request.form["password"]) < 8:
            flash("Password must be more than 8 characters", 'password')
            error = True

        if check:
            if check[0]['email'] == request.form['email']:
                flash("Email has already been registered", 'email')
                error = True

        if not EMAIL_REGEX.match(request.form["email"]):
            flash("Invalid Email format", 'email')
            error = True

        if request.form["password"] != request.form["confirm_password"]:
            flash("Passwords do not match", 'password')
            error = True

    if error == True:
        return redirect('/')
    elif error == False:
        reg_pass_hash = bcrypt.generate_password_hash(request.form['password'])
        mysql = connectToMySQL('login_info')
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(frname)s, %(lsname)s, %(e_mail)s, %(pass)s, NOW(), NOW());"
        data = {
            "frname": request.form['first_name'],
            "lsname": request.form['last_name'],
            "e_mail": request.form['email'],
            'pass': reg_pass_hash
        }
        mysql.query_db(query, data)
        flash('Registration Successful! Thank you for registering, you may now log in', 'success')
