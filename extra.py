import numpy
from collections import defaultdict 
from collections import Counter
import math

def element(x):
    return x[1]

def extra(train,test):
    '''
    TODO: implement improved viterbi algorithm for extra credits.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
            test data (list of sentences, no tags on the words)
            E.g  [[word1,word2,...][word1,word2,...]]
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''
        tagger = {}
    myTag = {}
    myRank = []
    dictionary = {}
    final_return = []

    for myWord in train:

        for the_word in myWord:

           if the_word[1] in myTag:
                myTag[the_word[1]] += 1                
           elif the_word[1] not in myTag:
                myTag[the_word[1]] = 1

           if the_word in tagger:
                tagger[the_word] += 1
           elif the_word not in tagger:
                tagger[the_word] = 1

    for tag in tagger:

        if tag[0] in dictionary:
           dictionary[tag[0]].append((tag[1], tagger.get(tag)))
        elif tag[0] not in dictionary:
           dictionary[tag[0]] = []
           dictionary[tag[0]].append((tag[1], tagger.get(tag)))

    for myval2 in myTag:
        myRank.append((myval2, myTag.get(myval2)))

    myRank.sort(key=element)

    for words in dictionary:
        dictionary.get(words).sort(key=element)

    for myWord in test:

        holder = []

        for word in myWord:

            if word in dictionary:
                final_tag = dictionary.get(word)[len(dictionary.get(word))-1][0]
                holder.append((word, final_tag))
            elif word not in dictionary:
                final_tag = myRank[len(myRank)-1][0]
                holder.append((word, final_tag))

        final_return.append(holder)

    return final_return