"""Load downloaded data into sqlite


"""


import sqlite3
import os
import sys


def connect_db(name):
    return sqlite3.connect(name)


def create_schema(conn, db_schema):
    with open(db_schema, 'r') as f:
        schema = f.read()
    try:
        conn.executescript(schema)
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        sys.exit(1)


def setup_database(filename, db_schema):
    db_is_new = not os.path.exists(filename)
    if db_is_new:
        conn = connect_db(filename)
        create_schema(conn, db_schema)
        return conn
    else:
        print('Database exists, assume schema does too.')
        return connect_db(filename)


def load_data(conn, gp_data, gp_sql, names_sql):
    cursor = conn.cursor()
    try:
        cursor.executemany(gp_sql, gp_data)
        conn.commit()
    except sqlite3.IntegrityError as e:
        for row in gp_data:
            try:
                cursor.execute(names_sql, (row[0],))
                cursor.execute(gp_sql, row)
            except sqlite3.IntegrityError as e:
                cursor.execute(gp_sql, row)
                continue
        conn.commit()
    except sqlite3.OperationalError as e:
        print('Operational error:', e)
        conn.rollback()
        sys.exit(4)
    except sqlite3.ProgrammingError as e:
        print('ProgrammingError error:', e)
        conn.rollback()
        sys.exit(5)
    finally:
        conn.close()


def print_data(conn, sql):
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print(dict(row))
