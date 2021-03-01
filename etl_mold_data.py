import os
import glob
import pandas as pd
from sql_queries_mold_tables import insert_queries
from connection_postgres import connection_postgres

def main():
    conn, cur = connection_postgres()
    process_molddata(conn, cur, filepath=r".\data", func=insert_budgetdata)
    #process_molddata(conn, cur, filepath=r".\data", func=insert_actualdata)
    conn.close()

def insert_budgetdata(cur, filepath):
    """loaclにある前処理後の予算データをテーブルに取り込む関数
    Args:
        cur: cursor object
        filepath: string, filepath to csvfiles
    Returns:
        None
    """
    # Load tidy mold data
    data_type = {
    'count_flag': 'object',
    'serial_no': 'object',
    'budget_no': 'object',
    'apply_unit': 'object',
    'exchange_no': 'object',
    'status': 'object',
    'sokei_no': 'object',
    'plant': 'object',
    'product_name': 'object',
    'description': 'object',
    'o_r_e': 'object',
    'oe_code': 'object',
    'vehicle': 'object',
    'tire_grp': 'object',
    'li': 'object',
    'ss': 'object',
    'sec': 'object',
    'sr': 'object',
    'rim': 'object',
    'mpp_info': 'object',
    'unit_price': 'float64',
    'year_month': 'object',
    'mold_num': 'float64'}
    parse_date = ['year_month',]
    df = pd.read_csv(filepath, dtype=data_type, parse_dates=parse_date)

    # Insert budget mold data into tables
    budget_info_df = df[[
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
    ]]
    # 元データには月別モールド面数を情報を保持していたため、モールド情報テーブルでは、重複を削除する必要がある
    budget_info_df.drop_duplicates(inplace=True)
    
    # Convert Dataframe to List in order to insert DB
    # insert_queries[0]; INSERT query for budget information.
    cur.executemany(insert_queries[0], budget_info_df.values.tolist())

    # Insert budget number into a table
    budget_num_df = df[[
        "serial_no",
        "budget_no",
        "year_month",
        "unit_price",
        "mold_num"
    ]]

    # In the budget_num table, serial_no is the VARCHAR, year_month is date
    budget_num_df["serial_no"] = budget_num_df["serial_no"].astype(str)
    budget_num_df["year_month"] = pd.to_datetime(budget_num_df["year_month"])
    # insert_queries[1]; INSERT query for budget mold number.
    cur.executemany(insert_queries[1], budget_num_df.values.tolist())

def insert_actualdata(cur, filepath):
    """loaclにある前処理後の実績データをテーブルに取り込む関数
    Args:
        cur: cursor object
        filepath: string, filepath to csvfiles
    Returns:
        None
    """
    data_type = {
    'count_flag': 'object',
    'serial_no': 'object',
    'budget_no': 'object',
    'apply_unit': 'object',
    'exchange_no': 'object',
    'status': 'object',
    'sokei_no': 'object',
    'plant': 'object',
    'product_name': 'object',
    'description': 'object',
    'o_r_e': 'object',
    'oe_code': 'object',
    'vehicle': 'object',
    'tire_grp': 'object',
    'li': 'object',
    'ss': 'object',
    'sec': 'object',
    'sr': 'object',
    'rim': 'object',
    'mpp_info': 'object',
    'unit_price': 'float64',
    'year_month': 'object',
    'mold_num': 'float64'}
    parse_date = ['year_month',]
    df = pd.read_csv(filepath, dtype=data_type, parse_dates=parse_date)

    actual_info_df = df[[
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
    ]]

    for row in actual_info_df.itertuples(name=None, index=False):

    # insert_queries[2]; INSERT query for actual info.
        cur.execute(insert_queries[2], list(row))

    actual_num_df = df[[
        "serial_no",
        "budget_no",
        "exchange_no",
        "year_month",
        "unit_price",
        "mold_num"
    ]]
    for row in actual_num_df.itertuples(name=None, index=False):
    # insert_queries[3]; INSERT query for actual mold number.
        cur.execute(insert_queries[3], list(row))

def process_molddata(conn, cur, filepath, func):
    """INSERT queryを実行する関数
    Args:
        conn:connectionクラス　conect to pastgresql at local
        cur:cursor object
        filepath: 前処理後のcsv fileパス　拡張子は除く
        func: INSERTを処理する関数名　予算と実績のデータをテーブルへ入れる関数
    """
    # get csv files from local folder
    abspath_for_files = []
    csv_files = glob.glob(os.path.join(filepath, "*mold.csv"))
    for csvfile in csv_files:
        abs_path = os.path.abspath(csvfile)
        abspath_for_files.append(abs_path)

    # total number of files
    number_files = len(csv_files)
    print(f"{number_files} files were found in {filepath}")

    # iterate over files and process
    for i, datafile in enumerate(abspath_for_files, 1):
        func(cur, datafile)
        conn.commit()
        print(f"{i}/{number_files} files processed")

if __name__ == "__main__":
    main()

