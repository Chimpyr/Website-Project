import mysql.connector, dbfunc
conn = dbfunc.getConnection()   #connection to DB
DB_NAME = input('Enter Database Name: ')            #DB Name
TABLE_NAME = input('Enter Table Name: ')
tid = input('Enter TempID: ')
# here you should perform data validation syntax/semantics 
DELETE_statement = 'DELETE FROM ' + TABLE_NAME + ' \
    WHERE tempId = %s;' 
    
if conn != None:    #Checking if connection is None
    if conn.is_connected(): #Checking if connection is established
        print('MySQL Connection is established')                          
        dbcursor = conn.cursor()    #Creating cursor object
        dbcursor.execute('USE {};'.format(DB_NAME)) #use database        
        dataset = (tid,)        
        dbcursor.execute(DELETE_statement, dataset)   
        conn.commit()              
        print('DELETE statement executed successfully.') 
        dbcursor.close()              
        conn.close() #Connection must be closed
    else:
        print('DB connection error')
else:
    print('DBFunc error')
