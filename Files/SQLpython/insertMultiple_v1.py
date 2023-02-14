import mysql.connector, dbfunc
conn = dbfunc.getConnection()   #connection to DB
DB_NAME = input('Enter Database Name: ')            #DB Name
TABLE_NAME = input('Enter Table Name: ')
INSERT_statement = 'INSERT INTO ' + TABLE_NAME + ' (\
    tempId, Name, Address) VALUES (%s, %s, %s);'    
if conn != None:    #Checking if connection is None
    if conn.is_connected(): #Checking if connection is established
        print('MySQL Connection is established')                          
        dbcursor = conn.cursor()    #Creating cursor object
        dbcursor.execute('USE {};'.format(DB_NAME)) #use database        
        dataset = [ (1000,'David Cameron','London, UK'),
            (2000,'James Bond','Surrey, UK'),
            (3000,'Katie Williams','Leeds, UK'),
            (4000,'Amanda Harris','Manchester, UK'),
            (5000,'Zaheer Khan','Bristol, UK'),
            (6000,'Amber Rudd','Kent, UK'),
            (7000,'Julia Roberts','NY, US') ]        
        dbcursor.executemany(INSERT_statement, dataset) #multiple datasets  
        conn.commit()              
        print('INSERT query executed successfully.') 
        dbcursor.close()              
        conn.close() #Connection must be closed
    else:
        print('DB connection error')
else:
    print('DBFunc error')
