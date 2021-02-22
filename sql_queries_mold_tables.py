# Drop tables
budget_info_drop = "DROP TABLES IF EXISTS budget_info"
budget_num_drop = "DROP TABLES IF EXISTS budget_num"
actual_info_drop = "DROP TABLES IF EXISTS actual_info"
actual_num_drop = "DROP TABLES IF EXISTS actual_num"

# Create tables

# 予算テーブル
budget_info_create = ("""
CREATE TABLE IF NOT EXISTS budget_info(
    serial_no varchar PRIMARY KEY,
    budget_no varchar,
    apply_unit char(4),
    status text,
    sokei_no varchar,
    plant char(2),
    product_name varchar,
    description text,
    o_r_e varchar,
    oe_code varchar,
    vehicle varchar,
    tire_grp char(3),
    li varchar,
    ss varchar,
    sec char(3),
    sr varchar,
    rim varchar,
    mpp_info text)"""
)


budget_num_create = ("""
CREATE TABLE IF NOT EXITSTS mold_buget(
    serial_no varchar PRIMARY KEY,
    budget_no varchar,
    unit_price int,
    budget_num int)"""
)

# 実績テーブル
actual_info_create = ("""
CREATE TABLE IF NOT EXISTS actual_info(
    serial_no varchar,
    budget_no varchar PRIMARY KEY,
    apply_unit char(4),
    status text,
    sokei_no varchar,
    plant char(2),
    product_name varchar,
    description text,
    o_r_e varchar,
    oe_code varchar,
    vehicle varchar,
    tire_grp char(3),
    li varchar,
    ss varchar,
    sec char(3),
    sr varchar,
    rim varchar,
    mpp_info text
    )"""
)

actual_num_create = ("""
CREATE TABLE IF NOT EXITSTS actual_num(
    serial_no varchar,
    budget_no varchar PRIMARY KEY,
    ex_serial_no varchar,
    actual_num int)"""
)

# INSERT DATA
budget_info_insert = ("""
    INSERT INTO budget_info(
        serial_no,
        budget_no,
        apply_unit,
        status,
        sokei_no,
        plant,
        product_name,
        description,
        o_r_e,
        oe_code,
        vehicle,
        tire_grp,
        li,
        ss,
        sec,
        sr,
        rim,
        mpp_info
    )
    VALUES(
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s
    )"""
)

buget_num_insert = ("""
    INSERT INTO budget_num(
        serial_no,
        budget_no,
        unit_price,
        budget_num
    )
    VALUES(
        %s,
        %s,
        %s,
        %s
    )"""
)

actual_info_insert = ("""
    INSERT INTO actual_info(
        serial_no,
        budget_no,
        apply_unit,
        status,
        sokei_no,
        plant,
        product_name,
        description,
        o_r_e,
        oe_code,
        vehicle,
        tire_grp,
        li,
        ss,
        sec,
        sr,
        rim,
        mpp_info
    )
    VALUES(
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s
    )"""
)

actual_num_insert = ("""
    INSERT INTO actual_num(
        serial_no varchar,
        budget_no varchar PRIMARY KEY,
        ex_serial_no varchar,
        actual_num int
    )
    VALUES(
        %s,
        %s,
        %s,
        %s
    )"""
)

# Queries List
create_table_queries = [budget_info_create, budget_num_create, actual_info_create, actual_num_create]
drop_table_queries = [budget_info_drop, budget_num_drop, actual_info_drop, actual_num_drop]