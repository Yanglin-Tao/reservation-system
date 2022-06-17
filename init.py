#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymsql.cursor

app = Flask(__name__)

#configure SQL
conn = pymsql.connect(host = 'localhost', user = 'root', password = 'root',
                      db = 'meetup', charset = 'utf8mb4',
                      cursorclass = pymsql.cursor.Dictursor)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('customer_login.html')

@app.route('/register')
def register():
    return render_template('customer_register.html')

@app.route('/loginAuth', methods = ['GET', 'POST'])
def loginAuth():
    username = request.form['username']
    password = request.form['password']
    cursor = conn.corsor()
    query = 'SELECT * FROM Customer WHERE customer_email = %s and customer_password = %s'
    cursor.excute(query, (username, password))

    data = cursor.fetchone()
    cursor.close()
    if(data):
        session['username'] = username
        return redirect(url_for('customer_home'))
    else:
        error = 'Invalid username or password. Please try again'
        return render_template('customer_login.html', error = error)

@app.route('/registerAuth', methods = ['GET', 'POST'])
def registerAuth():
    username = request.form['username']
    password = request.form['password']
    cursor = conn.corsor()
    query = 'SELECT * FROM Customer WHERE customer_email = %s and customer_password = %s'
    cursor.excute(query, (username, password))

    data = cursor.fetchone()
    
    if(data):
        error = 'The account has already exists'
        cursor.close()
        return render_template('customer_register.html', error = error)
    else:
        ins = 'INSERT INTO Customer VALUES(%s, %s)'
        cursor.excute(ins, (username, password))
        conn.commit()
        cursor.close()
        return render_template('index.html')

#not done now
@app.route('/home')
def home():
    username = session['username']
    cursor = conn.cursor()

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')


if(__name__) == "__main__":
    app.run("127.0.0.1", 5000, debug = True)


