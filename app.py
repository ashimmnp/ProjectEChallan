from flask import Flask, request, render_template, redirect, url_for, flash
from models import *
import secrets
from sqlalchemy import text
import pymysql
from database import db
from flask_migrate import Migrate

app = Flask(__name__)
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


@app.route('/sample_login', methods=['GET', 'POST'])
def sample_login():
    return render_template('trafficOfficerDB.html')


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


# @app.route('/')
# def adduserSuccess():
#     success_flag = request.args.get('adduserSuccess', False)
#     return render_template('addUser.html', success=success_flag)


@app.route('/newChallan', methods=['GET', 'POST'])
def newChallan():
    return render_template('newChallan.html')


if __name__ == '__main__':
    app.run(debug=True)