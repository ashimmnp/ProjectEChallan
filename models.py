from database import db


class ChallanHistory(db.Model):
    __tablename__ = 'challanhistory'

    challannumber = db.Column(db.String(255), primary_key=True)
    registrationNumber = db.Column(db.String(255), db.ForeignKey('vehicleowner.registrationNumber'))
    violationReason = db.Column(db.String(255))
    violationId = db.Column(db.String(255))
    chargedAmount = db.Column(db.Numeric(10, 2))
    dateIssued = db.Column(db.Date)
    issuedLocation = db.Column(db.String(255))

class Officer(db.Model):
    __tablename__ = 'officer'

    officerId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    badgeNumber = db.Column(db.String(255))
    rank = db.Column(db.String(255))
    assignedLocation = db.Column(db.String(255))

class Users(db.Model):
    __tablename__ = 'users'

    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    usertype = db.Column(db.String(50), nullable=False)

class Vehicle(db.Model):
    __tablename__ = 'vehicle'

    vehicleId = db.Column(db.String(255), primary_key=True)
    RegistrationId = db.Column(db.Integer)
    RegistrationNumber = db.Column(db.String(255))
    registrationdate = db.Column(db.Date)
    vehicleType = db.Column(db.String(255))
    vehicleMake = db.Column(db.String(255))
    VehicleModel = db.Column(db.String(255))
    ChasisNumber = db.Column(db.String(255))
    EngineNumber = db.Column(db.String(255))
    VehicleCategory = db.Column(db.String(255))
    VehicleCustomtaxId = db.Column(db.Integer)

class VehicleOwner(db.Model):
    __tablename__ = 'vehicleowner'

    registrationNumber = db.Column(db.String(255), primary_key=True)
    vehicleid = db.Column(db.String(255))
    citizenId = db.Column(db.String(255))
    Name = db.Column(db.String(255))
    RegistrationExp = db.Column(db.Date)
    RegistrationStatus = db.Column(db.String(50))


class rulesAndRegulations(db.Model):
    __tablename__ = 'rulesAndRegulations'

    rulesId = db.Column(db.String(255), primary_key=True)
    rulescategory = db.Column(db.String(255))
    ruleDesc = db.Column(db.String(225))
    fineAmount = db.column(db.String(255))

