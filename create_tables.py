import sqlite3
con = sqlite3.connect('example.db')
cur = con.cursor()

sql = '''
   CREATE TABLE Contacts (
   ID INTEGER PRIMARY KEY,  
   Name varchar(255) NOT NULL,
   Surname varchar(255) NOT NULL,
   Phone varchar(255) NOT NULL,
   Address varchar(255),
   Country varchar(255),
   Town varchar(255),
   Street varchar(255), 
   Url varchar(255), 
   Photo  varchar(255)
   )'''
cur.execute(sql)

con.commit()
con.close()



