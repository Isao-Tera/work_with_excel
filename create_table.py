import psycopg2
from connection_postgres import connection_postgres
from sql_queries_mold_tables import create_table_queries, drop_table_queries

def create_tables(conn, cur):
    """テーブルを作成する関数
    Args:
        conn: connection class for postgresql
        cur: cursor object for postgres DB
    Returns:
        None, Made four tables 
    """
    try:
        # Create tables one by one
        commands = create_table_queries
        for command in commands:
            cur.execute(command)
        conn.commit()
        print("Success! Made mold data tables")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.close()
        print("connection was closed")

def drop_tables(conn, cur):
    """テーブルを削除する関数
    Args:
        conn: connection class for postgresql
        cur: cursor object for postgres DB
    Returns:
        None, delete four tables 
    """
    commands = drop_table_queries
    try:
        for command in commands:
            cur.execute(command)
        conn.commit
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    
if __name__ == "__main__":
    connection, cursor = connection_postgres()
    drop_tables(connection, cursor)
    create_tables(connection, cursor)
