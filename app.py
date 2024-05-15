from flask import Flask, request, render_template, redirect, url_for, flash, abort, session, jsonify
from flask_login import UserMixin, login_user
from models import *
import secrets
from sqlalchemy import text, func
import pymysql
from database import db
from flask_migrate import Migrate
from werkzeug.security import check_password_hash
import traceback
from datetime import datetime
import re

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/dataechallan'
secret_key = secrets.token_urlsafe(32)
app.secret_key = secret_key

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def welcome():
    return render_template('index.html')



@app.route('/issueNewChallan', methods=['GET', 'POST'])
def issueNewChallan():
    # Render the template for adding a record
    username = session.get('username')
    if 'username' not in session:
        return redirect(url_for('login'))
    categories = rulesAndRegulations.query.distinct(rulesAndRegulations.rulecategory).all()
    rules = rulesAndRegulations.query.all()
    rules_data = [
        {'id': rule.rulesId, 'rulecategory': rule.rulecategory, 'ruleDesc': rule.ruleDesc}
        for rule in rules
    ]

    if request.method == 'POST':
        try:
            name = request.form['name']
            location = request.form['location']
            registration_number = request.form['registrationNumber']
            license_number = request.form['licenceId']
            violation_id = request.form['violationReason']
            print(name)
            print(violation_id)
            reason = '-'

            rule = rulesAndRegulations.query.filter_by(rulesId=violation_id).first()
            print(name)
            print(violation_id)

            previous_history = ChallanHistory.query.filter_by(
                registrationNumber=registration_number,
                licenseNumber=license_number,
                violationId=violation_id
            ).order_by(ChallanHistory.dateIssued.desc()).first()
            if previous_history and previous_history.violationCount >= rule.penaltyChance:
                reason = 'License is suspended due to maximum number of violations'
                flash('License is suspended due to repeated violations.', 'error')
                # return render_template('newChallan.html', username=username,categories = categories, rules=rules_data)
            print(previous_history)
            violation_count = previous_history.violationCount + 1 if previous_history else 1
            new_penalty = rule.fineStart * violation_count

            new_history = ChallanHistory(
                challannumber='CHL{}'.format(ChallanHistory.query.count() + 1),
                registrationNumber=registration_number,
                driverName = name,
                licenseNumber=license_number,
                violationReason=rule.ruleDesc,
                violationId=violation_id,
                chargedAmount=new_penalty,
                dateIssued = datetime.today(),
                issuedLocation=location,
                issuedBy=username,  # This could be dynamic based on logged-in user
                violationCount=violation_count

            )
            db.session.add(new_history)
            history_id = new_history.challannumber
            print(history_id)
            ChallanHistory.query.order_by(ChallanHistory.dateIssued.desc()).all()
            db.session.commit()
            print(reason)
            flash('Challan issued successfully!', 'success')
            return jsonify({'success': True, 'history_id': history_id, 'reasons': reason})
        except Exception as e:
            flash(str(e), 'error')
            app.logger.error(e)
            response = {
                "error": str(e),
                "traceback": traceback.format_exc().splitlines()
            }
            return jsonify(response), 500


        return render_template('newChallan.html', username=username,categories = categories, rules=rules_data)

    return render_template('newChallan.html', username=username,categories = categories, rules=rules_data)

@app.route('/issuedChallan/<history_id>/<reasons>')
def issuedChallan(history_id, reasons):
    history = ChallanHistory.query.get_or_404(history_id)
    return render_template('issueChallan.html', history=history, reasons=reasons)

@app.route('/adminDB')
def adminDB():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    return render_template('adminDB.html', username=username)


@app.route('/trafficOfficerDB')
def trafficOfficerDB():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('trafficOfficerDB.html', username=session['username'])


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

                    return redirect(url_for('adminDB',username=user.username))
                elif user.usertype == 'officer':

                    return redirect(url_for('trafficOfficerDB', username=user.username))
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
    if 'username' not in session:
        return redirect(url_for('login'))
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




@app.route('/userManagementPortal', methods=['GET', 'POST'])
def userManagementPortal():
    # officers = Officer.query.all()
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        search = request.form['query']
        officers = db.session.query(Officer, Users.usertype).join(Users, Officer.username == Users.username).filter(
            Users.name.ilike(f'%{search}')).all()
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


@app.route('/checkRegistration', methods=['GET', 'POST'])
def checkRegistration():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        regNumber = request.form.get('registrationNumber')
        result = Vehicle.query.filter(func.lower(Vehicle.RegistrationNumber) == regNumber.lower()).first()
        print(result)
        if result:
            return render_template('checkRegistration.html', result=result, registrationNumber=regNumber)
        else:
            return render_template('checkRegistration.html', result=None, registrationNumber=regNumber)
    return render_template('checkRegistration.html')


@app.route('/checkLicense', methods=['GET', 'POST'])
def checkLicense():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        licenseId = request.form.get('licenseNumber')
        result = licencesData.query.filter(func.lower(licencesData.licenseId) == licenseId.lower()).first()
        if result:
            issued = result.dateIssued
            expire = result.expirationDate
            current_date = datetime.now().date()
            if issued <= current_date <= expire:
                status = 'Active'
            else:
                status = 'Expired'
            return render_template('checkRegistration.html', result=result, licenseNumber=licenseId, status=status)
        else:
            return render_template('checkRegistration.html', result=None, licenseNumber=licenseId)
    return render_template('checkRegistration.html')


@app.route('/vehicleDetailAdd', methods=['GET', 'POST'])
def vehicleDetailAdd():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        try:
            vehicle_id = request.form.get('vehicle_id')
            vehicle_type = request.form.get('vehicle_type')
            make = request.form.get('make')
            chassis_number = request.form.get('chassis_number')
            engine_number = request.form.get('engine_number')
            registration_id = request.form.get('registration_id')
            registration_number = request.form.get('registration_number')
            registration_date = request.form.get('registration_date')
            vehicle_category = request.form.get('vehicle_category')
            vehicle_model = request.form.get('vehicle_model')
            vehicle_custom_tax_id = request.form.get('vehicle_custom_tax_id')

            # Update configuration data in the database
            configuration = Vehicle(
                vehicleId=vehicle_id,
                vehicleType=vehicle_type,
                vehicleMake=make,
                ChasisNumber=chassis_number,
                EngineNumber=engine_number,
                RegistrationId=registration_id,
                RegistrationNumber=registration_number,
                registrationdate=registration_date,
                VehicleCategory=vehicle_category,
                VehicleModel=vehicle_model,
                VehicleCustomtaxId=vehicle_custom_tax_id
            )
            db.session.add(configuration)
            db.session.commit()
            flash('Configuration updated successfully', 'success')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')

            return redirect(url_for('vehicleDetailAdd'))
        else:
            return render_template('vehicleDetailAdd.html')
    return render_template('vehicleDetailAdd.html')


@app.route('/registrationDetailAdd', methods=['GET', 'POST'])
def registrationDetailAdd():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        try:
            registration_number = request.form.get('registration_number')
            if not re.match(r"^[A-Z]+\d{4,6}$",registration_number):
                flash('Invalid Registration Number Format!\nThe correct format is REG000', 'warning')
                return redirect(url_for('registrationDetailAdd'))
            vehicle_id = request.form.get('vehicle_id')
            if not re.match(r"^[A-Z]+\d+$",vehicle_id):
                flash('Invalid Vehicle Id Format!\nThe correct format is VH000', 'warning')
                return redirect(url_for('registrationDetailAdd'))
            citizen_id = request.form.get('citizen_id')
            if not re.match(r"^[a-zA-Z]+\d+$",citizen_id):
                flash('Invalid Citizen Id Format!\nThe correct format is ctz000', 'warning')
                return redirect(url_for('registrationDetailAdd'))
            license_id = request.form.get('license_id')
            if not re.match(r"^[a-zA-Z]+\d+$",license_id):
                flash('Invalid License Number Format!\nThe correct format is lsCITY000', 'warning')
                return redirect(url_for('registrationDetailAdd'))
            name = request.form.get('name')
            if not re.match(r"^[A-Za-z]+(?: [A-Za-z]+)*$", name):
                flash('Invalid Name Format!\nName must be in alphabetic characters.', 'warning')
                return redirect(url_for('registrationDetailAdd'))
            registration_expired = request.form.get('registration_expired')

            registration_expired_date = datetime.strptime(registration_expired, '%Y-%m-%d').date()
            current_date = datetime.now().date()

            if registration_expired_date < current_date:
                registration_status = 'Expired'
            else:
                registration_status = 'Active'
            # Update registration data in the database
            ownerRegistration = VehicleOwner(
                registrationNumber=registration_number,
                vehicleid=vehicle_id,
                citizenId=citizen_id,
                licenseId=license_id,
                Name=name,
                RegistrationExp=registration_expired,
                RegistrationStatus=registration_status
            )
            db.session.add(ownerRegistration)
            db.session.commit()
            flash('Registration completed successfully', 'success')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')

        return redirect(url_for('registrationDetailAdd'))  # Redirect to home page after registration
    else:
        return render_template('registrationDetailAdd.html')
    return render_template('registrationDetailAdd.html')





@app.route('/userProfile', methods = ['GET', 'POST'])
def userProfile():
    if 'username' not in session:
        return redirect(url_for('login'))
    sessionUser = Users.query.filter_by(username=session['username']).first()
    usersName = sessionUser.name
    sessionUserUName = sessionUser.username
    usersType = sessionUser.usertype

    if request.method == 'POST':
        username = session['username']
        current_password = request.form.get('current-password')
        new_password = request.form.get('new-password')
        confirm_password = request.form.get('confirm-password')

        user = Users.query.filter_by(username=username).first()
        if user:
            if user.password == current_password:
                if new_password == confirm_password:
                    user.password = new_password
                    db.session.commit()
                    flash('Password updated successfully', 'success')
                else:
                    flash('New password and confirm password do not match', 'error')
            else:
                flash('Current password is incorrect', 'error')
        else:
            flash('Username not found', 'error')

        return redirect(url_for('userProfile'))

    return render_template('userProfile.html', name=usersName, usersType=usersType, username=sessionUserUName)


@app.route('/rulesPortal', methods=['GET', 'POST'])
def rulesPortal():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form.get('action') == 'add':
            rule_id = request.form.get('rule_id')
            rule_category = request.form.get('rule_category')
            fine_start = request.form.get('finestart')
            penalty_chance = request.form.get('penaltyChances')
            rule_desc = request.form.get('rule_desc')

            try:
                rule = rulesAndRegulations(rulesId=rule_id, rulecategory=rule_category,fineStart=fine_start, penaltyChance=penalty_chance, ruleDesc=rule_desc)
                db.session.add(rule)
                db.session.commit()
                flash('Rule added successfully', 'success')
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'error')

        elif request.form.get('action') == 'edit':
            rule_id = request.form.get('edit_rule_id')
            rule = rulesAndRegulations.query.filter_by(rulesId=rule_id).first()
            if rule:
                rule.rulecategory = request.form.get('edit_rule_category')
                rule.ruleDesc = request.form.get('edit_rule_desc')
                rule.fineStart = request.form.get('finechange')
                rule.penaltyChance = request.form.get('penaltyChange')

                try:
                    db.session.commit()
                    flash('Rule updated successfully', 'success')
                except Exception as e:
                    flash(f'An error occurred: {str(e)}', 'error')
            else:
                flash('Rule not found', 'error')

        elif request.form.get('action') == 'delete':
            rule_id = request.form.get('delete_rule_id')
            rule = rulesAndRegulations.query.filter_by(rulesId=rule_id).first()
            if rule:
                try:
                    db.session.delete(rule)
                    db.session.commit()
                    flash('Rule deleted successfully', 'success')
                except Exception as e:
                    flash(f'An error occurred: {str(e)}', 'error')
            else:
                flash('Rule not found', 'error')

        return redirect(url_for('rulesPortal'))

    else:
        rules = rulesAndRegulations.query.all()
        return render_template('rulesPortal.html', rules=rules)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        username = request.form.get('username')
        current_password = request.form.get('current-password')
        new_password = request.form.get('new-password')
        confirm_password = request.form.get('confirm-password')

        user = Users.query.filter_by(username=username).first()
        if user:
            if user.password == current_password:
                if new_password == confirm_password:
                    user.password = new_password
                    db.session.commit()
                    flash('Password updated successfully', 'success')
                else:
                    flash('New password and confirm password do not match', 'error')
            else:
                flash('Current password is incorrect', 'error')
        else:
            flash('Username not found', 'error')

        return redirect(url_for('change_password'))

    return render_template('change_password.html')


if __name__ == '__main__':
    app.config['DEBUG']=True
    app.run(debug=True)

