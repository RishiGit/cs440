# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
# Modified by Jaewook Yeom 02/02/2020

"""
This is the main entry point for Part 2 of this MP. You should only modify code
within this file for Part 2 -- the unvalueised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


import numpy as numpy
import math
from collections import Counter





def naiveBayesMixture(train_set, train_labels, dev_set, bigram_lambda,unigram_smoothing_parameter, bigram_smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie valueiew
    example: suppose I had two valueiews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two valueiews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each valueiew that we are testing on
              It follows the same format as train_set

    bigram_lambda - float between 0 and 1

    unigram_smoothing_parameter - Laplace smoothing parameter for unigram model (between 0 and 1)

    bigram_smoothing_parameter - Laplace smoothing parameter for bigram model (between 0 and 1)

    pos_prior - positive prior probability (between 0 and 1)
    """
 


    # TODO: Write your code here
    dev_labels = []
    bigNeg = Counter()
    uniNeg = Counter()
    bigPos = Counter()
    uniPos = Counter()
 
    for value in train_set:
        if(train_labels[train_set.index(value)]==0):
            for word in value:
                uniNeg[word]+=1
        else:
            for word in value:
                uniPos[word]+=1
   
    uninSum = sum(uniNeg.values())
    unipSum = sum(uniPos.values())

    for value in train_set:
        if(train_labels[train_set.index(value)]==0):
            for i in range(len(value)-1):
                word1 = value[i] + value[i+1]
                bigNeg[word1]+=1
        else:
            for i in range(len(value)-1):
                word1 = value[i] + value[i+1]
                bigPos[word1]+=1

    bignSum = sum(bigNeg.values())
    bigpSum = sum(bigPos.values())



    for word in dev_set:
        counterbigneg = 0
        counterunineg = 0
        counterbigpos = 0
        counterunipos = 0

        for instance in word:
            counterunineg += math.log10((unigram_smoothing_parameter + uniNeg[instance])/(unigram_smoothing_parameter*2 + uninSum))
            counterunipos += math.log10((unigram_smoothing_parameter + uniPos[instance])/(unigram_smoothing_parameter*2 + unipSum))

        for i in range(len(word)-1):
            word2 = word[i]+word[i+1]
            counterbigneg += math.log10((bigram_smoothing_parameter + bigNeg[word2])/(bigram_smoothing_parameter*2 + bignSum))
            counterbigpos += math.log10((bigram_smoothing_parameter + bigPos[word2])/(bigram_smoothing_parameter*2 + bigpSum))

        negChance = (1-bigram_lambda)*(math.log10(1-pos_prior)+counterunineg) + (bigram_lambda)*(math.log10(1-pos_prior)+counterbigneg)
        posChance = (1-bigram_lambda)*(math.log10(pos_prior)+counterunipos) + (bigram_lambda)*(math.log10(pos_prior)+counterbigpos)
        
        if(negChance > posChance):
            dev_labels.append(0)
        else:
            dev_labels.append(1)
            
    # return predicted labels of development set (make sure it's a list, not a numpy array or similar)
    return dev_labels

