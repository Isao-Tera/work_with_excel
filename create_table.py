import psycopg2
from connection_postgres import connection_postgres
from sql_queries_mold_tables import create_table_queries, drop_table_queries

def create_tables():
    """テーブルを作成する関数
    Args:
        None
    Returns:

    """
    try:
        # Make connection and cursor objects
        conn_cur = connection_postgres()
        conn = conn_cur[0]
        cur = conn_cur[1]

        # Create tables one by one
        commands = create_table_queries
        for command in commands:
            cur.exectute(command)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
