#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='blog',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Define route for customer login
@app.route('/customer_login')
def login():
	return render_template('customer_login.html')

#Define route for customer register
@app.route('/customer_register')
def register():
	return render_template('customer_register.html')

#Define route for staff login
@app.route('/staff_login')
def login():
	return render_template('staff_login.html')

#Define route for staff register
@app.route('/staff_register')
def register():
	return render_template('staff_register.html')

#Authenticates customer login
@app.route('/customer_login_auth', methods=['GET', 'POST'])
def customer_login_auth():
	#grabs information from the forms
	customer_email = request.form['customer_email']
	customer_password = request.form['customer_password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE customer_email = %s and customer_password = %s'
	cursor.execute(query, (customer_email, customer_password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['customer_email'] = customer_email
		return redirect(url_for('customer_home'))
	else:
		#returns an error message to the html page
		error = 'Invalid email address or password'
		return render_template('customer_login.html', error=error)

#Run the app on localhost port 5000
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)