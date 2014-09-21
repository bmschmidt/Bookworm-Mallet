import MySQLdb
import sys
from random import shuffle
import ConfigParser as conf

confs = conf.RawConfigParser()
confs.read("../../bookworm.cnf")
dbname = confs.get("client","database")
con = MySQLdb.connect(host="localhost",read_default_file="~/.my.cnf",db=dbname)

cursor = con.cursor(MySQLdb.cursors.SSCursor)


def fetchsome(cursor, some=1000):
    fetch = cursor.fetchmany
    while True:
        rows = fetch(some)
        if not rows: break
        for row in rows:
            yield row 


cursor.execute("SELECT bookid,wordid,count FROM master_bookcounts JOIN stopwords USING (wordid) WHERE stopword=0 ORDER BY bookid")

current_book = []
last_book_id = None
for row in fetchsome(cursor):
    (book,word,count) = row
    word = str(word)
    if book != last_book_id and last_book_id is not None:
        shuffle(current_book)
        print "%d\t%s" % (last_book_id," ".join(current_book))
        current_book = []
    current_book = current_book + [word]*count
    last_book_id = book
