"""Report change in Galactic power over a given time period


"""


import maya
import sqlite3
import csv


def connect_db(name):
    return sqlite3.connect(name)


def report_gp_deltas(conn, end, start='now'):
    params = {'start': maya.when(start).date.strftime('%Y-%m-%d'),
              'end': maya.when(end).date.strftime('%Y-%m-%d')}

    delta_sql = """SELECT DISTINCT
     DATE(dl_date, 'unixepoch') as date,
     name,
     total_gp,
     char_gp,
     ship_gp,
     MAX(total_gp) - MIN(total_gp) as Total,
     MAX(char_gp) - MIN(char_gp) as character,
     MAX(ship_gp) - MIN(ship_gp) as ship
     FROM gp g
     JOIN users u ON u.uid = g.u_id
     WHERE date == :start OR date = :end
     GROUP BY name
     HAVING MAX(date) and Total > 0
     ORDER BY name
    """

    # conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(delta_sql, params)
    rows = cursor.fetchall()
    return rows


def export_csv(filename, rows_obj):
    filename = f'reports/{filename}'
    headers = ['Date', 'Name', 'Current GP', 'Current Character GP',
               'Current Ship GP', '14 Day Change', 'Character Change',
               'Ship Change']
    with open(filename, 'w', newline='', encoding='utf-8') as cvsfile:
        writer = csv.writer(cvsfile, dialect='excel')
        writer.writerow(headers)
        writer.writerows(rows_obj)


def main():
    db = 'swgoh.db'
    time_period = '2018-08-29'
    today = maya.now().date.strftime('%Y-%m-%d')
    csv_file = f'gp_delta_hssf_{today}.csv'
    conn = connect_db(db)
    report = report_gp_deltas(conn, time_period)
    if not report:
        print("No rows found.")
    else:
        print(report)
        export_csv(csv_file, report)
    conn.close()


if __name__ == '__main__':
    main()
