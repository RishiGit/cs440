"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import numpy
from collections import defaultdict 
from collections import Counter
import math

'''<--------------------------- HELPER FUCNTIONS BELOW------------------------------> '''

def analyze(myval3, line, myPercent, myDistant):
    final_return = []
    traversed = []
    rows = len(myPercent) - 1
    myRows = myPercent[rows]
    cols = numpy.argmax(myRows)
    myCounter = 0

    if len(line) == 1:
        return [(line[0], myval3[cols])]

    while myCounter < len(line):
        traversed.insert(0, (rows, cols))
        (rows, cols) = myDistant[rows][cols]
        myCounter = myCounter + 1

    for (word, tag) in traversed:
        word = line[word]
        tag = myval3[tag]
        final_return.append((word, tag))

    return final_return

def update_dict(train):
    myval3 = []
    my_val4 = 0
    myval1 = defaultdict(lambda: defaultdict(int))
    myval2 = defaultdict(lambda: defaultdict(int))
    final_return = []

    for line in train:
        my_val4 = my_val4 + 1
        last_tag = 'f to pay respects'

        for (word, tag) in line:
            myval3.append(tag)
            myval1[tag]['total'] += 1
            myval1[last_tag][tag] += 1
            word = word.lower()
            final_return.append(word)
            myval2[word][tag] += 1
            last_tag = tag

    return list(set(myval3)), my_val4, myval1, myval2, list(set(final_return))

def element(x):
    return x[1]

'''<--------------------------- HELPER FUCNTIONS ABOVE ------------------------------> '''

def baseline(train, test):
    '''
    TODO: implement the baseline algorithm. This function has time out limitation of 1 minute.
    input:  training data (list of sentences, with myval2 on the words)
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
            test data (list of sentences, no myval2 on the words)
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

def viterbi_p1(train, test):
    '''
    TODO: implement the simple Viterbi algorithm. This function has time out limitation for 3 mins.
    input:  training data (list of sentences, with myval2 on the words)
            E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no myval2 on the words)
            E.g [[word1,word2...]]
    output: list of sentences with myval2 on the words
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''
    final_return = []
    laplace_smoothing = 0.1
    myval3, my_val4, myval1, myval2, lang = update_dict(train)
    langLength = len(lang)
    myLength = len(myval3)
    myval3.sort()

    for line in test:

        if len(line) == 0:
            final_return.append([])
            continue

        myPercent = [[0 for col in range(myLength)]
                    for row in range(len(line))]
        myDistant = [[(0, 0) for col in range(myLength)]
                    for row in range(len(line))]

        for i in range(0, len(line)):

            word = line[i].lower()

            for j in range(0, myLength):
                tag = myval3[j]

                if i == 0:
                    changeChance = (math.log(myval1['f to pay respects'][tag] + laplace_smoothing)- math.log(my_val4 + (laplace_smoothing * myLength)))
                else:
                    upperCoord = (0, 0)
                    upperBound = math.inf * (-1) 

                    for k in range(0, myLength):
                        last_tag = myval3[k]
                        lastChance = myPercent[i-1][k]
                        upperTransition = (math.log(myval1[last_tag][tag] + laplace_smoothing) - math.log(myval1[last_tag]['total'] + (k*myLength)))
                        upperTransition += lastChance

                        if upperBound < upperTransition:
                            upperCoord = (i-1, k)
                            upperBound = upperTransition

                    myDistant[i][j] = upperCoord
                    changeChance = upperBound

                percentChance = (math.log(myval2[word][tag] + laplace_smoothing) -math.log(myval1[tag]['total'] + (laplace_smoothing*(langLength+1))))
                myPercent[i][j] = changeChance + percentChance

        answer = analyze(myval3, line, myPercent, myDistant)
        final_return.append(answer)

    return final_return


def viterbi_p2(train, test):
    '''
    TODO: implement the optimized Viterbi algorithm. This function has time out limitation for 3 mins.
    input:  training data (list of sentences, with myval2 on the words)
            E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no myval2 on the words)
            E.g [[word1,word2...]]
    output: list of sentences with myval2 on the words
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






