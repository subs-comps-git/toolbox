"""Load downloaded data into sqlite


"""


import sqlite3
import os


def create_schema(db_name, db_schema):
    with sqlite3.connect(db_name) as conn:
        print('Creating schema')
        with open(db_schema, 'r') as f:
            schema = f.read()
        try:
            conn.executescript(schema)
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])


def create_database(filename, db_schema):
    db_filename = filename
    db_is_new = not os.path.exists(db_filename)
    conn = sqlite3.connect(db_filename)
    if db_is_new:
        create_schema(db_filename, db_schema)
    else:
        print('Database exists, assume schema does too.')
    conn.close()


def load_data(db_name, gp_data, gp_sql, names_sql):
    with sqlite3.connect(db_name) as conn:
        try:
            cursor = conn.cursor()
            for row in gp_data:
                name, total, character, ship = row[0], row[1], row[2], row[3]
                try:
                    cursor.execute(gp_sql, (name, total, character, ship))
                except sqlite3.Error as e:
                    cursor.execute(names_sql, (name,))
                    cursor.execute(gp_sql, (name, total, character, ship))
            conn.commit()
        except sqlite3.Error as e:
            print('An error occurred:', e.args[0])
            conn.rollback()


def print_data(db_name, sql):
    with sqlite3.connect(db_name) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(dict(row))
