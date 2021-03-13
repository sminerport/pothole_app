from itertools import groupby
import sqlite3
from main import get_db_connection

conn = get_db_connection()

result = conn.execute("select FULLNAME, ZIPLEFT \
                                from DenverStreets \
                                where JURISID == 'DENVER' \
                                group by fullname') AS t").fetchall()


streetList = {}
