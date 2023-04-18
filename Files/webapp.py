import mysql.connector
import dbfunc
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
from datetime import datetime
from passlib.hash import sha256_crypt
import hashlib
import gc
import requests
import json
from functools import wraps
app = Flask(__name__)
app.secret_key = 'suchSecret'  # secret key for sessions

# establishing a database connectoion.
dbfunc.getConnection()


@app.route('/home')
@app.route('/index')
@app.route('/')
def index():
    # check if the user is logged in as admin
        # then load the render template
    # else if the user is logged in as standard user

    return render_template('indexJinja.html')


@app.route('/about')
def about_route():
    return render_template('aboutJinja.html')


@app.route('/book')
def book_route():
    #This sorts out the inputs from the form and passes them to the book function to be used in the query later
    conn = dbfunc.getConnection()
    if conn != None:  # Checking if connection is None
        print('MySQL Connection is established')
        dbcursor = conn.cursor()  # Creating cursor object
        dbcursor.execute('SELECT DISTINCT department_location FROM journey;')
        # print('SELECT statement executed successfully.')
        rows = dbcursor.fetchall()
        dbcursor.close()
        conn.close()  # Connection must be closed
        cities = []
        for city in rows:
            city = str(city).strip("(")
            city = str(city).strip(")")
            city = str(city).strip(",")
            city = str(city).strip("'")
            cities.append(city)
        return render_template('bookJinja.html', departurelist=cities)
    else:
        print('DB connection Error')
        return 'DB Connection Error'


@app.route('/bookingview')
def bookingView():
    #This lets the user view their bookings

    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
    else:
        user_id = getUserID()

    conn = dbfunc.getConnection()
    if conn != None:  # Checking if connection is None
        dbcursor = conn.cursor()  # Creating cursor object
        #check if user id admin
        #if admin then show all bookings
        #else show only the users bookings
        if session['usertype'] == 'admin':
            query = "SELECT * FROM booking"
            dbcursor.execute(query)
        else:
            query = "SELECT * FROM booking WHERE user_id = %s"
            dbcursor.execute(query, (user_id,))
        
        bookings = dbcursor.fetchall()
        dbcursor.close()
        conn.close()  # Connection must be closed
        return render_template('bookingView.html', bookings=bookings, user_id=user_id)
    else:
            print('DB connection Error')
            return 'DB Connection Error'
    

    
@app.route('/delete-booking', methods=['POST'])
def delete_booking():
    #This one is self explanatory, it deletes the booking from the database

    # Delete the selected booking from the database
    conn = dbfunc.getConnection()
    if conn != None:
        try:
            # Retrieve the user ID and booking details from the form data
            user_id = int(request.form['user_id'])
            booking_id = int(request.form['booking_id'])
            date = request.form['date']
            print(date)
            fare = request.form['fare']
            print(fare)

            # Calculate the cancellation period
            days_before_booking = (datetime.strptime(date, '%Y-%m-%d') - datetime.now()).days
            if days_before_booking >= 60:
                cancellation_charge = 0
            elif days_before_booking >= 30:
                cancellation_charge = 0.5 * float(fare)
            else:
                cancellation_charge = float(fare)

            # Delete the booking from the database
            cursor = conn.cursor()
            query = "DELETE FROM booking WHERE user_id = %s AND booking_id = %s"
            #cursor.execute(query, (user_id, booking_id))
            conn.commit()
            cursor.close()
            conn.close()
            message = f"Booking Cancelled successfully. Cancellation charge: {cancellation_charge:.2f}."
            alert_type = "success"
        except Exception as e:
            print('DB error:', e)
            message = "Error deleting booking: {}".format(str(e))
            if (format(str(e)) == "400 Bad Request: The browser (or proxy) sent a request that this server could not understand."):
                message = "There was an Error Cancelling Booking because the Booking ID was not found or selected."
            alert_type = "danger"
    else:
        message = 'DB connection Error'
        alert_type = "danger"
    
    return render_template('bookingView.html', user_id=user_id, message=message, alert_type=alert_type)
    # return redirect(url_for('bookingView', user_id=user_id, message=message, alert_type=alert_type))


@app.route('/edit_booking/<string:id>/', methods=['GET', 'POST'])
def edit_booking(id):
    conn = dbfunc.getConnection()
    if conn != None:
        try:
           pass
        except Exception as e:
            print('DB error:', e)
            message = "Error deleting booking: {}".format(str(e))
    else:
        message = 'DB connection Error'
    
    return render_template()




@app.route('/returncity/', methods=['POST', 'GET'])
def ajax_returncity():
    print('/returncity')
    #This uses the database to retrieve all available return cities based on the departure city

    if request.method == 'GET':
        deptcity = request.args.get('q')
        conn = dbfunc.getConnection()
        if conn != None:  # Checking if connection is None
            print('MySQL Connection is established')
            dbcursor = conn.cursor()  # Creating cursor object
            dbcursor.execute(
                'SELECT DISTINCT arrival_location FROM journey WHERE department_location = %s;', (deptcity,))
            # print('SELECT statement executed successfully.')
            rows = dbcursor.fetchall()
            total = dbcursor.rowcount
            dbcursor.close()
            conn.close()  # Connection must be closed
            return jsonify(returncities=rows, size=total)
        else:
            print('DB connection Error')
            return jsonify(returncities='DB Connection Error')




# /login/ route receives email and password and checks against db user/pw
@app.route('/login', methods=["GET", "POST"])
def login_route():
    form = {}
    error = ''
    try:
        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']
            form = request.form
            print('login start 1.1')

            if email != None and password != None:  # check if un or pw is none
                conn = dbfunc.getConnection()
                if conn != None:  # Checking if connection is None
                    if conn.is_connected():  # Checking if connection is established
                        print('MySQL Connection is established')
                        dbcursor = conn.cursor()  # Creating cursor object
                        dbcursor.execute("SELECT password_hash, usertype \
                            FROM users WHERE email = %s;", (email,))
                        data = dbcursor.fetchone()
                        # print(data[0])
                        if dbcursor.rowcount < 1:  # this mean no user exists
                            error = "User / password does not exist, login again"
                            return render_template("loginJinja", error=error)
                        else:
                            # data = dbcursor.fetchone()[0] #extracting password
                            # verify passowrd hash and password received from user
                            if sha256_crypt.verify(request.form['password'], str(data[0])):
                                # set session variables
                                session['logged_in'] = True
                                session['email'] = request.form['email']
                                # fake user name to be used in the welcome messages
                                session['username'] = email.split('@')[0]
                                session['usertype'] = str(data[1])
                                if (session['usertype'] == 'admin'):
                                    return render_template('adminuser.html',
                                                       user=session['email'],
                                                       usertype=session['usertype'])
                                elif (session['usertype'] == 'standard'):
                                    return render_template('standarduser.html',
                                                       user=session['email'],
                                                       usertype=session['usertype'])
                                print("You are now logged in")
                                
                            else:
                                error = "Invalid credentials email/password, try again."
                    gc.collect()
                    print('login start 1.10')
                    return render_template("loginJinja.html", form=form, error=error)
    except Exception as e:
        error = str(e) + " <br/> Invalid credentials, try again."
        return render_template("loginJinja.html", form=form, error=error)

    return render_template("loginJinja.html", form=form, error=error)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            print("You need to login first")
            # return redirect(url_for('login', error='You need to login first'))
            return render_template('loginJinja.html', error='You need to login first')
    return wrap


@app.route("/logout")
@login_required
def logout():
    message = request.args.get("message")
    session.clear()  # clears session variables
    print("You have been logged out!")
    gc.collect()

    print(message)
    if message == "PU":
        optional_message = 'Password Updated'
    else:
        optional_message = 'You have been logged out'
    # optional_message = message or "You have been logged out!"
    return render_template("indexJinja.html", optionalmessage=optional_message)
    # return render_template('indexJinja.html', optionalmessage='You have been logged out')
    




@app.route('/selectBooking/', methods=['POST', 'GET'])
@login_required
def selectBooking():
    # This uses the form data to create the booking
    if request.method == 'POST':
        # print('Select booking initiated')
        departLocation = request.form['departureslist']
        arrivalLocation = request.form['arrivalslist']
        departDate = request.form['departDate']
        adultseats = request.form['adultseats']
        childseats = request.form['childseats']
        travelClass = request.form['travelClass']
        travelType = request.form['travelType']

        passenger_count = int(adultseats) + int(childseats)
        print('passenger count: ' + str(passenger_count))

        try:
            returnDate = request.form['returnDate']
        except:
            returnDate = None

        # used in HTML jinja
        lookupdata = [departLocation, arrivalLocation, departDate,
                      returnDate, adultseats, childseats, travelClass]

        isOneWay = False
        if(travelType == "one-way"):
            isOneWay = True

        conn = dbfunc.getConnection()

        if conn is not None:
            dbcursor = conn.cursor()

        #by default, and one way
        dbcursor.execute('SELECT * FROM journey WHERE department_location = %s AND arrival_location = %s;',
                                 (departLocation, arrivalLocation))
        OWrows = dbcursor.fetchall()
        journey_id = OWrows[0][0] #get the journey ID

        # THIS IS BROKEN - WHEN LDN TO MAN it breaks?
        # if it is a return trip, get the return trip data, this includes flights going back
        if not isOneWay:
            #flipped to do the opposite direction
            print
            dbcursor.execute('SELECT * FROM journey WHERE department_location = %s AND arrival_location = %s;',
                                 (arrivalLocation, departLocation))
            RTrows = dbcursor.fetchall()
            print("RTrows")
            print(RTrows)
            if RTrows == []:
                print("RT rows empty")
                flash('Sorry, currently there are currently no return flights from ' + arrivalLocation + ' to ' + departLocation + '. Please try again.')
                return redirect('/book')
            return_journey_id = RTrows[0][0] #get the return journey ID


        # check that flight is full
        # if flight is full give an error message
        capacity = 120 # this is the capacity of the plane

        # query to get the number of existing bookings on the flight for that date and specific journey
        # checks the first flight (one way, departure flight)
        dbcursor.execute("SELECT SUM(passenger_no) FROM booking WHERE journey_id = %s AND start_date = %s", (journey_id, departDate,))
        existing_bookings = dbcursor.fetchone()[0]
        if not isOneWay:
            # checks the second flight (return flight)
            dbcursor.execute("SELECT SUM(passenger_no) FROM booking WHERE journey_id = %s AND start_date = %s", (return_journey_id, returnDate,))
            existing_return_bookings = dbcursor.fetchone()[0]
            if existing_return_bookings is None:
                existing_return_bookings = 0
            print("return existing_bookings")
            print(existing_return_bookings)
            return_available_seats = capacity - existing_return_bookings - passenger_count
            print("return_available_seats")
            print(return_available_seats)

            



        if existing_bookings is None:
            existing_bookings = 0
        print("existing_bookings")
        print(existing_bookings)
        
        
        # Calculate the number of available seats on the flight
        available_seats = capacity - existing_bookings - passenger_count
        print("available_seats")
        print(available_seats)
        
        # Check if there are enough available seats for the booking
        if available_seats >= 0:
            print("flight where depart available_seats >= 0")
            if not isOneWay:
                print("return flight where depart available_seats >= 0")
                if return_available_seats < 0: #if there are NOT enough seats on the return flight the num is < 0
                    print("return flight where depart available_seats >= 0 AND return_available_seats < 0")
                    flash('Sorry, there are not enough available seats for your return booking. Please try again with a lower number of passengers.')
                    return redirect('/book')


            datarows = []
            RTdatarows = []

            for row in OWrows:
                data = list(row)
                fare = (float(row[5]) * float(adultseats)) + \
                    (float(row[5]) * 0.5 * float(childseats))

                if travelClass == 'Business class':
                    fare = fare * 2

                    
                
                # #going to only base it off the depart date in all cases for now
                # advance_time = (depart_date - today).days

                departDate = request.form['departDate']
                # Convert departDate string to date object
                depart_date = datetime.strptime(
                    departDate, '%Y-%m-%d').date()

                today = datetime.now().date()
                # Calculate the number of days between today and the departure date
                advance_time = (depart_date - today).days

                if advance_time >= 80:
                    fare = fare * 0.8
                elif advance_time >= 60:
                    fare = fare * 0.9
                elif advance_time >= 45:
                    fare = fare * 0.95

                data.append(fare)
                datarows.append(data)


            if not isOneWay:

                RTdata = [] # initialize RTdata with an empty list
                for row in RTrows:
                    RTdata = list(row)
                    fare = (float(row[5]) * float(adultseats)) + \
                        (float(row[5]) * 0.5 * float(childseats))

                if travelClass == 'Business class':
                    fare = fare * 2

                today = datetime.now().date()
                # Calculate the number of days between today and the departure date
                return_date = datetime.strptime(
                    returnDate, '%Y-%m-%d').date()


                advance_time = (return_date - today).days

                if advance_time >= 80:
                    fare = fare * 0.8
                elif advance_time >= 60:
                    fare = fare * 0.9
                elif advance_time >= 45:
                    fare = fare * 0.95
                    
                RTdata.append(fare)

                RTdatarows.append(RTdata)
                print('rt data rows vvv')
                print(RTdatarows)
            else:
                RTdatarows = None
                print('else(oneWay) rt data rows vvv')
                print(RTdatarows)

            dbcursor.close()
            conn.close()

            return render_template('booking_start.html', resultset=datarows, resultsetRT=RTdatarows, lookupdata=lookupdata, isOneWay=isOneWay)    
        else:
            print("return flight where depart available_seats is < 0 (not enough seats)")
            flash('Sorry, there are not enough available seats for your departure booking. Please try again with a lower number of passengers.')
            return redirect('/book')
    else:
        print('DB connection Error')
        return redirect(url_for('index'))



def getUserID():
    conn = dbfunc.getConnection()
    if conn != None:
            print('MySQL Connection is established')
            dbcursor = conn.cursor()  # Creating cursor object

        #getting the user_id to store booking with user's id
            userEmail = user=session['email']
            print("email is : " + userEmail)
            dbcursor.execute("SELECT user_id FROM users WHERE email = %s;", (userEmail,))
            userID = dbcursor.fetchone()[0] # gets the straight int value instead of tuple
            print("user id = " + str(userID))
            return userID
    else:
        print('DB connection Error')
        return redirect(url_for('index'))
            



@app.route('/booking_confirm/', methods=['POST', 'GET'])
def booking_confirm():
    if request.method == 'POST':
        isOneWay = True
        print('booking confirm initiated')
        outbound_journeyid = request.form['outbound_bookingchoice']
        departcity = request.form['deptcity']
        arrivalcity = request.form['arrivcity']
        outdate = request.form['outdate']
        
        adultseats = request.form['adultseats']
        childseats = request.form['childseats']
        outbound_totalfare = request.form['outbound_totalfare']
        cardnumber = request.form['cardnumber']

        if 'returnDate' in request.form:
            returndate = request.form['returnDate']
            return_journeyid = request.form['return_bookingchoice']
            return_totalfare = request.form['return_totalfare']
            return_bookingdata = [return_journeyid, departcity, arrivalcity, outdate, adultseats, childseats, return_totalfare]
            isOneWay = False
        else:
            return_journeyid = None
            return_departcity = None
            return_arrivalcity = None
            return_outdate = None
            return_adultseats = None
            return_childseats = None
            return_totalfare = None
            return_cardnumber = None
            return_bookingdata = None

        totalseats = int(adultseats) + int(childseats)
        outbound_bookingdata = [outbound_journeyid, departcity, arrivalcity, outdate, adultseats, childseats, outbound_totalfare]

        

        conn = dbfunc.getConnection()
        if conn != None:  # Checking if connection is None
            print('MySQL Connection is established')
            dbcursor = conn.cursor()  # Creating cursor object

            #get user id
            userID = getUserID()

            dbcursor.execute('SELECT LAST_INSERT_ID();')
            rows = dbcursor.fetchone()
            outbound_bookingid = rows[0]
            outbound_bookingdata.append(outbound_bookingid)

            if return_journeyid:
                dbcursor.execute('SELECT LAST_INSERT_ID();')
                rows = dbcursor.fetchone()
                return_bookingid = rows[0]
                return_bookingdata.append(return_bookingid)

            dbcursor.execute('SELECT * FROM journey WHERE journey_id = %s;', (outbound_journeyid,))
            rows = dbcursor.fetchall()
            outbound_deptTime = rows[0][2] # corresponding column depTime
            outbound_arrivTime = rows[0][4] # corresponding column arrivTime
            outbound_bookingdata.append(outbound_deptTime)
            outbound_bookingdata.append(outbound_arrivTime)

            if return_journeyid:
                dbcursor.execute('SELECT * FROM journey WHERE journey_id = %s;', (return_journeyid,))
                rows = dbcursor.fetchall()
                return_deptTime = rows[0][2] # corresponding column depTime
                return_arrivTime = rows[0][4] # corresponding column arrivTime
                return_bookingdata.append(return_deptTime)
                return_bookingdata.append(return_arrivTime)


            #get book date
            today = datetime.now().date()


            # Insert outbound booking data into database
            dbcursor.execute('INSERT INTO booking(user_id, journey_id, start_date, start_location, end_location, start_time, end_time, book_date, passenger_no, booking_cost) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);', (userID, outbound_journeyid, outdate, departcity, arrivalcity, outbound_deptTime, outbound_arrivTime, today, totalseats, outbound_totalfare))
            conn.commit()

            payload = request.form.to_dict()
            print(payload)
            

            if return_journeyid:
                dbcursor.execute('INSERT INTO booking(user_id, journey_id, start_date, start_location, end_location, start_time, end_time, book_date, passenger_no, booking_cost) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);', (userID, return_journeyid, returndate, arrivalcity, departcity, return_deptTime, return_arrivTime, today, totalseats, return_totalfare))
                conn.commit()
                returnDate = payload['returnDate']
            else:
                returnDate = None
            


            print('Booking Confirmed')

            cardnumber = cardnumber[-4:-1]
            print(cardnumber)

            dbcursor.close()
            conn.close()

            your_route_handler()


           

            return render_template('booking_confirm.html', outbound_bookingdata=outbound_bookingdata, return_bookingdata=return_bookingdata, cardnumber=cardnumber, isOneWay=isOneWay, returnDate=returnDate)
        else:
            print('DB connection Error')
            return redirect(url_for('index'))

def your_route_handler():
    if request.method == 'POST':
            try:
                payload = request.json
                print('Payload:', payload)
                return 'Success'
            except:
                return 'Error'
    else:
            return 'Invalid request method'


@app.route('/changePassword', methods=['POST', 'GET'])
@login_required
def changePassword():
    error = ''
    print('Pass change start')
    try:
        if request.method == "POST":
            email = request.form['email']
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            confirm_new_password = request.form['confirm_new_password']
            if email != None and old_password != None and new_password != None and confirm_new_password != None:
                conn = dbfunc.getConnection()
                if conn != None:  # Checking if connection is None
                    if conn.is_connected():  # Checking if connection is established
                        print('MySQL Connection is established')
                        dbcursor = conn.cursor()  # Creating cursor object
                        # hashing password
                        newPasswordHashed = sha256_crypt.hash((str(new_password)))
                        #selects password from email
                        dbcursor.execute("SELECT password_hash, usertype \
                            FROM users WHERE email = %s;", (email,))
                        data = dbcursor.fetchone()
                        if dbcursor.rowcount < 1:  # this mean no user exists
                            error = "User / password does not exist, login again"
                            return render_template("changePassword.html", error=error)
                        else:
                            # verify password hash and password received from user
                            if sha256_crypt.verify(request.form['old_password'], str(data[0])): #
                                query = "UPDATE users SET password_hash=%s WHERE email=%s;"
                                dbcursor.execute(query, (newPasswordHashed, email))
                                conn.commit()
                                #change password to newPassword hash where email is...
                                dbcursor.close()
                                conn.close()
                                gc.collect()
                                #loggs user out - makes them have to re log in with new password
                                flash("Your password has been changed successfully!")
                                return redirect(url_for("logout", message="PU"))
                                # return redirect(url_for("logout", message='PU', next=url_for("index")))
                                # return redirect(url_for("logout", next=url_for("index", optionalmessage='ddd')))
                            else:
                                error = "Invalid credentials email/password, try again."
                    else:
                        print('Connection error')
                        return 'DB Connection Error'
                else:
                    print('Connection error')
                    return 'DB Connection Error'
            else:
                print('empty parameters')
                return render_template("changePassword.html", error=error)
        else:
            return render_template("changePassword.html", error=error)
            
                                
    except Exception as e:
        return render_template("changePassword.html", error=e)

    return render_template("changePassword.html", error=error)

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
                if conn != None:  # Checking if connection is None
                    if conn.is_connected():  # Checking if connection is established
                        print('MySQL Connection is established')
                        dbcursor = conn.cursor()  # Creating cursor object
                        # here we should check if email / email already exists
                        # hashing password
                        password = sha256_crypt.hash((str(password)))

                        Verify_Query = "SELECT * FROM users WHERE email = %s;"
                        dbcursor.execute(Verify_Query, (email,))
                        rows = dbcursor.fetchall()
                        if dbcursor.rowcount > 0:  # this means there is a user with same email
                            print('email already taken, please choose another')
                            error = "Email already taken, please choose another"
                            return render_template("registerJinja.html", error=error)
                        else:  # this means we can add new user
                            dbcursor.execute("INSERT INTO users (first_name, last_name, email, password_hash) VALUES (%s, %s, %s, %s)", (
                                firstName, lastName, email, password))
                            conn.commit()  # saves data in database
                            print("Thanks for registering!")
                            dbcursor.close()
                            conn.close()
                            gc.collect()
                            session['logged_in'] = True  #  session variables
                            session['email'] = email
                            # default all users are standard
                            session['usertype'] = 'standard'
                            return render_template('standarduser.html',
                                                       user=session['email'],
                                                       usertype=session['usertype'])
                            # return render_template("success.html",
                            #                        message='User registered successfully and logged in..')
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


# We also write a wrapper for admin user(s). It will check with the user is
# logged in and the usertype is admin and only then it will allow user to
# perform admin functions
def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if ('logged_in' in session) and (session['usertype'] == 'admin'):
            return f(*args, **kwargs)
        else:
            print("You need to login first as admin user")
            # return redirect(url_for('login', error='You need to login first as admin user'))
            return render_template('loginJinja.html', error='You need to login first as admin user')
    return wrap


# We also write a wrapper for standard user(s). It will check with the usertype is
# standard and user is logged in, only then it will allow user to perform standard user functions
def standard_user_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if ('logged_in' in session) and (session['usertype'] == 'standard'):
            return f(*args, **kwargs)
        else:
            print("You need to login first as standard user")
            # return redirect(url_for('login', error='You need to login first as standard user'))
            return render_template('loginJinja.html', error='You need to login first as standard user')
    return wrap

# /userfeatures is loaded for standard users
# Here we us @standard_user_login_required wrapper ...
# this means that only users with user type standard can access this function
# the function implements features related to standard users


@app.route('/userfeatures')
@login_required
@standard_user_required
def user_features():
    print('fetchrecords')
    # records from database can be derived
    # user login can be checked..
    print('Welcome ', session['email'])
    return render_template('standarduser.html',
                           user=session['email'], message='User data from app and standard \
                user features can go here....')

# /adminfeatures is loaded for admin users
# Here we us @admin_required wrapper ...
# this means that only users with user type admin can access this function
# the function implements features related to admin users


@app.route('/adminfeatures')
@login_required
@admin_required
def admin_features():
    print('create / amend records / delete records / generate reports')
    # records from database can be derived, updated, added, deleted
    # user login can be checked..
    print('Welcome ', session['email'], ' as ', session['usertype'])
    return render_template('adminuser.html', user=session['email'],
                           message='Admin data from app and admin features can go here ...')


@app.route('/base')
def base_route():
    return render_template('baseHTML.html')


if __name__ == '__main__':
    app.run(debug=True)

# Process:
# 1. Put html files under templates folder             DONE
# 2. Put static files (i.e. css and images and js files) under static folder      DONE
    # 2a. you may create sub-folders i.e. css for CSS files, img for Images
# 3. Make app i.e. .py file and create decorates/endpoints for each webpage so that you can link them using url_for()          DONE
    # 3a. use render_template() to return the html page
# 4. Update <link> tag in html files to refer to css by using url_for()
# 5. Update <a> tag href attribute to call end point for each page by using url_for()
# 6. Update <img> tag src attribute to link to images e.g., 'static/image.jpeg'
# 7. Update css file if you're using background images e.g., 'static/image.jpeg'
