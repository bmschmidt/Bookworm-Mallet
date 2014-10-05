nTopics=63
dbName=$(shell cat ../../bookworm.cnf | sed -n 's/database *= *\(.*\)/\1/p')


all: topic-state.gz doneLoading

clean:
	rm -f stopwords.txt
	rm -f fakeinput.txt
	rm -f files.mallet
	rm -f topic-state.gz
	rm -f master_topics.txt

stopwords.txt:
	Rscript Prepper.R

fakeinput.txt: stopwords.txt
	python makefakevocab.py > $@

files.mallet: bookwormStopwords.txt fakeinput.txt
	~/mallet-2.0.7/bin/mallet import-file --input fakeinput.txt --output files.mallet --keep-sequence --token-regex "[0-9A-Z]+"

topic-state.gz: files.mallet
	~/mallet-2.0.7/bin/mallet train-topics --input files.mallet --num-topics $(nTopics) --output-state topic-state.gz --output-topic-keys keys.txt --output-doc-topics compostion.txt --optimize-interval 20 --num-threads 6

cleanFifo:
	rm -f master_topics.txt

master_topics.txt: topic-state.gz cleanFifo
	mkfifo $@
	python encodeMalletOutput.py > $@ &

doneLoading: master_topics.txt
	python enableMalletFields.py
