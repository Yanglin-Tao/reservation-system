#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymsql.cursors
import datetime
import random

app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='Project1',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def hello():
	return render_template('index.html')

#Define route for customer login
@app.route('/customer_login')
def customer_login():
	return render_template('customer_login.html')

#Define route for customer register
@app.route('/customer_register')
def customer_register():
	return render_template('customer_register.html')

#Define route for staff login
@app.route('/staff_login')
def staff_login():
	return render_template('staff_login.html')

#Define route for staff register
@app.route('/staff_register')
def staff_register():
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

#TODO: Authenticates staff login
#Author: Tianzuo Liu
@app.route('/staff_login_auth', methods=['GET', 'POST'])
def staff_login_auth():
	user_name = request.form['user_name']
	staff_password = request.form['staff_password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Airline_Staff WHERE user_name = %s and staff_password = %s'
	cursor.execute(query, (user_name, staff_password))
	#stores the results in a variable
	data = cursor.fetchone()
	cursor.close()
	error = None
	if(data):
		#creates a session for the user
		#session is a built in
		session['user_name'] = user_name
		return redirect(url_for('staff_home'))
	else:
		#returns an error message to the html page
		error = 'Invalid email address or password'
		return render_template('staff_login.html', error=error)

#TODO: Authenticates customer register
#Author: Tianzuo Liu
@app.route('/customer_register_auth', methods=['GET', 'POST'])
def customer_register_auth():
	customer_email = request.form['customer_email']
	customer_password = request.form['customer_password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE customer_email = %s and customer_password = %s'
	cursor.execute(query, (customer_email, customer_password))
	#stores the results in a variable
	data = cursor.fetchone()
	
	if(data):
		#if query returns the data, it means the data already exists
		error = "Sorry, this account has already existed."
		cursor.close()
		return render_template('customer_register.html', error=error)
	else:
		ins = 'INSERT INTO Customer VALUES(%s, %s)'
		cursor.execute(ins, (customer_email, customer_password))
		conn.commit()
		cursor.close()
		return render_template('index.html')

#TODO: Authenticates staff register
#Author: Tianzuo Liu
@app.route('/staff_register_auth', methods=['GET', 'POST'])
def staff_register_auth():
	user_name = request.form['user_name']
	staff_password = request.form['staff_password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Airline_Staff WHERE user_name = %s and staff_password = %s'
	cursor.execute(query, (user_name, staff_password))
	#stores the results in a variable
	data = cursor.fetchone()
	
	if(data):
		#if query returns the data, it means the data already exists
		error = "Sorry, this account has already existed."
		cursor.close()
		return render_template('staff_register.html', error=error)
	else:
		ins = 'INSERT INTO Airline_Staff (user_name, staff_password) VALUES(%s, %s)'
		cursor.execute(ins, (user_name, staff_password))
		conn.commit()
		cursor.close()
		return render_template('index.html')

#TODO: Customer home
#Author: Tianzuo Liu
@app.route('customer_home', methods=['GET', 'POST'])
def customer_home():
	if "customer_email" in session:
		customer_email = session['customer_email']
	else:
		return redirect(url_for('customer_login'))

	query = 'SELECT * FROM Customer \
	WHERE customer_email = %s'
	cursor = conn.cursor()
	cursor.execute(query,(customer_email))
	data = cursor.fetchall()
	cursor.close()

	return render_template('customer_home.html', customer_email = customer_email, data = data)

#TODO: Customer searches for flights
#Author: Tianzuo Liu
'''
Search for future flights (one way or round trip) based on source city/airport name, 
destination city/airport name, dates (departure or return).
'''
# Input: departure airport, arrival airport, daparture date, arrival date
# Output: flight_number, departure_airport, departure date, arrival date, arrival airport
@app.route('customer_search_flights', methods=['GET', 'POST'])
def customer_search_flights():
	departure_airport = request.form['departure_airport']
	arrival_airport = request.form['arrival_airport']
	daparture_date = request.form['daparture_date']
	arrival_date = request.form['arrival_date']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	if (arrival_date != null):
		query = 'SELETCT * \
		From Flight WHERE departure_airport = %s and arrival_airport = %s and departure_date = %s and arrival_data = %s \
		and departure_date >= NOW()'
		cursor.execute(query, (departure_airport, arrival_airport, daparture_date, arrival_date))
	else:
		query = 'SELETCT * \
		From Flight WHERE departure_airport = %s and arrival_airport = %s and departure_date = %s \
		and departure_date >= NOW()'
		cursor.execute(query, (departure_airport, arrival_airport, daparture_date))
	#stores the results in a variable
	data = cursor.fetchall()
	cursor.close()
	if(data):
		return data
	else:
		error = 'Could not find the flight'
		return render_template('customer_home.html', error = error)

#TODO: Customer purchases a ticket (from result of searching flight)
#Author: Tianzuo Liu
@app.route('customer_search_flights', methods=['GET', 'POST'])
def purchase_ticket():
	data = customer_search_flights()
	flight_number = request.form['flight_number']
	card_type = request.form['card_type']
	card_number = request.form['card_number']
	expiration_date = request.form['expiration_date']
	name_on_card = request.form['name_on_card']
	sold_price = request.form['sold_price']
	airline_name = request.form['airline_name']
	#cursor used to send queries
	
	cursor = conn.cursor()
	customer_email = session['customer_email']

	query = 'SELECT * \
	FROM data WHERE flight_number = %s'
	cursor.execute(query, (flight_number))
	
	new_data = cursor.fetchone()
	ticket_ID = str(random.randint(0,9999999))

	if (new_data):
		insertion = 'INSERT INTO Ticket VALUES \
		(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(insertion, (ticket_ID, customer_email, sold_price, card_type, card_number, \
			name_on_card, expiration_date, NOW(), NOW(), new_data['departure_date'], new_data['departure_time'],flight_number, airline_name))
		conn.commit()

		purchase = 'INSERT INTO Purchase VALUES(%s, %s)'
		cursor.execute(purchase, (customer_email, ticket_ID))
		conn.commit()
		cursor.close()
		message = 'Successfully'
		return render_template('customer_home.html', message = messgae)
	else:
		error = 'something wrong. Please try again'
		return render_template('customer_home.html', error = error)



#TODO: Customer cancels a trip
#Author: Tianzuo Liu
@app.route('cancel_trip', methods=['GET', 'POST'])
def cancel_trip():
	ticket_ID = request.form['ticket_ID']
	flight_number = request.form['flight_number']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'DELETE FROM Ticket WHERE ticket_ID = %s and customer_email = %s'
	cursor.execute(query, (ticket_ID, session['customer_email']))
	
	#executes query
	query = 'DELETE FROM Purchase WHERE ticket_ID = %s and customer_email = %s'
	cursor.execute(query, (ticket_ID, session['customer_email']))

	cursor.close()
	message = "Successfully cancel the trip"
	return render_template('customer_home.html', message = message)

#TODO: Customer gives rating and comment
#Author: Yanglin Tao
@app.route('customer_rating')
def customer_rating():
	pass

#TODO: Customer tracks spending
#Author: Yanglin Tao
@app.route('track_spending')
def track_spending():
	pass

#TODO: Customer logout
#Author: Yanglin Tao
@app.route('customer_logout')
def customer_logout():
	pass

#TODO: Staff views flights
#Author: Yanglin Tao
@app.route('staff_view_flights')
def staff_view_flights():
	pass

#TODO: Staff creates new flights
#Author: Yanglin Tao
@app.route('staff_create_flight')
def create_flight():
	pass

#TODO: Staff changes status of the flight
#Author: Yanglin Tao
@app.route('change_status')
def change_status():
	pass

#TODO: Staff adds new airplane in the system
#Author: Yanglin Tao
@app.route('add_airplane')
def add_airplane():
	pass

#TODO: Staff adds new airport in the system
#Author: Justin Li
@app.route('add_airport')
def add_airport():
	pass

#TODO: Staff views the rating and comments of the flight, along with the average rating
#Author: Justin Li
@app.route('view_rating')
def view_rating():
	pass

#TODO: Staff views the most frequent customer
#Author: Justin Li
@app.route('frequent_customer')
def frequent_customer():
	pass

#TODO: Staff views all flights of a customer
#Author: Justin Li
@app.route('view_customer_flights')
def view_customer_flights():
	pass

#TODO: Staff views reports
#Author: Justin Li
@app.route('view_reports')
def view_reports():
	pass

#TODO: Staff views earned revenue
#Author: Justin Li
@app.route('view_revenue')
def view_revenue():
	pass

#TODO: Staff logout
#Author: Justin Li
@app.route('staff_logout')
def staff_logout():
	pass

#Run the app on localhost port 5000
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)