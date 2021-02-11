# Libraries
import pandas as pd
from datetime import datetime as dt

# Load data
df = pd.read_excel(
    "②【一般モールド】20-23年サイズ別明細(12.23展開).xlsx", 
    sheet_name="21OB_MBP",
    header=3)

# Neccerary columns
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

#df_s = select_columns(df, col_names)
#print(df_s.head())


# Filter necessary rows
# unit_names = [2021, 2022]

def filter_rows(df):
    """データ集計に必要な行を選択する関数
    description:
        需要カウント: モールド実績を集計が必要なフラグ（"Y"）のみ
        申請部署: 商品計画部[2021, 2022]のみ
        予算管理#: naは予算を実行化できないため不要
    Args:
        df: モールド実績データのExcelファイルをpandasで読み込んだdataframe
    Returns:
        df_filtered: 必要な行を抽出したdataframe
    """
    df_filtered = df.query("需要カウント == 'Y' and 申請部署 in [2021, 2022]").dropna(subset=["予算管理#"])
    return df_filtered

df_f = filter_rows(df)
print(df_f.head())

def conver_long(df_extracted, converted_type="actual", keep_col=names):
    """モールド面数データが月毎に列になっているのを行に変換する関数。
    description:
        条件必要な行と列を抽出後に実行する。
    Args:
        df_extracted: 行と列を抽出後のdataframe
        converted_type: 予算ファイルならば"budget", 実績ファイルなら"actual"と指定する
        keep_col: 列のまま保持する列名のList　namesというグローバル変数をデフォルト設定
    Returns:
        df_converted: dataframe
    """
    if converted_type == "actual":
        var_name="actual_month"
        value_name="a_mold_num"

    elif converted_type == "budget":
        var_name="budget_month"
        value_name="b_mold_num"

    df_converted = df_extracted.melt(id_vars=keep_col, var_name=var_name, value_name=value_name)
    return df_converted

def trans_date(x):
    """モールド予算または実績の月をdate型に変換する関数
    Args:
        x: pandas series 文字列で1月から12月までのデータがある
            予算：Y1st(OB)/N月
            実績：発注面数N月
    Returns:
        datetime
    """
    if "1月" in x:
        return pd.to_datetime(str(dt.today().year) + "/" + "1")
    elif "2月" in x:
        return pd.to_datetime(str(dt.today().year) + "/" + "2")
    elif "3月" in x:
        return pd.to_datetime(str(dt.today().year) + "/" + "3")
    elif "4月" in x:
        return pd.to_datetime(str(dt.today().year) + "/" + "4")
    elif "5月" in x:
        return pd.to_datetime(str(dt.today().year) + "/" + "5")
    elif "6月" in x:
        return pd.to_datetime(str(dt.today().year) + "/" + "6")
    elif "7月" in x:
        return pd.to_datetime(str(dt.today().year) + "/" + "7")
    elif "8月" in x:
        return pd.to_datetime(str(dt.today().year) + "/" + "8")
    elif "9月" in x:
        return pd.to_datetime(str(dt.today().year) + "/" + "9")
    elif "10月" in x:
        return pd.to_datetime(str(dt.today().year) + "/" + "10")
    elif "11月" in x:
        return pd.to_datetime(str(dt.today().year) + "/" + "11")
    elif "12月" in x:
        return pd.to_datetime(str(dt.today().year) + "/" + "12")