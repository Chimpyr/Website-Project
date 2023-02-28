import mysql.connector, dbfunc
conn = dbfunc.getConnection()   #connection to DB
DB_NAME = input('Enter Database Name: ')            #DB Name
TABLE_NAME = input('Enter Table Name: ')
user_id = input('Enter ID: ')
first_name = input('Enter First Name: ')
last_name = input('Enter Last Name: ')
email = input('Enter email: ')
password_hash = input('Enter password: ')
usertype = input('Enter usertype: ')
# here you should perform data validation 
# syntax as well as semantics 

# INSERT_statement = 'INSERT INTO ' + TABLE_NAME + ' (\
#     tempId, Name, ADDRESS) VALUES (%s, %s, %s);'    

INSERT_statement = 'INSERT INTO ' + TABLE_NAME + ' (\
    user_id, first_name, last_name, email, password_hash, usertype) VALUES (%s, %s, %s, %s, %s, %s);'

if conn != None:    #Checking if connection is None
    if conn.is_connected(): #Checking if connection is established
        print('MySQL Connection is established')                          
        dbcursor = conn.cursor()    #Creating cursor object
        dbcursor.execute('USE {};'.format(DB_NAME)) #use database        
        dataset = (user_id, first_name, last_name, email, password_hash, usertype)        
        dbcursor.execute(INSERT_statement, dataset)   
        conn.commit()              
        print('INSERT query executed successfully.') 
        dbcursor.close()              
        conn.close() #Connection must be closed
    else:
        print('DB connection error')
else:
    print('DBFunc error')
