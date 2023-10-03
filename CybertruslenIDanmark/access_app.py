# app.py
from flask import Flask, render_template, request
import base64

PIN = '2112'
PASSWORD = "pokemon"
app = Flask(__name__)

@app.route('/')
def numpad():
    return render_template('numpad.html')

@app.route('/process', methods=['POST'])
def process():
    pincode = request.form['pincode']
    # Do something with the user input, like printing it
    print("Pincode:", pincode)
    if pincode == PIN:
        result = "ACCESS"
    else:
        result = "DENIED"
    
    return render_template('numpad.html', access_result=result)  # Pass the result to the templat


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handle the POST request 
    if request.method == 'POST':
        password = request.form['password']
        if password == PASSWORD:
            result = "ACCESS"
        else: 
            result = "DENIED"
        print(result)
        return render_template('login.html', login_result=result)
    return render_template('login.html', login_result='')


@app.route('/unilogin', methods=['GET', 'POST'])
def unilogin():
    # Handle the POST request
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
    return render_template('unilogin.html', login_result='')

if __name__ == '__main__':
    app.run(debug=True)

