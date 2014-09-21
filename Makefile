nTopics=64


files.mallet: bookwormStopwords.txt
	~/mallet-2.0.7/bin/mallet import-file --input input.txt --output files.mallet --keep-sequence --remove-stopwords --token-regex "[A-Za-z']+" --extra-stopwords bookwormStopwords.txt

topic-state.gz: files.mallet
	~/mallet-2.0.7/bin/mallet train-topics --input files.mallet --num-topics $(nTopics) --output-state topic-state.gz --output-topic-keys keys.txt --output-doc-topics compostion.txt --optimize-interval 20 --num-threads 6




