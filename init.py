#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursor

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
@app.route('customer_search_flights')
def customer_search_flights():
	pass

#TODO: Customer purchases a ticket (from result of searching flight)
#Author: Tianzuo Liu
@app.route('customer_search_flights')
def purchase_ticket():
	pass

#TODO: Customer cancels a trip
#Author: Tianzuo Liu
@app.route('cancel_trip')
def cancel_trip():
	pass

#TODO: Customer gives rating and comment
#Author: Yanglin Tao
'''
Customer will be able to rate and comment on their 
previous flights (for which he/she purchased tickets and already took that flight) for the airline they 
logged in.
'''
# input: flight_number, departure date, departure time, airline name
# output: none
@app.route('customer_rating')
def customer_rating():
	pass

#TODO: Customer tracks spending
#Author: Yanglin Tao
'''
Default view will be total amount of money spent in the past year and a bar
chart/table showing month wise money spent for last 6 months. He/she will also have option to specify 
a range of dates to view total amount of money spent within that range and a bar chart/table showing 
month wise money spent within that range
'''
# input: start_date, end_date
# output: total_spending, monthly_spending
@app.route('track_spending')
def track_spending():
	pass

#TODO: Customer logout
#Author: Yanglin Tao
'''
Customer logs out of the system
'''
# input: none
# output: none
@app.route('customer_logout')
def customer_logout():
	pass

#TODO: Staff views flights
#Author: Yanglin Tao
'''
Defaults will be showing all the future flights operated by the airline he/she works for 
the next 30 days. He/she will be able to see all the current/future/past flights operated by the airline 
he/she works for based range of dates, source/destination airports/city etc. He/she will be able to see 
all the customers of a particular flight.
'''
# input: 
# output:
@app.route('staff_view_flights')
def staff_view_flights():
	pass

#TODO: Staff creates new flights
#Author: Yanglin Tao
'''

'''
# input: 
# output:
@app.route('staff_create_flight')
def create_flight():
	pass

#TODO: Staff changes status of the flight
#Author: Yanglin Tao
'''

'''
# input: 
# output:
@app.route('change_status')
def change_status():
	pass

#TODO: Staff adds new airplane in the system
#Author: Yanglin Tao
'''

'''
# input: 
# output:
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