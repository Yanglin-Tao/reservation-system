#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Author: Yanglin Tao
@app.route('/')
def hello():
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
	pass

#TODO: Authenticates customer register
#Author: Tianzuo Liu
@app.route('/customer_register_auth', methods=['GET', 'POST'])
def customer_register_auth():
	pass

#TODO: Authenticates staff register
#Author: Tianzuo Liu
@app.route('/staff_register_auth', methods=['GET', 'POST'])
def staff_register_auth():
	pass

#TODO: Customer home
#Author: Tianzuo Liu
@app.route('customer_home')
def customer_home():
	pass

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
	pass

#TODO: Customer purchases a ticket (from result of searching flight)
#Author: Tianzuo Liu
@app.route('customer_search_flights', methods=['GET', 'POST'])
def purchase_ticket():
	pass

#TODO: Customer cancels a trip
#Author: Tianzuo Liu
@app.route('cancel_trip', methods=['GET', 'POST'])
def cancel_trip():
	pass

#################################################################################################################

#TODO: Customer gives rating and comment
#Author: Yanglin Tao
'''
Customer will be able to rate and comment on their 
previous flights (for which he/she purchased tickets and already took that flight) for the airline they 
logged in.
'''
# input: flight_number, departure date, departure time, airline name
# output: none
@app.route('customer_rating', methods=['GET', 'POST'])
def customer_rating():
	cursor = conn.cursor();
	flight_num = request.form['flight_number']
	dept_date = request.form['departure_date']
	dept_time = request.form['departure_time']
	airline = request.form['airline_name']
	rate = request.form['rating']
	comm = request.form['comment']
	query = 'INSERT INTO Take (rating, comment) VALUES (%s, %s) WHERE flight_number = %s AND departure_date = %s AND \
		departure_time = %s AND airline_name = %s'
	cursor.execute(query, (rate, comm, flight_num, dept_date, dept_time, airline))
	conn.commit()
	cursor.close()
	return redirect(url_for('customer_home'))

#TODO: Customer tracks spending
#Author: Yanglin Tao
'''
Default view will be total amount of money spent in the past year and a bar
chart/table showing month wise money spent for last 6 months. He/she will also have option to specify 
a range of dates to view total amount of money spent within that range and a bar chart/table showing 
month wise money spent within that range
'''
# default output: total_last_year, monthly_spending_last_year
# input: start_date, end_date
# output: total_spending, monthly_spending
@app.route('track_spending', methods=['GET', 'POST'])
def track_spending():
	cursor = conn.cursor();
	email = session['customer_email']
	start = request.form['start_date']
	end = request.form['end_date']
	query1 = 'SELECT SUM(sold_price) FROM Ticket NATURAL JOIN Customer WHERE customer_email = %s AND \
		purchase_date >= NOW() - 1 YEAR AND purchase_date <= NOW()'
	cursor.execute(query1, (email))
	conn.commit()
	query2 = 'SELECT purchase_date, sold_price FROM Ticket NATURAL JOIN Customer WHERE customer_email = %s AND \
		purchase_date >= NOW() - 6 MONTH AND purchase_date <= NOW()'
	cursor.execute(query2, (email))
	conn.commit()
	if start != None and end != None:
		query2 = 'SELECT purchase_date, sold_price FROM Ticket NATURAL JOIN Customer WHERE customer_email = %s AND \
		purchase_date >= %s AND purchase_date <= %s'
		cursor.execute(query2, (email, start, end))
		conn.commit()
	cursor.close()
	return redirect(url_for('customer_home'))

#TODO: Customer logout
#Author: Yanglin Tao
'''
Customer logs out of the system
'''
# input: none
# output: none
@app.route('customer_logout')
def customer_logout():
	session.pop('customer_email')
	return redirect('/')

#TODO: Staff views flights
#Author: Yanglin Tao
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
@app.route('staff_view_flights', methods=['GET', 'POST'])
def staff_view_flights():
	cursor = conn.cursor();
	start = request.form['start_date']
	end = request.form['end_date']
	dept_airport = request.form['departure_airport']
	dept_city = request.form['departure_city']
	arri_airport = request.form['arrival_airport']
	arri_city = request.form['arrival_city']
	query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time,\
			 arrival_airport, customer_email FROM Ticket NATURAL JOIN Customer WHERE departure_date >= NOW() DAY AND \
				departure_date <= DATE(NOW()) + 30 DAY'
	cursor.execute(query)
	conn.commit()
	# if there are inputs from user that specifies astart_date, end_date, departure_airport, departure_city, 
	# arrival_airport, and arrival_city
	if start != None and end != None and dept_airport != None and dept_city != None and arri_airport != None and \
		arri_city != None:
		query = 'SELECT flight_number, departure_date, departure_time, departure_airport, arrival_date, arrival_time,\
			 arrival_airport, customer_email FROM Ticket NATURAL JOIN Customer WHERE departure_date > %s AND departure_date < %s \
				AND departure_airport = %s AND departure_city = %s AND arrival_airport = %s AND \
				arrival_city = %s'
		cursor.execute(query, (start, end, dept_airport, dept_city, arri_airport, arri_city))
		conn.commit()
	cursor.close()
	return redirect(url_for('staff_home'))

#TODO: Staff creates new flights
#Author: Yanglin Tao
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
@app.route('add_flight', methods=['GET', 'POST'])
def create_flight():
	cursor = conn.cursor();
	flight_num = request.form['flight_number']
	dept_airport = request.form['departure_airport']
	dept_date = request.form['departure_date']
	dept_time = request.form['departure_time']
	arri_airport = request.form['arrival_airport']
	arri_date = request.form['arrival_date']
	arri_time = request.form['arrival_time']
	airplane_identifi_num = request.form['airplane_identification_number']
	airline = request.form['airline_name']
	query = 'INSERT INTO Flight (flight_number, departure_airport, departure_date, departure_time, arrival_airport, arrival_date, arrival_time, airplane_identification_number, airline_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
	cursor.execute(query, (flight_num, dept_airport, dept_date, dept_time, arri_airport, arri_date, arri_time, airplane_identifi_num, airline))
	conn.commit()
	cursor.close()
	return redirect(url_for('staff_home'))

#TODO: Staff changes status of the flight
#Author: Yanglin Tao
'''
He or she changes a flight status (from on-time to delayed or vice versa) via 
forms.
'''
# input: flight_number, departure_date, departure_time, airline_name, status
# output: none
@app.route('change_status', methods=['GET', 'POST'])
def change_status():
	cursor = conn.cursor();
	flight_num = request.form['flight_number']
	dept_date = request.form['departure_date']
	dept_time = request.form['departure_time']
	airline = request.form['airline_name']
	new_status = request.form['flight_status']
	query = 'INSERT INTO Flight (flight_status) VALUES (%s) WHERE flight_number = %s AND departure_date = %s AND departure_time = %s AND airline_name = %s' 
	cursor.execute(query, (new_status, flight_num, dept_date, dept_time, airline))
	conn.commit()
	cursor.close()
	return redirect(url_for('staff_home'))

#TODO: Staff adds new airplane in the system
#Author: Yanglin Tao
'''
He or she adds a new airplane, providing all the needed data, via forms. 
The application should prevent unauthorized users from doing this action. In the confirmation page, 
she/he will be able to see all the airplanes owned by the airline he/she works for.
'''
# default output: all_airplanes(airplane_identification_number, number_of_seats, manufacture_company, age, airline_name)
# input: airplane_identification_number, number_of_seats, manufacture_company, age, airline_name
# output: none
@app.route('add_airplane', methods=['GET', 'POST'])
def add_airplane():
	cursor = conn.cursor();
	airplane_identifi_num = request.form['airplane_identification_number']
	num_of_seats = request.form['number_of_seats']
	manufact_comp = request.form['manufacture_company']
	airplane_age = request.form['age']
	airline = request.form['airline_name']
	query = 'INSERT INTO Airplane (airplane_identification_number, number_of_seats, manufacture_company, age, airline_name) VALUES (%s, %s, %s, %s, %s)'
	cursor.execute(query, (airplane_identifi_num, num_of_seats, manufact_comp, airplane_age, airline))
	conn.commit()
	cursor.close()
	return redirect(url_for('staff_home'))

#################################################################################################################

#TODO: Staff adds new airport in the system
#Author: Justin Li
@app.route('add_airport', methods=['GET', 'POST'])
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