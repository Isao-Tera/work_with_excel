import psycopg2
import pandas as pd
from sql_queries_mold_tables import *

def insert_csvdata_db(cur, filepath, query):
    """loaclにあるcsv filesをデータベースに取り込む関数
    Args:
        cur: cursor object
        filepath: string, filepath to csvfiles
    Returns:
    
    """
    df = pd.read_csv(filepath)

    # Convert Dataframe to List to insert DB
    listed_df = []
    for row in df.itertuples(name=None):
        listed_df.append(list(row))

    # Insert list values to DB
    cur.execute(query, listed_df)
