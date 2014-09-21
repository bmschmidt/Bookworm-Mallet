import MySQLdb
import sys
from random import shuffle
import ConfigParser as conf

confs = conf.RawConfigParser()
confs.read("../../bookworm.cnf")
dbname = confs.get("client","database")

con = MySQLdb.connect(host="localhost",read_default_file="~/.my.cnf",db=dbname)

cursor = con.cursor(MySQLdb.cursors.SSCursor)


#cursor.execute("DROP TABLE IF EXISTS master_topicWords")
#cursor.execute("CREATE TABLE master_topicWords (bookid MEDIUMINT UNSIGNED, wordid MEDIUMINT, topic SMALLINT UNSIGNED, count MEDIUMINT,PRIMARY KEY (wordid,bookid,count),INDEX(topic,wordid,bookid,count))")
#cursor.execute("LOAD DATA LOCAL INFILE 'master_topics.txt' INTO TABLE master_topicWords")


seen = dict()

cursor.execute("DROP TABLE IF EXISTS topic_labels")
cursor.execute("CREATE TABLE IF NOT EXISTS topic_labels (topic SMALLINT UNSIGNED, PRIMARY KEY (topic), topic_label VARCHAR(10000)) ENGINE=MYISAM")


for line in open("keys.txt"):
    line = line.split("\t")
    topic = line[0]
    words = line[2].split(" ")
    tokens = []
    n = 0
    for wordid in words:
        if wordid=="":
            continue
        try:
            token = seen[wordid]
        except KeyError:
            cursor.execute("SELECT casesens FROM wordsheap WHERE wordid=%s" % wordid)
            seen[wordid] = cursor.fetchall()[0][0]
            token = seen[wordid]
        tokens.append(token)
        n+=1
        if n > 6:
            break
        
    cursor.execute("INSERT INTO topic_labels VALUES (%s,'%s')" %(topic," ".join(tokens)))


cursor.execute('INSERT INTO masterVariableTable VALUES ("topic_label","Topic","character","topic_labels","topic","topic","public","")')
cursor.execute('INSERT INTO masterVariableTable VALUES ("topic","Topic Number","lookup","master_topicWords","topic","topic","public","")')
cursor.execute('INSERT INTO masterTableTable VALUES ("topic_labels","master_topicWords","");')
