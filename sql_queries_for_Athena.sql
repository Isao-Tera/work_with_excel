-- Create database
CREATE DATABASE myfirstdb

-- Drop table
DROP TABLE IF EXISTS actualmold

-- Create tables
/* 
Athenaのテーブル名とテーブル列名は小文字にする必要がある
アンダースコアを除く特殊文字列はサポート外
テーブルや列名が数字で始まる場合、引用符"""で囲む
*/

-- Failed to create table
CREATE EXTERNAL TABLE IF NOT EXISTS myfirstdb.actualmold (
    count_flag CHAR, 
    serial_no VARCHAR,
    budget_no VARCHAR,
    unit VARCHAR,
    exchange_unit VARCHAR,
    budget_status STRING,
    sokei_no VARCHAR,
    plant VARCHAR,
    product_name STRING,
    product_description STRING,
    o_r_e VARCHAR,
    oe_code STRING,
    vehicle VARCHAR,
    tire_grp VARCHAR,
    li VARCHAR,
    ss VARCHAR,
    sec VARCHAR,
    sr VARCHAR,
    rim VARCHAR,
    mpp_info STRING,
    unit_price DECIMAL,
    year_month DATE,
    budget_num INT
) ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = ',',
  'field.delim' = ','
) STORED AS TEXTFILE
LOCATION 's3://lambdapoc-files-outputs/'
TBLPROPERTIES (
    'has_encrypted_data'='false',
    'skip.header.line.count'='1',
    'serialization.encoding'='SJIS');

-- Successed to create table
CREATE EXTERNAL TABLE IF NOT EXISTS myfirstdb.actualmold (
    count_flag STRING,
    serial_no STRING,
    budget_no STRING,
    unit STRING,
    exchange_unit STRING,
    budget_status STRING,
    sokei_no STRING,
    plant STRING,
    product_name STRING,
    product_description STRING,
    o_r_e STRING,
    oe_code STRING,
    vehicle STRING,
    tire_grp STRING,
    li STRING,
    ss STRING,
    sec STRING,
    sr STRING,
    rim STRING,
    mpp_info STRING,
    unit_price DECIMAL,
    year_month DATE,
    budget_num INT 
) 
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
         'serialization.format' = ',', 'field.delim' = ',' ) 
         LOCATION 's3://lambdapoc-files-outputs/' TBLPROPERTIES ('has_encrypted_data'='false', 'skip.header.line.count'='1');