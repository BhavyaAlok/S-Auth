from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors, generate_qr
import re
  
app = Flask(__name__)
  
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'
  
mysql = MySQL(app)
  
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            session['secret_key'] = user['secret_key']
            mesage = 'Logged in successfully !'
            render_template('login.html', mesage = mesage)
            mesage = 'Please Enter Authentication Code'
            return render_template('authentication.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        secret_key = generate_qr.generate_key()
        img = generate_qr.generate_QRCode(secret_key)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s, % s)', (userName, email, password, secret_key, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
            render_template('register.html', mesage = mesage)
            return render_template('qrcode_display.html', user_image = img)
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)

@app.route('/authenticate', methods =['GET', 'POST'])
def authenticate():
    mesage = ''
    if request.method == 'POST' and 'code' in request.form:
        code = request.form['code']
        #print("Code : ", code)
        secret_key = session['secret_key']
        auth_code = generate_qr.get_otp(secret_key)
        #print("Auth Code : ", auth_code)
        if int(code) == int(auth_code):
            mesage = 'Authentication Successful'
            return render_template('user.html', mesage = mesage)
        else:
            mesage = 'Authentication Failed'
            return render_template('authentication.html', mesage = mesage)
    elif request.method == 'POST':
        mesage = 'Please enter the authentication code!'
    return render_template('authentication.html', mesage = mesage)

if __name__ == "__main__":
    app.run()