import pyodbc

# Create connection object
# {ODBC Driver 17 for SQL Server} - supports SQL Server 2008 through 2019
#  you can get the driver names programmatically by running the Python command pyodbc.drivers()

"""
A DSN (or Data Source Name) allows you to define the ODBC driver, server, database, login credentials (possibly), 
and other connection attributes all in one place, so you don't have to provide them in your connection string. 
You can set up DSNs on your PC by using your ODBC Data Source Administrator window.

To get to your ODBC Data Source Administrator window, navigate to 
'Control Panel -> Administrative Tools -> Data Sources (ODBC)'. 
Under the tabs 'User DSN' or 'System DSN' click on the 'Add...' button and follow the wizard instructions. 
'User DSN' is for just you, 'System DSN' is for all users. 
Choose a driver that is suitable for the version of SQL Server you are connecting to,
 and add any other connection information that is relevant. 

You can connect to your SQL Server instance using a trusted connection, 
i.e. using your Windows account rather than a login name and password, 
by using the Trusted_Connection attribute

when autocommit is True, the database will executes a commit after each SQL statement, not pyodbc.
"""
conn = pyodbc.connect('DSN=SQLServer1; Database=test; Trusted_Connection=yes', autocommit=True,)
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=testdb;UID=me;PWD=pass')

# Create cursor
"""
When createing cursor, you will need to specify the encoding type depending on the database.
But pyodbc matches the specificaion of the latest MS SQLserver.
No configuration is needed. Default is recomended.
"""
cur = conn.cursor()

# Inserting data 
cur.executes("INSERT INTO \
tablename ( \
    id, names \
    ) \
values( \
    1, 'tera' \
    ) \
")