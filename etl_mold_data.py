import os
import glob
import psycopg2
import pandas as pd
from sql_queries_mold_tables import insert_queries

def insert_budgetdata(cur, filepath, query):
    """loaclにある前処理後の予算データをテーブルに取り込む関数
    Args:
        cur: cursor object
        filepath: string, filepath to csvfiles
    Returns:
        None
    """
    # Load tidy mold data
    df = pd.read_csv(filepath)

    # Insert budget mold data into tables
    if query == "budget_info_insert":
        budget_info_df = df[
            "serial_no",
            "budget_no",
            "apply_unit",
            "status",
            "sokei_no",
            "plant",
            "product_name",
            "description",
            "o_r_e",
            "oe_code",
            "vehicle",
            "tire_grp",
            "li",
            "ss",
            "sec",
            "sr",
            "rim",
            "mpp_info"]
        # Convert Dataframe to List to insert DB
        listed_df = []
        for row in budget_info_df.itertuples(name=None):
            listed_df.append(list(row))
        # Insert list values to DB
        # insert_queries[0]; INSERT query for budget info. 
        cur.execute(insert_queries[0], listed_df)
    if query == "budget_num_insert":
        budget_num_df = df[
            "serial_no",
            "budget_no",
            "unit_price",
            "budget_num"]
        listed_df = []
        for row in budget_num_df.itertuples(name=None):
            listed_df.append(list(row))
        # insert_queries[1]; INSERT query for budget mold number.
        cur.execute(insert_queries[1], listed_df)

def insert_actualdata(cur, filepath, query):
    """loaclにある前処理後の実績データをテーブルに取り込む関数
    Args:
        cur: cursor object
        filepath: string, filepath to csvfiles
        query: sql_queries_mold_tables.py からinsert文をインポート
    Returns:
        None
    """
    df = pd.read_csv(filepath)

    if query == "actual_info_insert":
        actual_info_df = df[
            "serial_no",
            "budget_no",
            "apply_unit",
            "status",
            "sokei_no",
            "plant",
            "product_name",
            "description",
            "o_r_e",
            "oe_code",
            "vehicle",
            "tire_grp",
            "li",
            "ss",
            "sec",
            "sr",
            "rim",
            "mpp_info"
        ]
        listed_df = []
        for row in actual_info_df.itertuples(name=None):
            listed_df.append(row)
        # insert_queries[2]; INSERT query for actual info.
        cur.execute(insert_queries[2], listed_df)

    if query == "actual_num_insert":
        actual_num_df = df[
            "serial_no",
            "budget_no",
            "ex_serial_no",
            "actual_num"
        ]
        listed_df = []
        for row in actual_num_df.itertuples(name=None):
            listed_df.append(row)
        # insert_queries[3]; INSERT query for actual mold number.
        cur.execute(insert_queries[3], listed_df)

def process_molddata(cur, conn, filepath, func):
    """
    """
