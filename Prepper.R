#!/usr/bin/R

library(RMySQL)
library(dplyr)

a= read.table("../../bookworm.cnf",sep="=",row.names=NULL);
names(a) = c("k","v");
a$k = gsub(" $","",a$k);
a$v = gsub("^ ","",a$v); 
dbname = as.character(a$v[a$k=="database"])
cat(dbname)

con = dbConnect("MySQL",dbname=dbname)

words = dbGetQuery(con,"SELECT * FROM wordsheap")
stopwords = read.table("bookwormStopwords.txt",sep="\t",quote="")
names(stopwords) = "lowercase"
stopwords$stopword = 1

output = words %>% left_join(stopwords)
output$stopword[nchar(iconv(output$word))==1] = 1
output$stopword[output$wordid>50000] = 1
output$stopword[is.na(output$stopword)] = 0

output = output %>% select(wordid,stopword)

dbGetQuery(con,"DROP TABLE IF EXISTS stopwords")
dbGetQuery(con,"CREATE TABLE stopwords (wordid MEDIUMINT, PRIMARY KEY (wordid), stopword TINYINT);")
write.table(output,file="stopwords.txt",sep="\t",row.names=F,col.names=F)

dbGetQuery(con,"LOAD DATA LOCAL INFILE 'stopwords.txt' INTO TABLE stopwords")

