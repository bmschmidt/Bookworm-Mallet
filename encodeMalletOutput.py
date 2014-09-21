import gzip

input = gzip.open("topic-state.gz")

thisDoc = -1
counts = dict()

#The first three lines aren't useful for us.
input.readline()
input.readline()
input.readline()


"""
To save space, we write the long version to stdout, but the compact (just doc-topic assignments) 
version to disk in the file "topicAssignments.txt"
"""

topicAssignments = open("topicAssignments.txt","w")

def printOutBook(counts,thisDoc):
    topics = dict()
    for token in counts.keys():
        for topic in counts[token].keys():
            try:
                topics[topic] += counts[token][topic]
            except KeyError:
                topics[topic] = counts[token][topic]
            print "\t".join([thisDoc,token,topic,str(counts[token][topic])])
    for topic in topics.keys():
        topicAssignments.write("\t".join([thisDoc,topic,str(topics[topic])]) + "\n")


for line in input:
    line = line.rstrip("\n")
    lookups = dict()
    line = line.split(" ")
    doc = line[0]
    token = line[4]
    topic = line[5]

    if doc != thisDoc:
        printOutBook(counts,thisDoc)

        thisDoc = doc
        counts = dict()
        
    try:
        counts[token][topic] += 1
    except KeyError:
        try:
            counts[token][topic] = 1
        except KeyError:
            counts[token] = dict()
            counts[token][topic] = 1

#And once for the last document
try:
    printOutBook(counts,thisDoc)
except:
    #It seems to work fine with the blank last line, but just in case.
    pass
    
