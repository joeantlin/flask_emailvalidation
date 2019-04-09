from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL      # import the function that will return an instance of a connection
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe' 
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods = ["POST"])
def submit():
    mysql = connectToMySQL('email_data')
    query = "INSERT INTO emails (email, created_at, updated_at) VALUES(%(email)s, NOW(), NOW());"
    data = {
        "email": request.form["user_email"]
    }
    if not EMAIL_REGEX.match(request.form['user_email']):
        flash("Email is not Valid")
        return redirect('/')
    else:
        flash(f"The email adress you entered {data['email']}, is a VALID email adress! Thank you!")
        new_emails = mysql.query_db(query, data)
        return redirect('/success')

@app.route('/success')
def success():
    mysql = connectToMySQL('email_data')
    the_emails = mysql.query_db('SELECT * FROM emails;')
    return render_template('success.html', emaildata = the_emails)



if __name__ =='__main__':
    app.run(debug=True)