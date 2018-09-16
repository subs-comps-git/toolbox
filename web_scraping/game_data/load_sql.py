"""Load data into sqlite


"""


import sqlite3
import sys


def create_schema(conn, db_schema):
    """Create sqlite3 database schema

    Runs a script to create tables in sqlite3.

    Args:
        conn: An open connection to the database.
        db_schema: File containing sql commands to create database tables.

    Raises:
        FileNotFoundError: db_schema file not found.
        sqlite3.Error: An error occurred accessing the database.

    """
    try:
        with open(db_schema, 'rb') as f:
            schema = f.read().decode('utf-8')
        conn.executescript(schema)
    except FileNotFoundError as e:
        print('An error occurred: ', e.args[0])
        conn.close()
        sys.exit(1)
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        conn.close()
        sys.exit(1)


def setup_database(db_name, db_schema):
    """Create sqlite3 database file if non-existent.

    Attempts to open database in read/write mode. Upon error, function creates
    new database file and runs schema script to create tables.

    Args:
        db_name: Name of database as a string.
        db_schema: File containing sql commands to create database tables.

    Returns:
        Open database connection.

    Raises:
        sqlite3.OperationalError: A error occurs is a connection cannot be made to database.

    """
    try:
        db_uri = f'file:{db_name}?mode=rw'
        return sqlite3.connect(db_uri, uri=True)
    except sqlite3.OperationalError as e:
        conn = sqlite3.connect(db_name)
        create_schema(conn, db_schema)
        return conn


def load_data(conn, gp_data, gp_sql, names_sql):
    """Loads data into sqlite3 database.

    Takes list of data and loads it into database given SQL statements, gp_sql
    and names_sql.

    Args:
        conn: Open connection to database.
        gp_data: List containing GP statistics for SWGOH guild.

    Returns:
        Sqlite3 row count of changes to database.

    Raises:
        sqlite3.IntegrityError: An error occurs if user is not found in users table.
            The new user is then added to users table.
        sqlite3.InegrityError: An error occurs if an attempt to add a duplicate user occurs.
        sqlite3.OperationalError: An error is raised if database connection is not open,
            transaction cannot be processed, or data source name is not found.
        sqlite3.ProgrammingError: An error occurs on SQL syntax errors, table not found,
            wrong number of parameters, etc.
    """
    cursor = conn.cursor()
    try:
        cursor.executemany(gp_sql, gp_data)
        conn.commit()
        return cursor.rowcount
    except sqlite3.IntegrityError:
        for row in gp_data:
            try:
                cursor.execute(names_sql, (row[0],))
                cursor.execute(gp_sql, row)
            except sqlite3.IntegrityError:
                cursor.execute(gp_sql, row)
                continue
        conn.commit()
        return cursor.rowcount
    except sqlite3.OperationalError as e:
        print('Operational error:', e)
        conn.rollback()
        sys.exit(4)
    except sqlite3.ProgrammingError as e:
        print('ProgrammingError error:', e)
        conn.rollback()
        sys.exit(5)


def print_data(conn, sql):
    """prints data retrieved from database.

    Function to retrieve and print data from database given a SQL statement.

    Args:
        conn: Open connection to database.
        sql: Sqlite3 SQL SELECT statement.

    Returns:
        Prints data retrieved by SELECT statement
    """
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print(dict(row))
