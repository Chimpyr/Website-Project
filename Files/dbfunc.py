import mysql.connector
from mysql.connector import errorcode
#22011032_Jacob_Craig 
# MYSQL CONFIG VARIABLES
hostname    = "localhost"
username    = "root"
passwd  = "pass" 
database = "horizon_travels_test"

# Function to get connection to the database, code from Zaheer
def getConnection():    
    try:
        conn = mysql.connector.connect(host=hostname,                              
                              user=username,
                              password=passwd,
                              database=database)  
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('User name or Password is not working')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist')
        else:
            print(err)                        
    else:  #will execute if there is no exception raised in try block
        return conn   
                
