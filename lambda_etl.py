import boto3
import os
from io import StringIO
from datetime import datetime as dt
import pandas as pd

# Excelから抽出が必要な列名
names = [
    "需要カウント",
    "9042付与セリアル(管理)番号",
    "予算管理#",
    "申請部署",
    "転用元(予算振替管理用)",
    "ステータスリスト/手配済・白紙化・翌年以降へ延期(スケジュール必ず更新)より選択",
    "総合計画No",
    "設定工場",
    "商品名",
    "案件名",
    "仕向先/OE/REP/EXP",
    "OEｺｰﾄﾞ",
    "車種",
    "GRP",
    "LI_1",
    "SS",
    "SEC",
    "SR",
    "RIM",
    "生産準備依頼(MPP)/PO発行情報", 
    "仮単価"]

actual_mold_num = [
    "発注面数1月",
    "発注面数2月",
    "発注面数3月",
    "発注面数4月",
    "発注面数5月",
    "発注面数6月",
    "発注面数7月",
    "発注面数8月",
    "発注面数9月",
    "発注面数10月",
    "発注面数11月",
    "発注面数12月"]

budget_mold_num = [
    "Y1st(OB)/1月",
    "Y1st(OB)/2月",
    "Y1st(OB)/3月",
    "Y1st(OB)/4月",
    "Y1st(OB)/5月",
    "Y1st(OB)/6月",
    "Y1st(OB)/7月",
    "Y1st(OB)/8月",
    "Y1st(OB)/9月",
    "Y1st(OB)/10月",
    "Y1st(OB)/11月",
    "Y1st(OB)/12月"]

# Excelファイルから抽出が必要な行
units = [2021, 2022]
count_flag = ["Y"]

# 英語の列名
new_colname = [
    "count_flag",
    "serial_no",
    "budget_no",
    "apply_unit",
    "exchange_no",
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
    "mpp_info",
    "unit_price",
    "year_month",
    "mold_num"
]

# 予算エクセルファイルの設定；データのあるシート＆読み込み開始行
sheetname = "21OB_MBP"
header = 3

def lambda_handler(event, context):
    """S3イベント入力（Excelファイルの保存）を受け取り、前処理を実行後ターゲットバケットにCSVとして保存する"""

    # S3から通知されてくるEventからアップロードされたファイル名とバケットを取得する
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key_name = event['Records'][0]['s3']['object']['key']

    df = load_excel_fromS3(bucket_name, key_name)
    converted_df = (df.pipe(select_columns, names, budget_mold_num)
                    .pipe(filter_rows, units=units,count_flag=count_flag)
                    .pipe(convert_long, convert_type="budget")
                   )
    # Rename column name for database
    converted_df.columns = new_colname

    # Output a csv file on S3
    write_df_toS3(converted_df, bucket="lambdapoc-files-outputs", output="tidydata.csv")

# get row data from S3
def load_excel_fromS3(event_bucket, event_key, sheet_name=sheetname, header=header):
    """pandasを使ってExcelファイルを読み込む関数
    Args:
        event_bucket: Lambda受け取るイベントにおいて、データが保存されるS3 bucket
        event_key: Lambda受け取るイベントにおいて、実績データ（Excel file）
        sheet_name: 文字列　予算や実績データがあるExcelシート名
        header: 整数型　読み込みをスキップする行数
    Returns:
        df: dataframe 
    """
    s3_client = boto3.client("s3")

    # get_object() returns a dictionary type
    obj = s3_client.get_object(Bucket=event_bucket, key=event_key)
    
    # 'Body': StreamingBody() object data
    df = pd.read_excel(
        obj["Body"],
        sheet_name=sheetname,
        header=header)
    return df

# Write dataframe to csv on S3
def write_df_toS3(df, bucket, output):
    """前処理後のExcelファイルをcsvでS3に保存する関数
    Args:
        df: dataframe
        bucket: string csv fileを保存するバケット名
        output: string csv file名
    Returns: None
    """
    #　オブジェクトの データを バイト列形式扱うためにbufferオブジェクトを作る
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, sep = ",", index=False)

    # Create S3 object then 保存したいデータをputメソッドに渡す
    # putメソッドにデータを渡すときの引数Body;  (bytes or seekable file-like object) -- Object data.
    s3_resource = boto3.resource("s3")
    s3_resource.Object(bucket, output).put(Body=csv_buffer.getvalue())


# Select necessary columns
def select_columns(df, col_items, col_value):
    """データ集計に必要な列を選択する関数
    Args:
        df: モールド実績データのExcelファイルをpandasで読み込んだdataframe
        col_items: リスト形式 予算No.など属性(names)を表す列
        col_value: リスト形式　予算の値(budget_mold_num) or 実績の値(actual_mold_num)がある列
    Returns:
        df_selected: 必要な列名のみ選択したdataframe
    """
    col_names = col_items + col_value
    df_selected = df[col_names]
    return df_selected


# Filter necessary rows
def filter_rows(df, count_flag, units):
    """データ集計に必要な行を選択する関数
    description:
        需要カウント: データを集計が必要なフラグを示す列
        申請部署: 予算申請部署を示す列、商品計画部は[2021, 2022]
        予算管理#: 承認された予算を示す列
        　　　　　 naは予算を実行化できないため不要
    Args:
        df: モールド実績データのExcelファイルをpandasで読み込んだdataframe
        units: 集計対象となる部署のリスト
        count_flag: 集計フラグのリスト、基本は（"Y"）のみ
    Returns:
        df_filtered: 必要な行を抽出したdataframe
    """
    df_filtered = df.query(f"需要カウント in {count_flag} and 申請部署 in {units}").dropna(subset=["予算管理#"])
    return df_filtered

# Convert a String to Datetime
def convert_to_date(df_col):
    """モールド予算または実績の月をdate型に変換する関数
    Args:
        df_col: pandas series 文字列で1月から12月までのデータがある
            予算：Y1st(OB)/N月
            実績：発注面数N月
    Returns:
        datetime
    """
    # ループ処理が昇順の場合、発注面数12月　は2月、発注面数11月　は1月と判断される。
    # 回避のため降順にループ処理を設定する
    for i in reversed(range(1,13)):
        mon_str = f"{i}月"
        if mon_str in df_col:
            return pd.to_datetime(str(dt.today().year) + "/" + f"{i}")


def convert_long(df_extracted, convert_type="actual", keep_col=names):
    """モールド面数データが月毎に列になっているのを行に変換する関数。
    description:
        条件必要な行と列を抽出後に実行する。
    Args:
        df_extracted: 行と列を抽出後のdataframe
        convert_type: 予算ファイルならば"budget", 実績ファイルなら"actual"と指定する
        keep_col: 列のまま保持する列名のList　namesというグローバル変数をデフォルト設定
    Returns:
        df_melted: dataframe (縦長の形式) 
    """
    if convert_type == "actual":
        var_name="actual_month"
        value_name="a_mold_num"
        df_melted = df_extracted.melt(id_vars=keep_col, var_name=var_name, value_name=value_name)
        # 各月のデータがある列は、文字列（発注面数1月など）となっているので、日付型に変換する
        df_melted[var_name] = df_melted[var_name].apply(convert_to_date)

    elif convert_type == "budget":
        var_name="budget_month"
        value_name="b_mold_num"
        df_melted = df_extracted.melt(id_vars=keep_col, var_name=var_name, value_name=value_name)
        df_melted[var_name] = df_melted[var_name].apply(convert_to_date)

    return df_melted