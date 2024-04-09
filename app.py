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
        user_name = request.form['username']
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



@app.route('/userManagementPortal', methods=['GET','POST'])
def userManagementPortal():
    # officers = Officer.query.all()
    if request.method == 'POST':
        search = request.form['query']
        officers = db.session.query(Officer, Users.usertype).join(Users, Officer.username == Users.username).filter(Users.name.ilike(f'%{search}')).all()
        return render_template('userManagementPortal.html', officers=officers)
    else:
        officers = db.session.query(Officer, Users.usertype).join(Users, Officer.username == Users.username).all()
        return render_template('userManagementPortal.html', officers=officers)


@app.route('/updateUser/<int:officer_id>', methods=['GET', 'POST'])
def updateUser(officer_id):
    officer = Officer.query.get_or_404(officer_id)
    if request.method == 'POST':
        try:
            officer.name = request.form['name']
            officer.badgeNumber = request.form['badge_number']
            officer.rank = request.form['rank']
            officer.assignedLocation = request.form['assigned_location']
            db.session.commit()
            flash('Successfully updated', 'success')
            return redirect(url_for('updateUser', officer_id=officer_id))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('Something went wrong in the system. Please try again', 'error')
    return render_template('updateUser.html', officer=officer)


@app.route('/deleteUser/<string:username>', methods=['DELETE'])
def deleteUser(username):
    try:
        officer = Users.query.filter_by(username=username).first()

        if officer:
            db.session.delete(officer)
            db.session.commit()
            return 'Officer Deleted Successfully', 200
        else:
            return 'Officer Not found', 404
    except SQLAlchemyError as e:
        db.session.rollback()
    return 'Problem, 500'

@app.route('/rulesStructure')
def rulesStructure():
    rules_category = {}
    rules = rulesAndRegulations.query.all()
    for rule in rules:
        if rule.rulecategory not in rules_category:
            rules_category[rule.rulecategory] = []
        rules_category[rule.rulecategory].append(rule)
    print(rules_category)
    return render_template('ruleStr.html', rules_category=rules_category)


if __name__ == '__main__':
    app.run(debug=True)
