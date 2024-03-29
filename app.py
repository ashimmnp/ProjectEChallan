from flask import Flask, request, render_template, redirect, url_for


app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')


# def search():
#     return render_template("checkRegistration.html")

@app.route('/checkRegistration', methods=['GET', 'POST'])
def checkRegistration():
    if request.method == 'POST':
        regNumber = request.form.get('registrationNumber')
        conn = db.engine.connect()
        sql = text("SELECT * FROM vehicle_registration WHERE registrationNumber = :regNumber")
        resultfetch = conn.execute(sql)
        result = resultfetch.fetchone()
        if result:
            return render_template('checkRegistration.html', result=result, registrationNumber=regNumber)
        else:
            return render_template('checkRegistration.html', result=None, registrationNumber=regNumber)
    return render_template('checkRegistration.html')


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

if __name__ == '__main__':
    app.run(debug=True)
