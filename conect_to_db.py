# Load packages
from configparser import ConfigParser
import psycopg2

# Use connection paramater from enviroment in database.ini
def config(filename="database.ini", section="postgresql"):
    """
    """
    # create a parser, then read the config file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param()] = param[1]
    else:
        raise Exception(f"section {section} not found in the {filename} file")

    return db



# Make connection and cursor to mold_db in AWS RDS posgtres
def connection_to_db():
    """AWS RDS postgresに接続する関数
    Description:
        1. read connection paramaters from database.ini
        2. conecting the AWS RDS
        3. if success the connection, display the success statement and create a cursor 
        4. if fail to connect to the database, display the error statement
        5. close the connection
    Args:
        none
    Returns:
        conn: connection object
        cur: cursor object to exectute SQL queries
    """
    conn = None
    try:
        # read connection paramaters
        params = config()
        
        # connect to the AWS RDS, then create a cursor
        print("Connecting to the AWS RDS....")
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # excute a succeesful statment
        print("Success to AWS RDS! database version:")
        cur.execute("SELECT version()")

        # display the database version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("I am unable to connect to the database")
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed")


