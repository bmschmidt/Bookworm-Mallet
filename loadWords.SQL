
DELETE FROM master_bookcounts;
ALTER IGNORE TABLE master_bookcounts ADD topic SMALLINT UNSIGNED;
ALTER IGNORE TABLE master_bookcounts ADD INDEX (topic,bookid,count);
ALTER IGNORE TABLE master_bookcounts ADD INDEX (wordid,bookid,topic,count);
LOAD DATA LOCAL INFILE "newBookcounts.txt" INTO TABLE master_bookcounts (bookid,wordid,topic,count);

