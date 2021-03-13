from itertools import groupby
import sqlite3

def get_db_connection():
    conn = sqlite3.connect(".\\db.sqlite")
    conn.row_factory = sqlite3.Row
    return conn

def main():
    conn = get_db_connection()
    
    rows = conn.execute("select FULLNAME, ZIPLEFT \
                                    from DenverStreets \
                                    where JURISID == 'DENVER' \
                                    group by fullname").fetchall()
    
    for row in rows:
        print(f"{row['fullname']}, {row['zipleft']})

if __name__ == '__main__': main()