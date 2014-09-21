import MySQLdb
import sys
from random import shuffle

dbname = sys.argv[1]

con = MySQLdb.connect(host="localhost",read_default_file="~/.my.cnf",db=dbname)

cursor = con.cursor(MySQLdb.cursors.SSCursor)


def fetchsome(cursor, some=1000):
    fetch = cursor.fetchmany
    while True:
        rows = fetch(some)
        if not rows: break
        for row in rows:
            yield row 


cursor.execute("SELECT bookid,casesens,count FROM master_bookcounts IGNORE INDEX (wordid) JOIN wordsheap USING (wordid) WHERE wordid < 20000 AND wordid > 20;")



current_book = []
last_book_id = None
for row in fetchsome(cursor):
    (book,word,count) = row
    if book != last_book_id and last_book_id is not None:
        shuffle(current_book)
        print "%d\t%s" % (last_book_id," ".join(current_book))
        current_book = []
    current_book = current_book + [word]*count
    last_book_id = book
