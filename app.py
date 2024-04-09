from flask import Flask, request, render_template, redirect, url_for, flash, abort, session
from flask_login import UserMixin, login_user
from models import *
import secrets
from sqlalchemy import text
import pymysql
from database import db
from flask_migrate import Migrate
from werkzeug.security import check_password_hash
import traceback


app = Flask(__name__,template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/dataechallan'
secret_key = secrets.token_urlsafe(32)
app.secret_key = secret_key

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/add-record', methods=['POST'])
def add_record():
    # Redirect to the page where record can be added
    return redirect(url_for('add_record_page'))


@app.route('/add-record-page')
def add_record_page():
    # Render the template for adding a record
    return render_template('newChallan.html')


@app.route('/adminDB')
def adminDB():
    return render_template('adminDB.html')


@app.route('/trafficOfficerDB')
def trafficOfficerDB():
    return render_template('trafficOfficerDB.html')


class users(UserMixin, db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    usertype = db.Column(db.String(50), nullable=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if not username or not password:
                flash('Username or password missing', 'error')
                return redirect(url_for('login'))

            user = Users.query.filter_by(username=username).first()

            if user and user.password == password:
                session['username'] = user.username
                session['usertype'] = user.usertype
                print(user.usertype)
                if user.usertype == 'admin':
                    flash('Admin login successful', 'success')
                    return redirect(url_for('adminDB'))
                elif user.usertype == 'officer':
                    flash('Officer login successful', 'success')
                    return redirect(url_for('trafficOfficerDB'))
                else:
                    flash('Invalid user type', 'error')
                    return redirect(url_for('login'))
            else:
                flash('Invalid username or password', 'error')
                return redirect(url_for('login'))

        return render_template('index.html')

    except Exception as e:
        traceback.print_exc()
        flash('An error occurred', 'error')
        return redirect(url_for('login'))

@app.route('/addUser', methods=['GET', 'POST'])
def addUser():
    if request.method == 'POST':
        name = request.form['name']
        officer_id = request.form['officer_id']
        user_id = request.form['user_id']
        user_name = request.form['user_name']
        badge_number = request.form['badge_number']
        rank = request.form['rank']
        user_type = request.form['user_type']
        location_assigned = request.form['location_assigned']
        password = 'pass1234'

        # Adding required record in officer table
        new_user_officer = Officer(officerId=officer_id, username=user_name, name=name, badgeNumber=badge_number,
                                   rank=rank, assignedLocation=location_assigned)

        # Adding required records in user table
        new_user_users = Users(userid=user_id, username=user_name, password=password, name=name, usertype=user_type)

        db.session.add(new_user_officer)
        db.session.add(new_user_users)

        try:
            db.session.commit()
            flash('Successfully added', 'success')
            return redirect(url_for('addUser'))
        except:
            db.session.rollback()
            flash('Something went wrong')
            return redirect(url_for('addUser'))
    return render_template('addUser.html')


@app.route('/newChallan', methods=['GET', 'POST'])
def newChallan():
    return render_template('newChallan.html')


if __name__ == '__main__':
    app.run(debug=True)
