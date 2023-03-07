import mysql.connector
import dbfunc
from flask import Flask, render_template, request, session, redirect, url_for
from passlib.hash import sha256_crypt
import hashlib
import gc
from functools import wraps
app = Flask(__name__)
app.secret_key = 'suchSecret'     #secret key for sessions

#establishing a database connectoion.
dbfunc.getConnection()

@app.route('/home')
@app.route('/index')
@app.route('/')
def index():
   return render_template('indexJinja.html')


@app.route('/about')
def about_route():
   return render_template('aboutJinja.html')

@app.route('/book')
def book_route():
   return render_template('bookJinja.html')


@app.route('/login')
def login_route():
   return render_template('loginJinja.html')


@app.route('/register', methods=['POST', 'GET'])
def register_route():
    error = ''
    print('Register start')
    try:
        if request.method == "POST":         
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            password = request.form['password']
            email = request.form['email']                      
            if firstName != None and lastName != None and password != None and email != None:           
                conn = dbfunc.getConnection()
                if conn != None:    #Checking if connection is None           
                    if conn.is_connected(): #Checking if connection is established
                        print('MySQL Connection is established')                          
                        dbcursor = conn.cursor()    #Creating cursor object 
                        #here we should check if email / email already exists   
                        #hashing password                                                     
                        password = sha256_crypt.hash((str(password)))    
                               
                        Verify_Query = "SELECT * FROM users WHERE email = %s;"
                        dbcursor.execute(Verify_Query,(email,))
                        rows = dbcursor.fetchall()           
                        if dbcursor.rowcount > 0:   #this means there is a user with same email
                            print('email already taken, please choose another')
                            error = "Email already taken, please choose another"
                            return render_template("registerJinja.html", error=error)    
                        else:   #this means we can add new user             
                            dbcursor.execute("INSERT INTO users (first_name, last_name, email, password_hash) VALUES (%s, %s, %s, %s)", (firstName, lastName, email, password))                
                            conn.commit()  #saves data in database              
                            print("Thanks for registering!")
                            dbcursor.close()
                            conn.close()
                            gc.collect()                        
                            session['logged_in'] = True     #session variables
                            session['email'] = email
                            session['usertype'] = 'standard'   #default all users are standard
                            return render_template("success.html",\
                             message='User registered successfully and logged in..')
                    else:                        
                        print('Connection error')
                        return 'DB Connection Error'
                else:                    
                    print('Connection error')
                    return 'DB Connection Error'
            else:                
                print('empty parameters')
                return render_template("registerJinja.html", error=error)
        else:            
            return render_template("registerJinja.html", error=error)        
    except Exception as e:                
        return render_template("registerJinja.html", error=e)    
    return render_template("registerJinja.html", error=error)











@app.route('/base')
def base_route():
   return render_template('baseHTML.html')

   

if __name__ == '__main__':
    app.run(debug = True)

#Process:
#1. Put html files under templates folder             DONE
#2. Put static files (i.e. css and images and js files) under static folder      DONE
   #2a. you may create sub-folders i.e. css for CSS files, img for Images
#3. Make app i.e. .py file and create decorates/endpoints for each webpage so that you can link them using url_for()          DONE
   #3a. use render_template() to return the html page
#4. Update <link> tag in html files to refer to css by using url_for()
#5. Update <a> tag href attribute to call end point for each page by using url_for()
#6. Update <img> tag src attribute to link to images e.g., 'static/image.jpeg'
#7. Update css file if you're using background images e.g., 'static/image.jpeg'
