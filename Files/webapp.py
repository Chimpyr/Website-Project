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


#/login/ route receives email and password and checks against db user/pw
@app.route('/login', methods=["GET","POST"])
def login_route():
    form={}
    error = ''
    try:	
        if request.method == "POST":            
            email = request.form['email']
            password = request.form['password']            
            form = request.form
            print('login start 1.1')

            if email != None and password != None:  #check if un or pw is none          
                conn = dbfunc.getConnection()
                if conn != None:    #Checking if connection is None                    
                    if conn.is_connected(): #Checking if connection is established                        
                        print('MySQL Connection is established')                          
                        dbcursor = conn.cursor()    #Creating cursor object                                                 
                        dbcursor.execute("SELECT password_hash, usertype \
                            FROM users WHERE email = %s;", (email,))                                                
                        data = dbcursor.fetchone()
                        #print(data[0])
                        if dbcursor.rowcount < 1: #this mean no user exists                         
                            error = "User / password does not exist, login again"
                            return render_template("loginJinja", error=error)
                        else:                            
                            #data = dbcursor.fetchone()[0] #extracting password   
                            # verify passowrd hash and password received from user                                                             
                            if sha256_crypt.verify(request.form['password'], str(data[0])):                                
                                session['logged_in'] = True     #set session variables
                                session['email'] = request.form['email']
                                session['usertype'] = str(data[1])                          
                                print("You are now logged in")                                
                                return render_template('userresources.html', \
                                    email=email, data='this is user specific data',\
                                         usertype=session['usertype'])
                            else:
                                error = "Invalid credentials email/password, try again."                               
                    gc.collect()
                    print('login start 1.10')
                    return render_template("loginJinja.html", form=form, error=error)
    except Exception as e:                
        error = str(e) + " <br/> Invalid credentials, try again."
        return render_template("loginJinja.html", form=form, error = error)   
    
    return render_template("loginJinja.html", form=form, error = error)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:            
            print("You need to login first")
            #return redirect(url_for('login', error='You need to login first'))
            return render_template('loginJinja.html', error='You need to login first')    
    return wrap

@app.route("/logout")
@login_required
def logout():    
    session.clear()    #clears session variables
    print("You have been logged out!")
    gc.collect()
    return render_template('indexJinja.html', optionalmessage='You have been logged out')


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



#We also write a wrapper for admin user(s). It will check with the user is 
# logged in and the usertype is admin and only then it will allow user to
# perform admin functions
def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if ('logged_in' in session) and (session['usertype'] == 'admin'):
            return f(*args, **kwargs)
        else:            
            print("You need to login first as admin user")
            #return redirect(url_for('login', error='You need to login first as admin user'))
            return render_template('loginJinja.html', error='You need to login first as admin user')    
    return wrap



#We also write a wrapper for standard user(s). It will check with the usertype is 
#standard and user is logged in, only then it will allow user to perform standard user functions
def standard_user_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if ('logged_in' in session) and (session['usertype'] == 'standard'):
            return f(*args, **kwargs)
        else:            
            print("You need to login first as standard user")
            #return redirect(url_for('login', error='You need to login first as standard user'))
            return render_template('loginJinja.html', error='You need to login first as standard user')    
    return wrap

#/userfeatures is loaded for standard users
# Here we us @standard_user_login_required wrapper ... 
# this means that only users with user type standard can access this function
# the function implements features related to standard users
@app.route('/userfeatures')
@login_required
@standard_user_required
def user_features():
        print('fetchrecords')
        #records from database can be derived
        #user login can be checked..
        print ('Welcome ', session['email'])
        return render_template('standarduser.html', \
            user=session['email'], message='User data from app and standard \
                user features can go here....')

#/adminfeatures is loaded for admin users
# Here we us @admin_required wrapper ... 
# this means that only users with user type admin can access this function
# the function implements features related to admin users
@app.route('/adminfeatures')
@login_required
@admin_required
def admin_features():
        print('create / amend records / delete records / generate reports')
        #records from database can be derived, updated, added, deleted
        #user login can be checked..
        print ('Welcome ', session['email'], ' as ', session['usertype'])
        return render_template('adminuser.html', user=session['email'],\
             message='Admin data from app and admin features can go here ...')




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
