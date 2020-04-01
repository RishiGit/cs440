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
        last_tag = '<s>'

        for (word, tag) in line:
            myval3.append(tag)
            myval1[tag]['total'] += 1
            myval1[last_tag][tag] += 1
            word = word.lower()
            final_return.append(word)
            myval2[word][tag] += 1
            last_tag = tag

    return list(set(myval3)), my_val4, myval1, myval2, list(set(final_return))

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

    for words in dictionary:
        dictionary.get(words).sort(key=lambda x:x[1])

    myRank.sort(key=lambda x:x[1])
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

    for words in dictionary:
        dictionary.get(words).sort(key=lambda x:x[1])

    myRank.sort(key=lambda x:x[1])
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
    final_return = []
    firstChance = Counter()
    changeChance = Counter()
    startChance = Counter()
    myval1 = Counter()
    myval2 = Counter()
    myval3 = Counter()
    myval4 = Counter()
    myval5 = Counter()
    myval6 = Counter()
    first_holder = []

    for line in train:
        tag_at_start = line[0][1]
        myval3[tag_at_start] += 1

        for const in range(len(line)):
            curr_myval2 = line[const]
            word = curr_myval2[0]
            tag = curr_myval2[1]

            if const + 1 < len(line) - 1:
                next2 = line[const + 1]
                tagger = next2[1]
                myval4[(tag, tagger)] += 1

            myval6[word] += 1
            myval5[tag] += 1
            myval2[(word, tag)] += 1

    k = 0.000001

    for tag in myval5:
        for last_tag in myval5:
            changeChance[(tag, last_tag)] = math.log((myval4[(last_tag, tag)] + k) / (myval5[last_tag] + k * len(myval5)))

        startChance[tag] = math.log((myval3[tag] + k) / (k * len(myval5) + sum(myval3.values())))

    for word in myval6:
        if myval6[word] == 1:
            first_holder.append(word)

    for tag in myval5:
        for word in first_holder:
            myval1[tag] += myval2[(word, tag)]

        firstChance[tag] = (myval1[tag] + k) / (k * len(myval5) + len(first_holder))
        
    for line in test:
        final_ans = []
        way = []
        analyze = {}
        algo = {}
        upperBound = Counter()
        T = len(line) - 1

        for tag in myval5: 
            analyze[(tag, 0)] = 0                               
            determinant = k * firstChance[tag]   
            algo[(tag, 0)] = math.log((myval2[(line[0], tag)] + determinant) / (myval5[tag] + determinant * len(myval6))) + startChance[tag]

        for val in range(len(line)):
            if val == 0:
                continue

            for tag in myval5:
                highChance = {}
                determinant = k * firstChance[tag]   

                for last_tag in myval5:                                                                            
                    highChance[last_tag] = math.log((myval2[(line[val], tag)] + determinant) / (myval5[tag] + determinant * len(myval6))) + changeChance[(tag, last_tag)] + algo[(last_tag, val-1)] 

                analyze[(tag, val)] = (max(highChance, key = highChance.get), val-1)
                algo[(tag, val)] = max(highChance.values())

        for tag in myval5:
            upperBound[(tag, T)] = algo[(tag, T)]
        daWay = max(upperBound, key = upperBound.get)

        while daWay != 0:
            way.append(daWay[0])
            daWay = analyze[daWay]
        way.reverse()

        for const in range(len(line)):
            final_ans.append((line[const], way[const]))

        final_return.append(final_ans)
    return final_return







