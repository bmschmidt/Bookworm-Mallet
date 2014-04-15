from tokenizer import *
import gzip
Dictionary = readDictionaryFile("../../")
IDfile = readIDfile("../../")

MalletIDs = dict()

for line in open("compostion.txt"):
    m = line.split("\t")
    try:
        MalletIDs[m[0]] = m[1]
    except IndexError:
        pass

input = gzip.open("topic-state.gz")

thisDoc = -1
counts = dict()
input.readline()
input.readline()
input.readline()

def printOutBook(counts):
    for type in counts.keys():
        for topic in counts[type].keys():
            try:
                #Two layers of lookups for the bookids.
                try:
                    malletID = MalletIDs[doc]
                except KeyError:
                    print "no id for " + doc
                try:
                    bookid = IDfile[MalletIDs[doc]]
                except:
                    print "no bookid for " + MalletIDs[doc]
                wordid = Dictionary[type]
                topic = topic
                count = str(counts[type][topic])
                #This is where it actually gets printed out.
                print "\t".join([bookid,wordid,topic,count])
            except KeyError:
                print "no match for '" + type + "' " + topic

for line in input:
    line = line.rstrip("\n")
    lookups = dict()
    line = line.split(" ")
    doc = line[0]
    type = line[4]
    topic = line[5]

    if doc != thisDoc:
        if MalletIDs[doc] in IDfile:
            printOutBook(counts)
        counts = dict()
        
    try:
        counts[type][topic] += 1
    except KeyError:
        try:
            counts[type][topic] = 1
        except KeyError:
            counts[type] = dict()
            counts[type][topic] = 1

#And once for the last document
try:
    printOutBook(counts)
except:
    #It seems to work fine with the blank last line, but just in case.
    pass
    
