from flask import Flask, request, render_template, redirect, url_for


app = Flask(__name__)

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


@app.route('/addUser',methods=['GET', 'POST'])
def addUser():
    return render_template('addUser.html')


if __name__ == '__main__':
    app.run(debug=True)
