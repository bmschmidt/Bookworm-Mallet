nTopics=32
databaseName=streets
all: topic-state.gz

tokenization.mallet:
	#Note: using a crummy regex for now.
	~/mallet-2.0.7/bin/mallet import-file --input ../../files/texts/input.txt --output tokenization.mallet --keep-sequence --remove-stopwords --preserve-case --token-regex  '[\p{L}]{3,}'

topic-state.gz: tokenization.mallet
	~/mallet-2.0.7/bin/mallet train-topics --input tokenization.mallet --num-topics $(nTopics) --output-state topic-state.gz --output-topic-keys keys.txt --output-doc-topics compostion.txt --optimize-interval 20 --num-threads 2

newBookcounts.txt: topic-state.gz
	rm -f newBookcounts.txt
	mkfifo newBookcounts.txt
	python encodeMalletOutput.py > newBookcounts.txt &

database: newBookcounts.txt
	mysql $(databaseName) < loadWords.sql
	touch database
