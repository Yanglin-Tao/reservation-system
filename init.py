#Import Flask Library
from email import message
import email
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
# test: pass
@app.route('/')
def hello():
	return render_template('index.html')

#Show all future flights to anyone using the system
#Author: Yanglin Tao
# test: pass
@app.route('/general_show_flights', methods=['GET', 'POST'])
def general_show_flights():
	cursor = conn.cursor()
	if request.method == 'POST':
		dept_airport = request.form['departure_airport']
		arri_airport = request.form['arrival_airport']
		dept_date = request.form['departure_date']
		arri_date = request.form['arrival_date']
		if dept_airport != None and arri_airport != None and dept_date != None and arri_date != None:
			query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time, arrival_airport FROM Flight WHERE departure_date = %s AND departure_airport = %s AND arrival_date = %s AND arrival_airport = %s AND %s > CURRENT_DATE()'
			cursor.execute(query, (dept_date, dept_airport, arri_date, arri_airport, dept_date))
			data = cursor.fetchall()	
			cursor.close()
			return render_template('index.html', flights = data)
		else:
			error = 'Invalid data'
			return render_template('index.html', error=error)
	else:
		return render_template('index.html')

#Check flight status to anyone using the system
#Author: Yanglin Tao
# test: pass
@app.route('/general_check_status', methods=['GET', 'POST'])
def general_check_status():
	cursor = conn.cursor()
	if request.method == 'POST':
		airline = request.form['airline_name']
		flight_num = request.form['flight_number']
		dept_date = request.form['departure_date']
		arri_date = request.form['arrival_date']
		if airline != None and flight_num != None and dept_date != None and arri_date != None:
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
# test: pass
@app.route('/customer_login')
def customer_login():
	return render_template('customer_login.html')

#Define route for customer register
#Author: Yanglin Tao
# test: pass
@app.route('/customer_register')
def customer_register():
	return render_template('customer_register.html')

#Define route for staff login
#Author: Yanglin Tao
# test: pass
@app.route('/staff_login')
def staff_login():
	return render_template('staff_login.html')

#Define route for staff register
#Author: Yanglin Tao
# test: pass
@app.route('/staff_register')
def staff_register():
	return render_template('staff_register.html')

#Authenticates customer login
#Author: Yanglin Tao
# test: pass
@app.route('/customer_login_auth', methods=['GET', 'POST'])
def customer_login_auth():
	#grabs information from the forms
	email = request.form['customer_email']
	password = request.form['customer_password']
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

#TODO: Authenticates staff login
#Author: Tianzuo Liu
# test: pass
@app.route('/staff_login_auth', methods=['GET', 'POST'])
def staff_login_auth():
	if request.method == 'POST':
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
			error = 'Invalid username or password'
			return render_template('staff_login.html', error=error)
	else:
		return render_template('staff_login.html')


#TODO: Authenticates customer register
#Author: Tianzuo Liu
# test: pass
@app.route('/customer_register_auth', methods=['GET', 'POST'])
def customer_register_auth():
	customer_name = request.form['customer_name']
	customer_email = request.form['customer_email']
	customer_password = request.form['customer_password']
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

#TODO: Authenticates staff register
#Author: Tianzuo Liu
# test: pass
@app.route('/staff_register_auth', methods=['GET', 'POST'])
def staff_register_auth():
	user_name = request.form['user_name']
	staff_password = request.form['staff_password']
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

#TODO: Customer home
#Author: Tianzuo Liu
# test: pass
@app.route('/customer_home')
def customer_home():
	customer_email = session['customer_email']
	total_last_year = spending_last_year()
	spending = monthly_spending_last_year()
	return render_template('customer_home.html', customer_email = customer_email, total_last_year = total_last_year, spending = spending)

#TODO: Customer view all future flights
#Author: Tianzuo Liu
@app.route('/customer_view_flights', methods=['GET', 'POST'])
def customer_view_flights():
	cursor = conn.cursor()
	customer_email = session['customer_email']
	if request.method == 'POST':

		query ='SELECT * FROM Ticket NATURAL JOIN Flight WHERE customer_email = %s and departure_date >= CURDATE()'
		cursor.execute(query, (session['customer_email']))
		future_flights = cursor.fetchall()

		if(future_flights):
			return render_template('customer_home.html', future_flights = future_flights, customer_email = customer_email)
		else:
			no_future_error = 'No future flight'
		return render_template('customer_home.html', no_future_error = no_future_error, customer_email = customer_email)
	else:
		return render_template('index.html')

#TODO: Customer searches for flights
#Author: Tianzuo Liu
#test: pass for round trip
'''
Search for future flights (one way or round trip) based on source city/airport name, 
destination city/airport name, dates (departure or return).
'''
# Input: departure airport, arrival airport, daparture date, arrival date
# Output: flight_number, departure_airport, departure date, arrival date, arrival airport
@app.route('/customer_search_flights', methods=['GET', 'POST'])
def customer_search_flights():
	cursor = conn.cursor()
	if request.method == 'POST':
		departure_airport = request.form['departure_airport']
		arrival_airport = request.form['arrival_airport']
		departure_date = request.form['departure_date']
		arrival_date = request.form['arrival_date']
		customer_email = session['customer_email']
		
		#executes query
		if (arrival_date != None):
			query = 'SELECT * From Flight WHERE departure_airport = %s and arrival_airport = %s and departure_date = %s and arrival_date = %s and departure_date >= CURDATE()'
			cursor.execute(query, (departure_airport, arrival_airport, departure_date, arrival_date))
		else:
			query = 'SELECT * From Flight WHERE departure_airport = %s and arrival_airport = %s and departure_date = %s and departure_date >= CURDATE()'
			cursor.execute(query, (departure_airport, arrival_airport, departure_date))
		#stores the results in a variable
		search_flights = cursor.fetchall()
		cursor.close()
		
		if(search_flights):
			return render_template('customer_home.html', search_flights = search_flights, customer_email = customer_email)
		else:
			no_search_error = 'Could not find the flight'
			return render_template('customer_home.html', no_search_error = no_search_error, customer_email = customer_email)
	else:
		return render_template('index.html')

#TODO: Customer purchases a ticket (from result of searching flight)
#Author: Tianzuo Liu
@app.route('/purchase_ticket', methods=['GET', 'POST'])
def purchase_ticket():
	cursor = conn.cursor()
	if request.method == 'POST':
		data = customer_search_flights()
		flight_number = request.form['flight_number']
		card_type = request.form['card_type']
		card_number = request.form['card_number']
		expiration_date = request.form['expiration_date']
		name_on_card = request.form['name_on_card']
		sold_price = request.form['sold_price']
		airline_name = request.form['airline_name']
		
		customer_email = session['customer_email']

		query = 'SELECT * FROM data WHERE flight_number = %s'
		cursor.execute(query, (flight_number))
	
		new_data = cursor.fetchone()
		ticket_ID = str(random.randint(0,9999999))

		if (new_data):
			insertion = 'INSERT INTO Ticket VALUES (%s, %s, %s, %s, %s, %s, %s, CURDATE(), CURDATE(), %s, %s, %s, %s)'
			cursor.execute(insertion, (ticket_ID, customer_email, sold_price, card_type, card_number, \
				name_on_card, expiration_date, new_data['departure_date'], new_data['departure_time'],flight_number, airline_name))
			conn.commit()

			purchase = 'INSERT INTO Purchase VALUES(%s, %s)'
			cursor.execute(purchase, (customer_email, ticket_ID))
			conn.commit()
			cursor.close()
			purchase_message = 'Successfully'
			return render_template('customer_home.html', purchase_message = purchase_message, customer_email = customer_email)
		else:
			no_purchase_error = 'something wrong. Please try again'
			return render_template('customer_home.html', no_purchase_error = no_purchase_error, customer_email = customer_email)
	else:
		return render_template('index.html')

#TODO: Customer cancels a trip
#Author: Tianzuo Liu
#test: pass for round trip
@app.route('/cancel_trip', methods=['GET', 'POST'])
def cancel_trip():
	cursor = conn.cursor()
	if request.method == 'POST':
		departure_airport = request.form['departure_airport']
		arrival_airport = request.form['arrival_airport']
		departure_date = request.form['departure_date']
		arrival_date = request.form['arrival_date']

		customer_email = session['customer_email']
		query = 'SELECT ticket_ID FROM Ticket NATURAL JOIN Flight WHERE customer_email = %s and departure_airport = %s and arrival_airport = %s and departure_date = %s and arrival_date = %s and departure_date >= CURDATE()'

		cursor.execute(query, (session['customer_email'], departure_airport, arrival_airport, departure_date, arrival_date))
		data = cursor.fetchone()

		if(data):
			query = 'DELETE FROM Purchase WHERE ticket_ID = %s'
			cursor.execute(query, (data['ticket_ID']))
			conn.commit()
			query = 'DELETE FROM Ticket WHERE ticket_ID = %s'
			cursor.execute(query, (data['ticket_ID']))
			conn.commit()
			cursor.close()
			cancel_message = 'Successfully deleted'
			return render_template("customer_home.html", cancel_message = cancel_message, customer_email = customer_email)
		else:
			no_cancel_error = 'Could not cancel the flight'
			return render_template('customer_home.html', no_cancel_error = no_cancel_error, customer_email = customer_email)
	else:
		return render_template('index.html')


#################################################################################################################

# TODO: Customer gives rating and comment
# Author: Yanglin Tao
'''
Customer will be able to rate and comment on their 
previous flights (for which he/she purchased tickets and already took that flight) for the airline they 
logged in.
'''
# input: flight_number, departure date, departure time, airline name
# output: none
# test: pass
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
				return render_template('customer_home.html', commentExistError = commentExistError, total_last_year = total_last_year, spending = spending)
			else:
				query = 'INSERT INTO Taken VALUES(%s, %s, %s, %s, %s, %s, %s)'
				cursor.execute(query, (customer_email, airline, rate, comm, flight_num, dept_date, dept_time))
				conn.commit()
				cursor.close()
				commentSucc = 'Thanks for your feedback!'
				return render_template('customer_home.html', commentSucc = commentSucc, total_last_year = total_last_year, spending = spending)
		else:
			noFlightError = 'There is no flight you are looking for. Please try again.'
			return render_template('customer_home.html', noFlightError = noFlightError, total_last_year = total_last_year, spending = spending)
	else: 
		return render_template('customer_home.html', customer_email = customer_email)

# TODO: Customer tracks spending
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
# test: pass
@app.route('/track_spending', methods=['GET', 'POST'])
def track_spending():
	cursor = conn.cursor();
	email = session['customer_email']
	total_last_year = spending_last_year()
	if request.method == 'POST':
		start = request.form['start_date']
		end = request.form['end_date']
		if start != None and end != None:
			query = 'SELECT %s AS start_date, %s AS end_date, SUM(sold_price) AS total FROM Ticket NATURAL JOIN Customer WHERE customer_email = %s AND purchase_date >= %s AND purchase_date <= %s'
			cursor.execute(query, (start, end, email, start, end))
			# stores purchase date, sold_price in a given date range
			data = cursor.fetchall()
		cursor.close()
		return render_template('customer_home.html', customer_email = email, spending = data, total_last_year = total_last_year)
	else:
		return render_template('customer_home.html', customer_email = email, total_last_year = total_last_year)

# TODO: Customer logout
# Author: Yanglin Tao
# test: pass
'''
Customer logs out of the system
'''
# input: none
# output: none
@app.route('/customer_logout')
def customer_logout():
	del session['customer_email']
	return render_template('customer_logout.html')

# TODO: Default show all airplanes
# Author: Yanglin Tao
# test: pass
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
		flights[i]['customer_email'] = customer_list

	cursor.close()
	return flights

# TODO: Staff home
# Author: Yanglin Tao
# test: pass
@app.route('/staff_home')
def staff_home():
	user_name = session['user_name']
	airplanes = default_show_all_airplanes()
	flights = default_view_30days()
	return render_template('staff_home.html', user_name = user_name, airplanes = airplanes, flights = flights)

# TODO: Staff views flights
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
		# find which airline it is 
		query = 'SELECT airline_name FROM Airline_staff WHERE user_name = %s'
		cursor.execute(query, (user_name))
		data = cursor.fetchone()
		airline = data['airline_name']
		# if there are inputs from user that specifies start_date, end_date, departure_airport, departure_city, 
		# arrival_airport, and arrival_city
		if start != None and end != None and dept_airport != None and arri_airport != None:
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
				flights[i]['customer_email'] = customer_list
		cursor.close()
		return render_template('staff_home.html', user_name = user_name, flights = flights, airplanes = airplanes)
	else:
		return render_template('staff_home.html', user_name = user_name, flights = flights, airplanes = airplanes)

# TODO: Staff creates new flights
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
# test: pass
@app.route('/add_flight', methods=['GET', 'POST'])
def create_flight():
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
				return render_template('staff_home.html', user_name = user_name, addFlightSucc = addFlightSucc, airplanes = airplanes, flights = flights)
			else:
				noPlaneError = 'This is a new airplane. Please add to the system first or try another.'
				return render_template('staff_home.html', user_name = user_name, noPlaneError = noPlaneError, airplanes = airplanes, flights = flights)
	else:
		return render_template('staff_home.html', user_name = user_name, airplanes = airplanes, flights = flights)

# TODO: Staff changes status of the flight
# Author: Yanglin Tao
'''
He or she changes a flight status (from on-time to delayed or vice versa) via 
forms.
'''
# input: flight_number, departure_date, departure_time, airline_name, status
# output: none
# test: pass
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

# TODO: Staff adds new airplane in the system
# Author: Yanglin Tao
# test: pass
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

#################################################################################################################

#TODO: Staff adds new airport in the system
#Author: Justin Li
@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
	cursor = conn.cursor()
	airport_name = request.form['airport_name']
	airport_city = request.form['airport_city']
	airport_cout = request.form['airport_country']
	airport_type = request.form['airport_type']
	query = 'INSERT INTO AIRPORT (airport_name, airport_city, airport_country, airport_type) VALUES (%s, %s, %s, %s)'
	cursor.execute(query, (airport_name, airport_city, airport_cout, airport_type))
	conn.commit()
	conn.close()
	return redirect(url_for('staff_home'))

#TODO: Staff views the rating and comments of the flight, along with the average rating
#Author: Justin Li
@app.route('/view_rating')
def view_rating():
    cursor = conn.cursor();
    customer_email = request.form['cus_email']
    airline_name = request.form['airline_name']
    airline_rating = request.form['air_rating']
    airline_comment = request.form['air_comment']
    query = 'SELECT cus_email, airline_name, air_rating, air_comment FROM Taken NATURAL JOIN Airline_Staff'
    cursor.execute(query)
    conn.commit
    #now, view the average
    query = 'SELECT AVG(air_rating) FROM Taken NATURAL JOIN Airline_staff'
    cursor.execute(query)
    conn.commit()
    cursor.close()
    return redirect(url_for('staff_home'))

#TODO: Staff views the most frequent customer
#Author: Justin Li
@app.route('/frequent_customer')
def frequent_customer():
    cursor = conn.cursor();
    customer_name = request.form['cus_name']
    customer_email = request.form['cus_email']
    ticket_ID = request.form['ticket_id']
    query = 'SELECT MAX(ticket_id) FROM Customer NATURAL JOIN Purchase where Customer.cus_email = Purchase.cus_email GROUP BY Customer.cus_email'
    cursor.execute(query)
    conn.commit
    cursor.close()
    return redirect(url_for('staff_home'))

#TODO: Staff views all flights of a customer
#Author: Justin Li
@app.route('/view_customer_flights')
def view_customer_flights():
    cursor = conn.cursor();
    customer_name = request.form['cus_name']
    customer_email = request.form['cus_email']
    ticket_ID = request.form['ticket_id']
    flight_number = request.form['flight_num']
    departure_date = request.form['depart_date']
    departure_time = request.form['depart_time']
    departure_airport = request.form['depart_airport']
    arrival_date = request.form['arri_date']
    arrival_time = request.form['arri_time']
    arrival_airport = request.form['arri_airport']
    query = 'SELECT flight_num, depart_airport, depart_date, depar_time, arri_airport, arri_date, arri_time FROM Customer NATURAL JOIN Purchase NATURAL JOIN Ticket NATURAL JOIN Flight WHERE Customer.cus_email = %s'
    cursor.execute(query)
    conn.commit
    cursor.close()
    return redirect(url_for('staff_home'))

#TODO: Staff views reports
#Author: Justin Li
@app.route('/view_reports')
def view_reports():
    cursor = conn.cursor();
    flight_number = request.form['flight_num']
    departure_date = request.form['depart_date']
    departure_time = request.form['depart_time']
    departure_airport = request.form['depart_airport']
    arrival_date = request.form['arri_date']
    arrival_time = request.form['arri_time']
    arrival_airport = request.form['arri_airport']
    flight_status = request.form['flight_status']
    airline_name = request.form['airline_name']
    user_name = request.form['user_name']
    query = 'SELECT flight_status FROM Flight NATURAL JOIN Airline_staff WHERE Flight.airline_name = Airline_staff.airline_name'
    cursor.execute(query)
    conn.commit
    cursor.close()
    return redirect(url_for('staff_home'))

#TODO: Staff views earned revenue
#Author: Justin Li
@app.route('/view_revenue')
def view_revenue():
    cursor = conn.cursor();
    flight_number = request.form['flight_num']
    departure_date = request.form['depart_date']
    departure_time = request.form['depart_time']
    departure_airport = request.form['depart_airport']
    arrival_date = request.form['arri_date']
    arrival_time = request.form['arri_time']
    arrival_airport = request.form['arri_airport']
    base_price = request.form['base_price']
    airline_name = request.form['airline_name']
    user_name = request.form['user_name']
    query = 'SELECT SUM(base_price) FROM Flight NATURAL JOIN Airline_staff WHERE Airline_staff.airline_name = Flight.airline_name'
    cursor.execute(query)
    conn.commit
    cursor.close()
    return redirect(url_for('staff_home'))

#TODO: Staff logout
#Author: Justin Li
@app.route('/staff_logout')
def staff_logout():
    session.pop('staff_email')
    return redirect('/')

app.secret_key = 'some key that you will never guess'

#Run the app on localhost port 5000
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)