# Drop tables
budget_info_drop = "DROP TABLE IF EXISTS budget_info"
budget_num_drop = "DROP TABLE IF EXISTS budget_num"
actual_info_drop = "DROP TABLE IF EXISTS actual_info"
actual_num_drop = "DROP TABLE IF EXISTS actual_num"

# Create tables

# 予算テーブル
budget_info_create = ("""
CREATE TABLE IF NOT EXISTS budget_info(
    serial_no varchar,
    budget_no varchar PRIMARY KEY,
    apply_unit char(4),
    status text,
    sokei_no varchar,
    plant varchar,
    product_name varchar,
    description text,
    o_r_e varchar,
    oe_code varchar,
    vehicle varchar,
    tire_grp char(3),
    li varchar,
    ss varchar,
    sec varchar,
    sr varchar,
    rim varchar,
    mpp_info text)"""
)


budget_num_create = ("""
CREATE TABLE IF NOT EXISTS  budget_num(
    serial_no varchar,
    budget_no varchar,
    date date,
    unit_price decimal,
    budget_num decimal,
    PRIMARY KEY(budget_no, date)
    )"""
)

# 実績テーブル
actual_info_create = ("""
CREATE TABLE IF NOT EXISTS actual_info(
    serial_no varchar,
    budget_no varchar PRIMARY KEY,
    apply_unit char(4),
    status text,
    sokei_no varchar,
    plant varchar,
    product_name varchar,
    description text,
    o_r_e varchar,
    oe_code varchar,
    vehicle varchar,
    tire_grp char(3),
    li varchar,
    ss varchar,
    sec varchar,
    sr varchar,
    rim varchar,
    mpp_info text
    )"""
)

actual_num_create = ("""
CREATE TABLE IF NOT EXISTS  actual_num(
    serial_no varchar,
    budget_no varchar,
    ex_serial_no varchar,
    date date,
    unit_price decimal,
    actual_num decimal,
    PRIMARY KEY(budget_no, date)
    )"""
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

budget_num_insert = ("""
    INSERT INTO budget_num(
        serial_no,
        budget_no,
        date,
        unit_price,
        budget_num
    )
    VALUES(
        %s,
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
        serial_no,
        budget_no,
        ex_serial_no,
        date,
        unit_price,
        actual_num
    )
    VALUES(
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    )"""
)

# Queries List
create_table_queries = [budget_info_create, budget_num_create, actual_info_create, actual_num_create]
drop_table_queries = [budget_info_drop, budget_num_drop, actual_info_drop, actual_num_drop]
insert_queries = [budget_info_insert, budget_num_insert, actual_info_insert, actual_num_insert]