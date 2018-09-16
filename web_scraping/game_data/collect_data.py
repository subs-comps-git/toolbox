"""Main program to collect swgoh guild data


"""


import sqlite3
import get_gp_data as gp_data
import load_sql as load


def connect_db(db_name):
    db_uri = f'file:{db_name}?mode=rw'
    try:
        conn = sqlite3.connect(db_uri, uri=True)
        cursor = conn.cursor()
        cursor.execute(
            """SELECT name
             FROM sqlite_master
             WHERE type='table' AND name = 'gp'
             ORDER BY 1"""
        )
        if cursor.fetchone():
            print('Found tables')
            return conn
        else:
            print("No tables found.")
            raise sqlite3.DatabaseError
    except sqlite3.DatabaseError:
        conn = sqlite3.connect(db_name)
        load.create_schema(conn, '../swgoh.sql')
        return conn


def main():
    """Collect data from swgoh.gg and load database.

    """

    # Guild data website.
    url = 'https://swgoh.gg/g/11008/hansoloshotfirst/gp/'
    # SQL
    insert_gp = """
        INSERT INTO gp
         (u_id, dl_date, total_gp, char_gp, ship_gp)
        VALUES
         ((SELECT uid FROM users WHERE name = ?), (strftime('%s', 'now')), ?, ?, ?);
        """
    insert_names = 'INSERT INTO users (name) VALUES (?);'

    # Collect data
    html_data = gp_data.get_html(url)
    swgoh_soup = gp_data.make_soup(html_data, 'html5lib')
    gp = gp_data.make_gp_list(swgoh_soup)

    # Load database
    db_name = 'swgoh.db'
    db_schema = 'swgoh.sql'
    conn = load.setup_database(db_name, db_schema)
    load.load_data(conn, gp, insert_gp, insert_names)
    conn.close()


if __name__ == '__main__':
    main()
