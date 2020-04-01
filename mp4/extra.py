import numpy
from collections import defaultdict 
from collections import Counter
import math

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

    k = 0.0000001

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
