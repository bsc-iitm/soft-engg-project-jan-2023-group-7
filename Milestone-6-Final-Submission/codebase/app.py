from flask import request, url_for, redirect
from flask_login import LoginManager, login_manager, login_user
from os import environ, path, remove
from models.users import user_datastore, User, Role, roles_users
from models import db
from flask import Flask, render_template, request, redirect
from flask_security import login_required, Security, logout_user, roles_accepted
from flask_restful import Resource, Api
from controllers.query_Controller import Query_Create, Query_Others, Query_Search
from controllers.faqs_Controller import FAQ_Create, FAQ_Others, FAQ_Search
from controllers.users_Controller import User_Create, User_Others
from flask_cors import CORS

# Create app
app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'HelloWorld'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'

# CORS
CORS(app)

# Create database connection object
db.init_app(app)
students = Security(app, user_datastore)


def resetdb():
    file_exists = path.exists("database.sqlite3")
    if file_exists is True:                             # Remove this
        remove("database.sqlite3")               # before production


# Create Roles
@app.before_first_request
def create_user():
    resetdb()               # This needs to removed
    file_exists = path.exists("database.sqlite3")
    if file_exists != True:
        db.create_all()
        user_datastore.create_role(
            name='Admin', description='Admin Enrolled in Program')
        user_datastore.create_role(
            name='Instructors', description='Instructors for the Program')
        user_datastore.create_role(
            name='Staff', description='Staff Enrolled in Program')
        user_datastore.create_role(
            name='Student', description='Students Enrolled in Program')
        # add a admin user
        user_datastore.create_user(
            email="admin@mail.com", password="root", active=True)
        user_datastore.add_role_to_user(User.query.filter_by(
            email="admin@mail.com").first(), Role.query.filter_by(name="Admin").first())
        db.session.commit()
        user_datastore.create_user(
            email="student@mail.com", password="toor", active=True)
        user_datastore.add_role_to_user(User.query.filter_by(
            email="student@mail.com").first(), Role.query.filter_by(name="Student").first())
        db.session.commit()


# Views
@app.route("/test")
def HelloWorld():
    return '''<h1>Welcome user !!</h1>
                <br/><hr/>
                <h3>
                We are glad to inform you that the application is running successfully !!
                </h3>'''

@app.route("/")
def Index():
    return render_template("index.html")


# Signup code block
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ""
    # if the form is submitted
    if request.method == 'POST':
        # check if user already exists
        user = User.query.filter_by(email=request.form['email']).first()
        msg = ""
        # if user already exists render the msg
        if user:
            msg = "User already exist"
            # render signup.html if user exists
            return render_template('signup.html', msg=msg)

        # if user doesn't exist

        # store the user to database
        user = User(email=request.form['email'],
                    active=1, password=request.form['password'])
        # store the role
        role = Role.query.filter_by(id=request.form['options']).first()
        user.roles.append(role)

        # commit the changes to database
        db.session.add(user)
        db.session.commit()

        # login the user to the app
        # this user is current user
        login_user(user)
        # redirect to index page
        return redirect('/')

    # case other than submitting form, like loading the page itself
    else:
        return render_template("signup.html", msg=msg)


# Signin code block
@app.route('/sign_in', methods=['GET', 'POST'])
def signin():
    msg = ""
    if request.method == 'POST':
        # search user in database
        user = User.query.filter_by(email=request.form['email']).first()
        # if exist check password
        if user:
            if user.password == request.form['password']:
                # if password matches, login the user
                login_user(user)
                return redirect('/')
            # if password doesn't match
            else:
                msg = "Wrong password"

        # if user does not exist
        else:
            msg = "User doesn't exist"
        return render_template('signin.html', msg=msg)

    else:
        return render_template("signin.html", msg=msg)


# Admin only access
@app.route('/see_users')
@roles_accepted('Admin')
def see_all_users():
    admins = []
    # query for role Teacher that is role_id=2
    role_admin = db.session.query(roles_users).filter_by(role_id=1)
    # query for the users' details using user_id
    for a in role_admin:
        user = User.query.filter_by(id=a.user_id).first()
        admins.append(user)
    # return the teachers list
    return render_template("all_users.html", admins=admins)


# Api Intialisation
api = Api(app)
api.add_resource(Query_Create, '/api/query')
api.add_resource(Query_Others, '/api/query/<query_id>')
api.add_resource(FAQ_Create, '/api/faq')
api.add_resource(FAQ_Others, '/api/faq/<faq_id>')
api.add_resource(User_Create, '/api/client')
api.add_resource(User_Others, '/api/client/<client_id>')
api.add_resource(Query_Search, '/api/search_by_query/<text>')
api.add_resource(FAQ_Search, '/api/search_by_faq/<text>')

if __name__ == '__main__':
    app.run(port=environ.get("PORT", 8080), host='0.0.0.0', debug=True)
