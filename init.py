#Import Flask Library
import hashlib
from hashlib import md5
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import datetime
import random

app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
					   port = 8889,
                       password='root',
                       db='system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define route for index page
#Author: Yanglin Tao
@app.route('/')
def hello():
	return render_template('index.html')

#Show all future flights to anyone using the system
#Author: Yanglin Tao
@app.route('/general_show_flights', methods=['GET', 'POST'])
def general_show_flights():
	cursor = conn.cursor()
	if request.method == 'POST':
		dept_airport = request.form['departure_airport']
		arri_airport = request.form['arrival_airport']
		dept_city = request.form['departure_city']
		arri_city = request.form['arrival_city']
		dept_date = request.form['departure_date']
		return_date = request.form['return_date']
		# search for one way trip by airports
		if dept_airport != "" and arri_airport != "" and dept_date != "" and return_date == "" and dept_city == "" and arri_city == "":
			query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time, arrival_airport FROM Flight WHERE departure_date = %s AND departure_airport = %s AND arrival_airport = %s AND %s > CURRENT_DATE()'
			cursor.execute(query, (dept_date, dept_airport, arri_airport, dept_date))
			go_flights = cursor.fetchall()	
			cursor.close()
			if(go_flights):
				return render_template('index.html', go_flights = go_flights)
			else:
				noGoError = 'Sorry, no trip found.'
				return render_template('index.html', noGoError = noGoError)
		# search for round trip by airports
		elif dept_airport != "" and arri_airport != "" and dept_date != "" and return_date != "" and dept_city == "" and arri_city == "":
			if dept_date > return_date:
				dateError = "Arrival date must be after departure date."
				return render_template('index.html', dateError = dateError)
			# check if there is a return trip
			query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time, arrival_airport FROM Flight WHERE departure_date = %s AND departure_airport = %s AND arrival_airport = %s AND %s > CURRENT_DATE()'
			cursor.execute(query, (return_date, arri_airport, dept_airport, return_date))
			return_flights = cursor.fetchall()
			if (return_flights):
				query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time, arrival_airport FROM Flight WHERE departure_date = %s AND departure_airport = %s AND arrival_airport = %s AND %s > CURRENT_DATE()'
				cursor.execute(query, (dept_date, dept_airport, arri_airport, dept_date))
				go_flights = cursor.fetchall()	
				if(go_flights):
					return render_template('index.html', return_flights = return_flights, go_flights = go_flights)
				else:
					noGoError = "Sorry, no trip found"
					return render_template('index.html', noGoError = noGoError)
			else:
				noReturnError = 'Sorry, no return trip found.'
				return render_template('index.html', noReturnError = noReturnError)
		# search for round trip by city
		elif dept_airport == "" and arri_airport == "" and dept_date != "" and return_date != "" and dept_city != "" and arri_city != "":
			if dept_date > return_date:
				dateError = "Arrival date must be after departure date."
				return render_template('index.html', dateError = dateError)
			# check if there is a return trip
			query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time, arrival_airport FROM Flight, Airport D, Airport A WHERE Flight.departure_airport = D.airport_name AND Flight.arrival_airport = A.airport_name AND D.airport_city = %s AND A.airport_city = %s AND departure_date = %s AND %s > CURRENT_DATE()'
			cursor.execute(query, (arri_city, dept_city, return_date, return_date))
			return_flights = cursor.fetchall()
			if (return_flights):
				query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time, arrival_airport FROM Flight, Airport D, Airport A WHERE Flight.departure_airport = D.airport_name AND Flight.arrival_airport = A.airport_name AND D.airport_city = %s AND A.airport_city = %s AND departure_date = %s AND %s > CURRENT_DATE()'
				cursor.execute(query, (dept_city, arri_city, dept_date, dept_date))
				go_flights = cursor.fetchall()
				if(go_flights):
					return render_template('index.html', return_flights = return_flights, go_flights = go_flights)
				else:
					noGoError = "Sorry, no trip found"
					return render_template('index.html', noGoError = noGoError)
			else:
				noReturnError = 'Sorry, no return trip found.'
				return render_template('index.html', noReturnError = noReturnError)
		# search for one way by city
		elif dept_airport == "" and arri_airport == "" and dept_date != "" and return_date == "" and dept_city != "" and arri_city != "":
			query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time, arrival_airport FROM Flight, Airport D, Airport A WHERE Flight.departure_airport = D.airport_name AND Flight.arrival_airport = A.airport_name AND D.airport_city = %s AND A.airport_city = %s AND departure_date = %s AND %s > CURRENT_DATE()'
			cursor.execute(query, (dept_city, arri_city, dept_date, dept_date))
			go_flights = cursor.fetchall()
			if(go_flights):
				return render_template('index.html', go_flights = go_flights)
			else:
				noGoError = 'Sorry, no trip found.'
				return render_template('index.html', noGoError = noGoError)
		elif dept_airport == "" and arri_airport == "" and dept_city != "" and arri_city != "":
			invalidSearchError = 'Please enter only departure/arrival city or departure/arrival airport'
			return render_template('index.html', invalidSearchError = invalidSearchError)
		else:
			invalidSearchError = 'Invalid data'
			return render_template('index.html', invalidSearchError = invalidSearchError)
	else:
		return render_template('index.html')

#Check flight status to anyone using the system
#Author: Yanglin Tao
@app.route('/general_check_status', methods=['GET', 'POST'])
def general_check_status():
	cursor = conn.cursor()
	if request.method == 'POST':
		airline = request.form['airline_name']
		flight_num = request.form['flight_number']
		dept_date = request.form['departure_date']
		arri_date = request.form['arrival_date']
		if airline != "" and flight_num != "" and dept_date != "" and arri_date != "":
			query = 'SELECT airline_name, flight_number, departure_date, arrival_date, flight_status FROM Flight WHERE airline_name = %s AND flight_number = %s AND departure_date = %s AND arrival_date = %s'
			cursor.execute(query, (airline, flight_num, dept_date, arri_date))
			data = cursor.fetchall()	
			cursor.close()
			return render_template('index.html', status = data)
		else:
			error = 'Invalid data'
			return render_template('index.html', error=error)
	else:
		return render_template('index.html')

#Define route for customer login
#Author: Yanglin Tao
@app.route('/customer_login')
def customer_login():
	return render_template('customer_login.html')

#Define route for customer register
#Author: Yanglin Tao
@app.route('/customer_register')
def customer_register():
	return render_template('customer_register.html')

#Define route for staff login
#Author: Yanglin Tao
@app.route('/staff_login')
def staff_login():
	return render_template('staff_login.html')

#Define route for staff register
#Author: Yanglin Tao
@app.route('/staff_register')
def staff_register():
	return render_template('staff_register.html')

#Authenticates customer login
#Author: Yanglin Tao
@app.route('/customer_login_auth', methods=['GET', 'POST'])
def customer_login_auth():
	#grabs information from the forms
	email = request.form['customer_email']
	password = (hashlib.md5((request.form['customer_password']).encode())).hexdigest()
	# password = request.form['customer_password']
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE customer_email = %s and customer_password = %s'
	cursor.execute(query, (email, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['customer_email'] = email
		return redirect(url_for('customer_home'))
	else:
		#returns an error message to the html page
		error = 'Invalid email address or password'
		return render_template('customer_login.html', error=error)

#Authenticates staff login
#Author: Tianzuo Liu
@app.route('/staff_login_auth', methods=['GET', 'POST'])
def staff_login_auth():
	if request.method == 'POST':
		user_name = request.form['user_name']
		staff_password = (hashlib.md5((request.form['staff_password']).encode())).hexdigest()
		# staff_password = request.form['staff_password']
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
			error = 'Invalid username or password'
			return render_template('staff_login.html', error=error)
	else:
		return render_template('staff_login.html')


#Authenticates customer register
#Author: Tianzuo Liu
@app.route('/customer_register_auth', methods=['GET', 'POST'])
def customer_register_auth():
	customer_name = request.form['customer_name']
	customer_email = request.form['customer_email']
	customer_password = (hashlib.md5((request.form['customer_password']).encode())).hexdigest()
	building_number = request.form['building_number']
	street = request.form['street']
	city = request.form['city']
	state_name = request.form['state_name']
	phone_number = request.form['phone_number']
	passport_number = request.form['passport_number']
	passport_expiration = request.form['passport_expiration']
	passport_country = request.form['passport_country']
	date_of_birth = request.form['date_of_birth']

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
		ins = 'INSERT INTO Customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (customer_name, customer_email, customer_password, building_number, street, city, state_name, phone_number, \
		passport_number, passport_expiration, passport_country, date_of_birth))
		conn.commit()
		cursor.close()
		return render_template('index.html')

#Authenticates staff register
#Author: Tianzuo Liu
@app.route('/staff_register_auth', methods=['GET', 'POST'])
def staff_register_auth():
	user_name = request.form['user_name']
	staff_password = (hashlib.md5((request.form['staff_password']).encode())).hexdigest()
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	date_of_birth = request.form['date_of_birth']
	airline_name = request.form['airline_name']
	staff_phone = request.form['staff_phone']
	staff_email = request.form['staff_email']

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
		ins1 = 'INSERT INTO Airline_Staff VALUES(%s, %s, %s, %s, %s, %s)'
		cursor.execute(ins1, (user_name, staff_password, first_name, last_name, date_of_birth, airline_name))
		num_list = staff_phone.split(",")
		for num in num_list:
			ins2 = 'INSERT INTO staff_phone VALUES(%s, %s)'
			cursor.execute(ins2, (user_name, num))
			conn.commit()
		email_list = staff_email.split(",")
		for email in email_list:
			ins3 = 'INSERT INTO staff_email VALUES(%s, %s)'
			cursor.execute(ins3, (user_name, email))
			conn.commit()
		cursor.close()
		return render_template('index.html')

# return customer's total spending last year 
def spending_last_year():
	cursor = conn.cursor();
	email = session['customer_email']
	query = 'SELECT SUM(sold_price) AS total_last_year FROM Ticket NATURAL JOIN Customer WHERE customer_email = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) AND purchase_date <= CURRENT_DATE()'
	cursor.execute(query, (email))
	total_last_year = cursor.fetchone()
	if total_last_year == None:
		total_last_year = 0
	total_last_year = total_last_year['total_last_year']
	cursor.close()
	return total_last_year

# return customer's spending by month
def monthly_spending_last_year():
	cursor = conn.cursor();
	email = session['customer_email']
	spending = []
	# month 1
	query1 = 'SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH) AS start_date, DATE_SUB(CURRENT_DATE(), INTERVAL 5 MONTH) AS end_date, SUM(sold_price) AS total FROM Ticket NATURAL JOIN Customer WHERE customer_email = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH) AND purchase_date <= DATE_SUB(CURRENT_DATE(), INTERVAL 5 MONTH)'
	cursor.execute(query1, (email))
	# stores purchase date, sold_price of that month
	month1 = cursor.fetchone()
	# month 2
	query2 = 'SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 5 MONTH) AS start_date, DATE_SUB(CURRENT_DATE(), INTERVAL 4 MONTH) AS end_date, SUM(sold_price) AS total FROM Ticket NATURAL JOIN Customer WHERE customer_email = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 5 MONTH) AND purchase_date <= DATE_SUB(CURRENT_DATE(), INTERVAL 4 MONTH)'
	cursor.execute(query2, (email))
	# stores purchase date, sold_price of that month
	month2 = cursor.fetchone()
	# month 3
	query3 = 'SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 4 MONTH) AS start_date, DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH) AS end_date, SUM(sold_price) AS total FROM Ticket NATURAL JOIN Customer WHERE customer_email = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 4 MONTH) AND purchase_date <= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH)'
	cursor.execute(query3, (email))
	# stores purchase date, sold_price of that month
	month3 = cursor.fetchone()
	# month 4
	query4 = 'SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH) AS start_date, DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH) AS end_date, SUM(sold_price) AS total FROM Ticket NATURAL JOIN Customer WHERE customer_email = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH) AND purchase_date <= DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH)'
	cursor.execute(query4, (email))
	# stores purchase date, sold_price of that month
	month4 = cursor.fetchone()
	# month 5
	query5 = 'SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH) AS start_date, DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH) AS end_date, SUM(sold_price) AS total FROM Ticket NATURAL JOIN Customer WHERE customer_email = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH) AND purchase_date <= DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH)'
	cursor.execute(query5, (email))
	# stores purchase date, sold_price of that month
	month5 = cursor.fetchone()
	# month 6
	query6 = 'SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH) AS start_date, CURRENT_DATE() AS end_date, SUM(sold_price) AS total FROM Ticket NATURAL JOIN Customer WHERE customer_email = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH) AND purchase_date <= CURRENT_DATE()'
	cursor.execute(query6, (email))
	# stores purchase date, sold_price of that month
	month6 = cursor.fetchone()
	spending.append(month1)
	spending.append(month2)
	spending.append(month3)
	spending.append(month4)
	spending.append(month5)
	spending.append(month6)
	for item in spending:
		if item['total'] == None:
			item['total'] = 0
	cursor.close()
	return spending

#Customer home
#Author: Tianzuo Liu
@app.route('/customer_home')
def customer_home():
	customer_email = session['customer_email']
	total_last_year = spending_last_year()
	spending = monthly_spending_last_year()
	return render_template('customer_home.html', customer_email = customer_email, total_last_year = total_last_year, spending = spending)

#Customer view all future flights
#Author: Tianzuo Liu
@app.route('/customer_view_flights', methods=['GET', 'POST'])
def customer_view_flights():
	cursor = conn.cursor()
	customer_email = session['customer_email']
	total_last_year = spending_last_year()
	spending = monthly_spending_last_year()
	if request.method == 'POST':
		query ='SELECT * FROM Ticket NATURAL JOIN Flight WHERE customer_email = %s and departure_date >= CURDATE()'
		cursor.execute(query, (session['customer_email']))
		future_flights = cursor.fetchall()
		if(future_flights):
			return render_template('customer_home.html', future_flights = future_flights, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
		else:
			no_future_error = 'No future flight'
		return render_template('customer_home.html', no_future_error = no_future_error, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
	else:
		return render_template('customer_home.html', customer_email = customer_email, total_last_year = total_last_year, spending = spending)

#Customer searches for flights
#Author: Tianzuo Liu
'''
Search for future flights (one way or round trip) based on source city/airport name, 
destination city/airport name, dates (departure or return).
'''
# Input: departure airport, arrival airport, daparture date, arrival date
# Output: flight_number, departure_airport, departure date, arrival date, arrival airport
@app.route('/customer_search_flights', methods=['GET', 'POST'])
def customer_search_flights():
	cursor = conn.cursor()
	total_last_year = spending_last_year()
	spending = monthly_spending_last_year()
	if request.method == 'POST':
		dept_airport = request.form['departure_airport']
		arri_airport = request.form['arrival_airport']
		dept_date = request.form['departure_date']
		return_date = request.form['return_date']
		dept_city = request.form['departure_city']
		arri_city = request.form['arrival_city']
		customer_email = session['customer_email']
		# search one way by airport
		if dept_airport != "" and arri_airport != "" and dept_date != "" and return_date == "" and dept_city == "" and arri_city == "":
			query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time, arrival_airport, airline_name, base_price FROM Flight WHERE departure_date = %s AND departure_airport = %s AND arrival_airport = %s AND %s > CURRENT_DATE()'
			cursor.execute(query, (dept_date, dept_airport, arri_airport, dept_date))
			go_flights = cursor.fetchall()	
			if (go_flights):
				return render_template('customer_home.html', go_flights = go_flights, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
			else:
				noGoError = 'Sorry, no trip found.'
				return render_template('customer_home.html', noGoError = noGoError, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
		# search round trip by airport
		elif dept_airport != "" and arri_airport != "" and dept_date != "" and return_date != "" and dept_city == "" and arri_city == "":
			if dept_date > return_date:
				dateError = "Arrival date must be after departure date."
				return render_template('customer_home.html', customer_email = customer_email, total_last_year = total_last_year, spending = spending, dateError = dateError)
			query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time, arrival_airport, airline_name, base_price FROM Flight WHERE departure_date = %s AND departure_airport = %s AND arrival_airport = %s AND %s > CURRENT_DATE()'
			cursor.execute(query, (return_date, arri_airport, dept_airport, return_date))
			return_flights = cursor.fetchall()
			if (return_flights):
				query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time, arrival_airport, airline_name, base_price FROM Flight WHERE departure_date = %s AND departure_airport = %s AND arrival_airport = %s AND %s > CURRENT_DATE()'
				cursor.execute(query, (dept_date, dept_airport, arri_airport, dept_date))
				go_flights = cursor.fetchall()
				if (go_flights):
					return render_template('customer_home.html', return_flights = return_flights, go_flights = go_flights, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
				else:
					noGoError = 'Sorry, no trip found.'
					return render_template('customer_home.html', noGoError = noGoError, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
			else:
				noReturnError = 'Sorry, no return trip found.'
				return render_template('customer_home.html', noReturnError = noReturnError, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
		# search round trip by city
		elif dept_airport == "" and arri_airport == "" and dept_date != "" and return_date != "" and dept_city != "" and arri_city != "":
			if dept_date > return_date:
				dateError = "Arrival date must be after departure date."
				return render_template('customer_home.html', customer_email = customer_email, total_last_year = total_last_year, spending = spending, dateError = dateError)
			# check if there is a return trip
			query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time, arrival_airport, airline_name, base_price FROM Flight, Airport D, Airport A WHERE Flight.departure_airport = D.airport_name AND Flight.arrival_airport = A.airport_name AND D.airport_city = %s AND A.airport_city = %s AND departure_date = %s AND %s > CURRENT_DATE()'
			cursor.execute(query, (arri_city, dept_city, return_date, return_date))
			return_flights = cursor.fetchall()
			if (return_flights):
				query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time, arrival_airport, airline_name, base_price FROM Flight, Airport D, Airport A WHERE Flight.departure_airport = D.airport_name AND Flight.arrival_airport = A.airport_name AND D.airport_city = %s AND A.airport_city = %s AND departure_date = %s AND %s > CURRENT_DATE()'
				cursor.execute(query, (dept_city, arri_city, dept_date, dept_date))
				go_flights = cursor.fetchall()
				if (go_flights):
					return render_template('customer_home.html', return_flights = return_flights, go_flights = go_flights, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
				else:
					noGoError = 'Sorry, no trip found.'
					return render_template('customer_home.html', noGoError = noGoError, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
			else:
				noReturnError = 'Sorry, no return trip found.'
				return render_template('customer_home.html', noReturnError = noReturnError, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
		# search one way by airport
		elif dept_airport == "" and arri_airport == "" and dept_date != "" and return_date == "" and dept_city != "" and arri_city != "":
			query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time, arrival_airport, airline_name, base_price FROM Flight, Airport D, Airport A WHERE Flight.departure_airport = D.airport_name AND Flight.arrival_airport = A.airport_name AND D.airport_city = %s AND A.airport_city = %s AND departure_date = %s AND %s > CURRENT_DATE()'
			cursor.execute(query, (dept_city, arri_city, dept_date, dept_date))
			go_flights = cursor.fetchall()
			if(go_flights):
				return render_template('customer_home.html', go_flights = go_flights, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
			else:
				noGoError = 'Sorry, no trip found.'
				return render_template('customer_home.html', noGoError = noGoError, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
		elif dept_airport == "" and arri_airport == "" and dept_city != "" and arri_city != "":
			invalidSearchError = 'Please enter only departure/arrival city or departure/arrival airport'
			return render_template('customer_home.html', invalidSearchError = invalidSearchError, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
		else:
			invalidSearchError = 'Invalid data'
			return render_template('customer_home.html', invalidSearchError = invalidSearchError, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
	else:
		return render_template('customer_home.html', customer_email = customer_email, total_last_year = total_last_year, spending = spending)

#Customer purchases a ticket (from result of searching flight)
#Author: Tianzuo Liu
@app.route('/purchase_ticket', methods=['GET', 'POST'])
def purchase_ticket():
	cursor = conn.cursor()
	total_last_year = spending_last_year()
	spending = monthly_spending_last_year()
	if request.method == 'POST':
		flight_number = request.form['flight_number']
		dept_date = request.form['departure_date']
		dept_time = request.form['departure_time']
		airline_name = request.form['airline_name']
		card_type = request.form['card_type']
		card_number = request.form['card_number']
		expiration_date = request.form['expiration_date']
		name_on_card = request.form['name_on_card']
		customer_email = session['customer_email']
		# check if the flight to purchase exists
		query = 'SELECT * FROM Flight WHERE flight_number = %s AND departure_date = %s AND departure_time = %s AND airline_name = %s'
		cursor.execute(query, (flight_number, dept_date, dept_time, airline_name))
	
		new_data = cursor.fetchone()
		ticket_ID = str(random.randint(100000,200000))

		if (new_data):
			query = 'SELECT base_price FROM Flight WHERE flight_number = %s AND departure_date = %s AND departure_time = %s AND airline_name = %s AND departure_date > CURRENT_DATE()'
			cursor.execute(query, (flight_number, dept_date, dept_time, airline_name))
			data = cursor.fetchone()
			# The sold price may be different from the base price. Handle the price increase mechanism.
			query = 'SELECT COUNT(ticket_ID) FROM Ticket NATURAL JOIN Airplane NATURAL JOIN Flight WHERE flight_number = %s'
			cursor.execute(query, (flight_number))
			count_num = cursor.fetchone()
			query = 'SELECT number_seats FROM Flight NATURAL JOIN Airplane WHERE flight_number = %s'
			cursor.execute(query, (flight_number))
			num_seats = cursor.fetchone()
			sold_price = data['base_price']

			# Should return error message if the card expiration date has passed.
			if(datetime.datetime.now() > datetime.datetime.strptime(expiration_date, "%Y-%m-%d")):
				card_exp_error = 'Sorry, the card expiration date has passed!'
				return render_template('customer_home.html', card_exp_error = card_exp_error, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
			# Should return error message if the tickets of the flight is fully booked.
			if(count_num['COUNT(ticket_ID)'] == (int(num_seats['number_seats']))):
				no_ticket_error = 'Sorry, there is no ticket!'
				return render_template('customer_home.html', no_ticket_error = no_ticket_error, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
			elif(count_num['COUNT(ticket_ID)'] >= (int(num_seats['number_seats']) * 0.6)):
				sold_price = float(data['base_price'])
				sold_price *= 1.2
			insertion = 'INSERT INTO Ticket VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIME(), CURRENT_TIME(), %s, %s, %s, %s)'
			cursor.execute(insertion, (ticket_ID, customer_email, sold_price, card_type, card_number, \
				name_on_card, expiration_date, dept_date, dept_time,flight_number, airline_name))
			conn.commit()
			purchase = 'INSERT INTO Purchase VALUES(%s, %s)'
			cursor.execute(purchase, (customer_email, ticket_ID))
			conn.commit()
			cursor.close()
			total_last_year = spending_last_year()
			spending = monthly_spending_last_year()
			purchase_message = 'Successfully purchased ticket'
			return render_template('customer_home.html', purchase_message = purchase_message, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
		else:
			no_purchase_error = 'Something wrong. Please try again'
			return render_template('customer_home.html', no_purchase_error = no_purchase_error, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
	else:
		return render_template('customer_home.html', customer_email = customer_email, total_last_year = total_last_year, spending = spending)



#Customer cancels a trip
#Author: Tianzuo Liu
@app.route('/cancel_trip', methods=['GET', 'POST'])
def cancel_trip():
	cursor = conn.cursor()
	total_last_year = spending_last_year()
	spending = monthly_spending_last_year()
	if request.method == 'POST':
		flight_number = request.form['flight_number']
		departure_date = request.form['departure_date']
		departure_time = request.form['departure_time']
		airline_name = request.form['airline_name']
		customer_email = session['customer_email']
		query = 'SELECT ticket_ID FROM Ticket NATURAL JOIN Flight WHERE customer_email = %s and departure_date = %s and flight_number = %s and departure_time = %s and airline_name = %s and departure_date >= CURDATE()'
		cursor.execute(query, (session['customer_email'], departure_date, flight_number, departure_time, airline_name))
		data = cursor.fetchone()
		if(data):
			dep_date = datetime.datetime.strptime(departure_date, "%Y-%m-%d")
			dep_time = datetime.datetime.strptime(departure_time, "%H:%M")
			com_date = datetime.datetime.combine(dep_date.date(), dep_time.time())
			now_date = datetime.datetime.now()
			now_date += datetime.timedelta(days=1)
			if(now_date < com_date):
				query = 'DELETE FROM Purchase WHERE ticket_ID = %s'
				cursor.execute(query, (data['ticket_ID']))
				conn.commit()
				query = 'DELETE FROM Ticket WHERE ticket_ID = %s'
				cursor.execute(query, (data['ticket_ID']))
				conn.commit()
				cursor.close()
				total_last_year = spending_last_year()
				spending = monthly_spending_last_year()
				cancel_message = 'Successfully cancelled the trip'
				return render_template("customer_home.html", cancel_message = cancel_message, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
			else:
				no_cancel_error = 'Could not cancel the flight, since the date is less than 24 hour'
				return render_template('customer_home.html', no_cancel_error = no_cancel_error, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
		else:
			no_cancel_error = 'Could not cancel the flight'
			return render_template('customer_home.html', no_cancel_error = no_cancel_error, customer_email = customer_email, total_last_year = total_last_year, spending = spending)
	else:
		return render_template('customer_home.html', customer_email = customer_email, total_last_year = total_last_year, spending = spending)

# Customer gives rating and comment
# Author: Yanglin Tao
'''
Customer will be able to rate and comment on their 
previous flights (for which he/she purchased tickets and already took that flight) for the airline they 
logged in.
'''
# input: flight_number, departure date, departure time, airline name
# output: none
@app.route('/customer_rating', methods=['GET', 'POST'])
def customer_rating():
	cursor = conn.cursor();
	# display default data
	total_last_year = spending_last_year()
	spending = monthly_spending_last_year()
	customer_email = session['customer_email']
	if request.method == 'POST':
		flight_num = request.form['flight_number']
		dept_date = request.form['departure_date']
		dept_time = request.form['departure_time']
		airline = request.form['airline_name']
		rate = request.form['rating']
		comm = request.form['comment']
		# check if the flight is in the customer's past flights
		query = 'SELECT * FROM Customer NATURAL JOIN Ticket WHERE customer_email = %s AND flight_number = %s AND departure_date = %s AND departure_time = %s AND airline_name = %s AND %s < CURRENT_DATE()'
		cursor.execute(query, (customer_email, flight_num, dept_date, dept_time, airline, dept_date))
		data = cursor.fetchone()
		if(data):
			# check if the customer already commented the trip
			query = 'SELECT * FROM Taken WHERE customer_email = %s AND flight_number = %s AND departure_date = %s AND departure_time = %s AND airline_name = %s'
			cursor.execute(query, (customer_email, flight_num, dept_date, dept_time, airline))
			comment = cursor.fetchone()
			if(comment):
				commentExistError = 'Sorry, this flight has already been commented or rated. Please try another.'
				return render_template('customer_home.html', commentExistError = commentExistError, total_last_year = total_last_year, spending = spending, customer_email = customer_email)
			else:
				query = 'INSERT INTO Taken VALUES(%s, %s, %s, %s, %s, %s, %s)'
				cursor.execute(query, (customer_email, airline, rate, comm, flight_num, dept_date, dept_time))
				conn.commit()
				cursor.close()
				commentSucc = 'Thanks for your feedback!'
				return render_template('customer_home.html', commentSucc = commentSucc, total_last_year = total_last_year, spending = spending, customer_email = customer_email)
		else:
			noFlightError = 'There is no flight or past flight you are looking for. Please try again.'
			return render_template('customer_home.html', noFlightError = noFlightError, total_last_year = total_last_year, spending = spending, customer_email = customer_email)
	else: 
		return render_template('customer_home.html', customer_email = customer_email)

# Customer tracks spending
# Author: Yanglin Tao
'''
Default view will be total amount of money spent in the past year and a bar
chart/table showing month wise money spent for last 6 months. He/she will also have option to specify 
a range of dates to view total amount of money spent within that range and a bar chart/table showing 
month wise money spent within that range
'''
# default output: total_last_year, monthly_spending_last_year
# input: start_date, end_date
# output: total_spending, monthly_spending
@app.route('/track_spending', methods=['GET', 'POST'])
def track_spending():
	cursor = conn.cursor();
	email = session['customer_email']
	total_last_year = spending_last_year()
	spending = monthly_spending_last_year()
	if request.method == 'POST':
		start = request.form['start_date']
		end = request.form['end_date']
		if start != "" and end != "":
			query = 'SELECT %s AS start_date, %s AS end_date, SUM(sold_price) AS total FROM Ticket NATURAL JOIN Customer WHERE customer_email = %s AND purchase_date >= %s AND purchase_date <= %s'
			cursor.execute(query, (start, end, email, start, end))
			# stores purchase date, sold_price in a given date range
			spending = cursor.fetchall()
		cursor.close()
		return render_template('customer_home.html', customer_email = email, spending = spending, total_last_year = total_last_year)
	else:
		return render_template('customer_home.html', customer_email = email, total_last_year = total_last_year)

# Customer logout
# Author: Yanglin Tao
'''
Customer logs out of the system
'''
# input: none
# output: none
@app.route('/customer_logout')
def customer_logout():
	del session['customer_email']
	return render_template('customer_logout.html')

# Default show all airplanes
# Author: Yanglin Tao
def default_show_all_airplanes():
	cursor = conn.cursor();
	user_name = session['user_name']
	# find which airline it is 
	query = 'SELECT airline_name FROM Airline_staff WHERE user_name = %s'
	cursor.execute(query, (user_name))
	data = cursor.fetchone()
	airline = data['airline_name']
	query = 'SELECT airplane_identification_number, number_seats, manufacture_company, age, airline_name FROM Airplane WHERE airline_name = %s'
	cursor.execute(query, (airline))
	airplanes = cursor.fetchall()
	cursor.close()
	return airplanes

# Default show all flights in the next 30 days
# Author: Yanglin Tao
def default_view_30days():
	cursor = conn.cursor();
	user_name = session['user_name']
	# find which airline it is 
	query = 'SELECT airline_name FROM Airline_staff WHERE user_name = %s'
	cursor.execute(query, (user_name))
	data = cursor.fetchone()
	airline = data['airline_name']
	query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time, arrival_airport FROM Flight WHERE departure_date >= CURRENT_DATE() AND departure_date <= DATE_ADD(CURRENT_DATE(), INTERVAL 30 DAY) AND airline_name = %s'
	cursor.execute(query, (airline))
	flights = cursor.fetchall()
	for i in range(len(flights)):
		flight_num = flights[i]['flight_number']
		dept_date = flights[i]['departure_date']
		dept_time = flights[i]['departure_time']
		query = 'SELECT customer_email FROM Ticket WHERE flight_number = %s AND departure_date = %s AND departure_time = %s AND airline_name = %s'
		cursor.execute(query, (flight_num, dept_date, dept_time, airline))
		customers = cursor.fetchall()
		customer_list = []
		for j in range(len(customers)):
			customer_list.append(customers[j]['customer_email'])
		customer_email_str = ", ".join(customer_list)
		flights[i]['customer_email'] = customer_email_str
	cursor.close()
	return flights

# Staff home
# Author: Yanglin Tao
@app.route('/staff_home')
def staff_home():
	user_name = session['user_name']
	airplanes = default_show_all_airplanes()
	flights = default_view_30days()
	return render_template('staff_home.html', user_name = user_name, airplanes = airplanes, flights = flights)

# Staff views flights
# Author: Yanglin Tao
'''
Defaults will be showing all the future flights operated by the airline he/she works for 
the next 30 days. He/she will be able to see all the current/future/past flights operated by the airline 
he/she works for based range of dates, source/destination airports/city etc. He/she will be able to see 
all the customers of a particular flight.
'''
# default output: next_30day_flights(flight_number, departure_date, departure_time, departure_airport, arrival_date, 
# 			arrival_time, arrival_airport, customers)
# input: start_date, end_date, departure_airport, departure_city, arrival_airport, arrival_city
# output: flight_number, departure_date, departure_time, departure_airport, arrival_date, 
# 			arrival_time, arrival_airport, customers
@app.route('/staff_view_flights', methods=['GET', 'POST'])
def staff_view_flights():
	cursor = conn.cursor();
	user_name = session['user_name']
	airplanes = default_show_all_airplanes()
	flights = default_view_30days()
	if request.method == 'POST':
		start = request.form['start_date']
		end = request.form['end_date']
		dept_airport = request.form['departure_airport']
		arri_airport = request.form['arrival_airport']
		dept_city = request.form['departure_city']
		arri_city = request.form['arrival_city']
		# find which airline it is 
		query = 'SELECT airline_name FROM Airline_staff WHERE user_name = %s'
		cursor.execute(query, (user_name))
		data = cursor.fetchone()
		airline = data['airline_name']
		# if there are inputs from user that specifies start_date, end_date, departure_airport, departure_city, 
		# arrival_airport, and arrival_city
		if start == "" and end != "" and dept_airport == "" and arri_airport == "" and dept_city == "" and arri_city == "":
			return render_template('staff_home.html', user_name = user_name, flights = flights, airplanes = airplanes)
		if start != "" and end != "" and dept_airport != "" and arri_airport != "" and dept_city == "" and arri_city == "":
			query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time, arrival_airport FROM Flight WHERE departure_date >= %s AND departure_date <= %s AND departure_airport = %s AND arrival_airport = %s AND airline_name = %s'
			cursor.execute(query, (start, end, dept_airport, arri_airport, airline))
			flights = cursor.fetchall()
			for i in range(len(flights)):
				flight_num = flights[i]['flight_number']
				dept_date = flights[i]['departure_date']
				dept_time = flights[i]['departure_time']
				query = 'SELECT customer_email FROM Ticket WHERE flight_number = %s AND departure_date = %s AND departure_time = %s AND airline_name = %s'
				cursor.execute(query, (flight_num, dept_date, dept_time, airline))
				customers = cursor.fetchall()
				customer_list = []
				for j in range(len(customers)):
					customer_list.append(customers[j]['customer_email'])
				customer_email_str = ", ".join(customer_list)
				flights[i]['customer_email'] = customer_email_str
			cursor.close()
			return render_template('staff_home.html', user_name = user_name, flights = flights, airplanes = airplanes)
		elif start != "" and end != "" and dept_airport == "" and arri_airport == "" and dept_city != "" and arri_city != "":
			query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time, arrival_airport FROM Flight, Airport D, Airport A WHERE Flight.departure_airport = D.airport_name AND Flight.arrival_airport = A.airport_name AND D.airport_city = %s AND A.airport_city = %s AND departure_date >= %s AND departure_date <= %s AND airline_name = %s'
			cursor.execute(query, (dept_city, arri_city, start, end, airline))
			flights = cursor.fetchall()
			cursor.close()
			return render_template('staff_home.html', user_name = user_name, flights = flights, airplanes = airplanes)
		else:
			mismatchError = 'Please enter only departure/arrival city or departure/arrival airport.'
			return render_template('staff_home.html', user_name = user_name, mismatchError = mismatchError, airplanes = airplanes)

	else:
		return render_template('staff_home.html', user_name = user_name, flights = flights, airplanes = airplanes)

# Staff creates new flights
# Author: Yanglin Tao
'''
He or she creates a new flight, providing all the needed data, via forms. The 
application should prevent unauthorized users from doing this action. Defaults will be showing all the 
future flights operated by the airline he/she works for the next 30 days.
'''
# default output: next_30day_flights(flight_number, departure_date, departure_time, departure_airport, arrival_date, 
# 			arrival_time, arrival_airport)
# input: flight_number, departure_airport, departure_date, departure_time, arrival_airport, arrival_date, 
# 			arrival_time, airplane_identification_number, airline_name
# output: none
@app.route('/add_flight', methods=['GET', 'POST'])
def add_flight():
	cursor = conn.cursor();
	user_name = session['user_name']
	airplanes = default_show_all_airplanes()
	flights = default_view_30days()
	if request.method == 'POST':
		flight_num = request.form['flight_number']
		dept_airport = request.form['departure_airport']
		dept_date = request.form['departure_date']
		dept_time = request.form['departure_time']
		arri_airport = request.form['arrival_airport']
		arri_date = request.form['arrival_date']
		arri_time = request.form['arrival_time']
		airplane_identifi_num = request.form['airplane_identification_number']
		b_price = request.form['base_price']
		# find which airline it is 
		query = 'SELECT airline_name FROM Airline_staff WHERE user_name = %s'
		cursor.execute(query, (user_name))
		data = cursor.fetchone()
		airline = data['airline_name']
		# check if this is an existing flight
		query = 'SELECT * FROM Flight WHERE flight_number = %s AND departure_date = %s AND departure_time = %s AND airline_name = %s'
		cursor.execute(query, (flight_num, dept_date, dept_time, airline))
		data = cursor.fetchone()
		if(data):
			flightExistError = "This is an existing flight, try another"
			return render_template('staff_home.html', user_name = user_name, flightExistError = flightExistError, airplanes = airplanes, flights = flights)
		else:
			# check if departure and arrival airports are the same
			if dept_airport == arri_airport:
				sameAirportError = 'Departure airport and arrival airport cannot be the same'
				return render_template('staff_home.html', user_name = user_name, sameAirportError = sameAirportError, airplanes = airplanes, flights = flights)
			# check if departure_date and time < arrival_date and time exist in the system
			dep_date = datetime.datetime.strptime(dept_date, "%Y-%m-%d")
			dep_time = datetime.datetime.strptime(dept_time, "%H:%M")
			com_date = datetime.datetime.combine(dep_date.date(), dep_time.time())
			arr_date = datetime.datetime.strptime(arri_date, "%Y-%m-%d")
			arr_time = datetime.datetime.strptime(arri_time, "%H:%M")
			com_date2 = datetime.datetime.combine(arr_date.date(), arr_time.time())
			now_date = datetime.datetime.now()
			if(com_date < now_date):
				pastFlightError = 'Cannot create a flight in the past'
				return render_template('staff_home.html', user_name = user_name, pastFlightError = pastFlightError, airplanes = airplanes, flights = flights)
			if(com_date < com_date2):
				# check if the airplane exist in the system
				query = 'SELECT * FROM Airplane WHERE airplane_identification_number = %s AND airline_name = %s'
				cursor.execute(query, (airplane_identifi_num, airline))
				planeExist = cursor.fetchone()
				if (planeExist):
					query = 'INSERT INTO Flight (flight_number, departure_airport, departure_date, departure_time, arrival_airport, arrival_date, arrival_time, airplane_identification_number, base_price, airline_name, flight_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)'
					cursor.execute(query, (flight_num, dept_airport, dept_date, dept_time, arri_airport, arri_date, arri_time, airplane_identifi_num, b_price, airline))
					conn.commit()
					cursor.close()
					addFlightSucc = "Sucessfully added a flight"
					flights = default_view_30days()
					return render_template('staff_home.html', user_name = user_name, addFlightSucc = addFlightSucc, airplanes = airplanes, flights = flights)
				else:
					noPlaneError = 'This is a new airplane. Please add to the system first or try another.'
					return render_template('staff_home.html', user_name = user_name, noPlaneError = noPlaneError, airplanes = airplanes, flights = flights)
			else:
				departureDateError = 'Departure date time can not be greater than arrival date time. Please check again.'
				return render_template('staff_home.html', user_name = user_name, departureDateError = departureDateError, airplanes = airplanes, flights = flights)

	else:
		return render_template('staff_home.html', user_name = user_name, airplanes = airplanes, flights = flights)

# Staff changes status of the flight
# Author: Yanglin Tao
'''
He or she changes a flight status (from on-time to delayed or vice versa) via 
forms.
'''
# input: flight_number, departure_date, departure_time, airline_name, status
# output: none
@app.route('/change_status', methods=['GET', 'POST'])
def change_status():
	cursor = conn.cursor();
	user_name = session['user_name']
	airplanes = default_show_all_airplanes()
	flights = default_view_30days()
	if request.method == 'POST':
		flight_num = request.form['flight_number']
		dept_date = request.form['departure_date']
		dept_time = request.form['departure_time']
		airline = request.form['airline_name']
		new_status = request.form['flight_status']
		query = 'SELECT * FROM Flight WHERE flight_number = %s AND departure_date = %s AND departure_time = %s AND airline_name = %s'
		cursor.execute(query, (flight_num, dept_date, dept_time, airline))
		data = cursor.fetchone()
		if (data):
			query = 'UPDATE Flight SET flight_status = %s WHERE flight_number = %s AND departure_date = %s AND departure_time = %s AND airline_name = %s' 
			cursor.execute(query, (new_status, flight_num, dept_date, dept_time, airline))
			conn.commit()
			cursor.close()
			changeStatusSucc = "Successfully changed the flight status"
			return render_template('staff_home.html', user_name = user_name, changeStatusSucc = changeStatusSucc, airplanes = airplanes, flights = flights)
		else:
			changeStatusError = "Sorry, cannot find the flight"
			return render_template('staff_home.html', user_name = user_name, changeStatusError = changeStatusError, airplanes = airplanes, flights = flights)
	else:
		return render_template('staff_home.html', user_name = user_name, airplanes = airplanes, flights = flights)

# Staff adds new airplane in the system
# Author: Yanglin Tao
'''
He or she adds a new airplane, providing all the needed data, via forms. 
The application should prevent unauthorized users from doing this action. In the confirmation page, 
she/he will be able to see all the airplanes owned by the airline he/she works for.
'''
# default output: all_airplanes(airplane_identification_number, number_of_seats, manufacture_company, age, airline_name)
# input: airplane_identification_number, number_of_seats, manufacture_company, age, airline_name
# output: none
@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
	cursor = conn.cursor();
	user_name = session['user_name']
	airplanes = default_show_all_airplanes()
	flights = default_view_30days()
	if request.method == 'POST':
		airplane_identifi_num = request.form['airplane_identification_number']
		num_of_seats = request.form['number_seats']
		manufact_comp = request.form['manufacture_company']
		airplane_age = request.form['age']
		# find which airline it is 
		query = 'SELECT airline_name FROM Airline_staff WHERE user_name = %s'
		cursor.execute(query, (user_name))
		data = cursor.fetchone()
		airline = data['airline_name']
		# check if an airplane already exist in the system
		query = 'SELECT * FROM Airplane WHERE airplane_identification_number = %s AND airline_name = %s'
		cursor.execute(query, (airplane_identifi_num, airline))
		data = cursor.fetchone()
		if (data):
			planeExistError = "Sorry, this plane already exists. Please try another."
			return render_template('staff_home.html', user_name = user_name, planeExistError = planeExistError, airplanes = airplanes, flights = flights)
		else:
			query = 'INSERT INTO Airplane (airplane_identification_number, number_seats, manufacture_company, age, airline_name) VALUES (%s, %s, %s, %s, %s)'
			cursor.execute(query, (airplane_identifi_num, num_of_seats, manufact_comp, airplane_age, airline))
			conn.commit()
			cursor.close()
			addPlaneSucc = 'Successfully added a plane'
			airplanes = default_show_all_airplanes()
			return render_template('staff_home.html', user_name = user_name, addPlaneSucc = addPlaneSucc, airplanes = airplanes, flights = flights)
	else:
		return render_template('staff_home.html', user_name = user_name, flights = flights, airplanes = airplanes)

#Staff adds new airport in the system
#Author: Justin Li
@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
	cursor = conn.cursor();
	user_name = session['user_name']
	airplanes = default_show_all_airplanes()
	flights = default_view_30days()
	if request.method == 'POST':
		airport_name = request.form['airport_name']
		airport_city = request.form['airport_city']
		airport_cout = request.form['airport_country']
		airport_type = request.form['airport_type']
		if airport_name != None and airport_city != None and airport_cout != None and airport_type != None:
			query = 'SELECT * FROM Airport WHERE airport_name = %s'
			cursor.execute(query, (airport_name))
			data = cursor.fetchone()
			if (data):
				airportExistError = "Sorry, this airport already exist. Please try another one."
				return render_template('staff_home.html', user_name = user_name, airportExistError = airportExistError, airplanes = airplanes, flights = flights)
			else:
				query = 'INSERT INTO AIRPORT (airport_name, airport_city, airport_country, airport_type) VALUES (%s, %s, %s, %s)'
				cursor.execute(query, (airport_name, airport_city, airport_cout, airport_type))
				conn.commit()
				cursor.close()
				addAirportSucc = 'Successfully added an airport'
				return render_template('staff_home.html', user_name = user_name , addAirportSucc = addAirportSucc, airplanes = airplanes, flights = flights)
	else:
		return render_template('staff_home.html', user_name = user_name)

#Staff views the rating and comments of the flight, along with the average rating
#Author: Justin Li
@app.route('/view_rating', methods=['GET', 'POST'])
def view_rating():
	cursor = conn.cursor();
	user_name = session['user_name']
	airplanes = default_show_all_airplanes()
	flights = default_view_30days()
	if request.method == 'POST':
		flight_number = request.form['flight_number']
		dept_date = request.form['departure_date']
		dept_time = request.form['departure_time']
		# find out which airline it is
		query = 'SELECT airline_name FROM Airline_staff WHERE user_name = %s'
		cursor.execute(query, (user_name))
		data = cursor.fetchone()
		airline = data['airline_name']
		if flight_number != "" and dept_date != "" and dept_time != "":
			query = 'SELECT rating, comment FROM Taken WHERE flight_number = %s AND departure_date = %s AND departure_time = %s AND airline_name = %s'
			cursor.execute(query, (flight_number, dept_date, dept_time, airline))
			rating_comment = cursor.fetchall()
			if (rating_comment):
				query = 'SELECT AVG(rating) AS average_rating FROM Taken WHERE flight_number = %s AND departure_date = %s AND departure_time = %s AND airline_name = %s'
				cursor.execute(query, (flight_number, dept_date, dept_time, airline))
				avg_rating = cursor.fetchone()
				average_rating = avg_rating['average_rating']
				cursor.close()
				return render_template('staff_home.html', user_name = user_name, rating_comment = rating_comment, average_rating = average_rating, airplanes = airplanes, flights = flights)
			else:
				invalidFlightError = 'This flight either does not exist or has no ratings or comments yet.'
				return render_template('staff_home.html', user_name = user_name, invalidFlightError = invalidFlightError, airplanes = airplanes, flights = flights)
		else:
			noDataError = 'Please specify a flight'
			return render_template('staff_home.html', user_name = user_name, noDataError = noDataError, airplanes = airplanes, flights = flights)
	else:
		return render_template('staff_home.html', user_name = user_name)


#Staff views the most frequent customer
#Author: Justin Li
@app.route('/frequent_customer', methods=['GET', 'POST'])
def frequent_customer():
	cursor = conn.cursor();
	user_name = session['user_name']
	airplanes = default_show_all_airplanes()
	flights = default_view_30days()
	if request.method == 'POST':
		# find out which airline it is
		query = 'SELECT airline_name FROM Airline_staff WHERE user_name = %s'
		cursor.execute(query, (user_name))
		data = cursor.fetchone()
		airline = data['airline_name']
		# query = 'CREATE VIEW last_year_customers AS SELECT * FROM Customer NATURAL JOIN Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR); SELECT customer_email, COUNT(ticket_ID) AS frequency FROM last_year_customers GROUP BY customer_email ORDER BY frequency DESC LIMIT 1'
		query = 'SELECT customer_email, COUNT(ticket_ID) AS frequency FROM Customer NATURAL JOIN Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) GROUP BY customer_email ORDER BY frequency DESC LIMIT 1'
		cursor.execute(query, (airline))
		data = cursor.fetchone()
		freq_customer = data['customer_email']
		cursor.close()
		return render_template('staff_home.html', user_name = user_name, freq_customer = freq_customer, airplanes = airplanes, flights = flights)
	else:
		return render_template('staff_home.html', user_name = user_name, airplanes = airplanes, flights = flights)

#Staff views all flights of a customer
#Author: Justin Li
@app.route('/view_customer_flights', methods=['GET', 'POST'])
def view_customer_flights():
	cursor = conn.cursor();
	user_name = session['user_name']
	airplanes = default_show_all_airplanes()
	flights = default_view_30days()
	if request.method == 'POST':
		customer_email = request.form['customer_email']
		# find out which airline it is
		query = 'SELECT airline_name FROM Airline_staff WHERE user_name = %s'
		cursor.execute(query, (user_name))
		data = cursor.fetchone()
		airline = data['airline_name']
		if customer_email != "":
			query = 'SELECT * FROM Customer NATURAL JOIN Ticket NATURAL JOIN Flight WHERE customer_email = %s AND airline_name = %s'
			cursor.execute(query, (customer_email, airline))
			customer_flights = cursor.fetchall()
			cursor.close()
			return render_template('staff_home.html', user_name = user_name, customer_flights = customer_flights, airplanes = airplanes, flights = flights)
		else:
			noEmailError = 'Please sepcify a customer email'
			return render_template('staff_home.html', user_name = user_name, noEmailError = noEmailError, airplanes = airplanes, flights = flights)
	else:
		return render_template('staff_home.html', user_name = user_name, airplanes = airplanes, flights = flights)

#Staff views reports
#Author: Justin Li
@app.route('/view_reports', methods=['GET', 'POST'])
def view_reports():
	cursor = conn.cursor()
	user_name = session['user_name']
	airplanes = default_show_all_airplanes()
	flights = default_view_30days()
	if request.method == 'POST':
		start = request.form['start_date']
		end = request.form['end_date']
		query = 'SELECT airline_name FROM Airline_staff WHERE user_name = %s'
		cursor.execute(query, (user_name))
		data = cursor.fetchone()
		airline = data['airline_name']
		if start != "" and end != "":
			query = 'SELECT COUNT(ticket_id) AS num_tickets FROM Ticket WHERE airline_name = %s AND purchase_date >= %s AND purchase_date <= %s'
			cursor.execute(query, (airline, start, end))
			data = cursor.fetchone()
			custom_num_tickets = data['num_tickets']
			cursor.close()
			return render_template('staff_home.html', user_name = user_name, custom_num_tickets = custom_num_tickets, start_date = start, end_date = end, airplanes = airplanes, flights = flights)
		elif start == "" and end == "":
			query = 'SELECT COUNT(ticket_id) AS num_tickets FROM Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) AND purchase_date <= CURRENT_DATE()'
			cursor.execute(query, (airline))
			data = cursor.fetchone()
			last_year_num = data['num_tickets']
			query = 'SELECT COUNT(ticket_id) AS num_tickets FROM Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH) AND purchase_date <= CURRENT_DATE()'
			cursor.execute(query, (airline))
			data = cursor.fetchone()
			last_month_num = data['num_tickets']
			return render_template('staff_home.html', user_name = user_name, last_year_num = last_year_num, last_month_num = last_month_num, airplanes = airplanes, flights = flights)
		else:
			noDateError = 'Please specify a correct date range'
			return render_template('staff_home.html', user_name = user_name, noDateError = noDateError, airplanes = airplanes, flights = flights)
	else:
		return render_template('staff_home.html', user_name = user_name)

#Staff views earned revenue
#Author: Justin Li
@app.route('/view_revenue', methods=['GET', 'POST'])
def view_revenue():
	cursor = conn.cursor()
	user_name = session['user_name']
	airplanes = default_show_all_airplanes()
	flights = default_view_30days()
	if request.method == 'POST':
		# find out which airline it is
		query = 'SELECT airline_name FROM Airline_staff WHERE user_name = %s'
		cursor.execute(query, (user_name))
		data = cursor.fetchone()
		airline = data['airline_name']
		query = 'SELECT SUM(sold_price) AS year_revenue FROM Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) AND purchase_date <= CURRENT_DATE()'
		cursor.execute(query, (airline))
		data1 = cursor.fetchone()
		last_year_revenue = data1['year_revenue']
		query = 'SELECT SUM(sold_price) AS month_revenue FROM Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH) AND purchase_date <= CURRENT_DATE()'
		cursor.execute(query, (airline))
		data2 = cursor.fetchone()
		last_month_revenue = data2['month_revenue']
		return render_template('staff_home.html', user_name=user_name, last_year_revenue=last_year_revenue, last_month_revenue=last_month_revenue, airplanes = airplanes, flights = flights)
	else:
		return render_template('staff_home.html', user_name = user_name, airplanes = airplanes, flights = flights)

#Staff logout
#Author: Justin Li
@app.route('/staff_logout', methods=['GET', 'POST'])
def staff_logout():
	if request.method == 'POST':
		del session['user_name']
		return render_template('staff_logout.html')
	else:
		return render_template('staff_home.html')


app.secret_key = 'some key that you will never guess'

#Run the app on localhost port 5000
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)

