# classify.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018
# Extended by Daniel Gonzales (dsgonza2@illinois.edu) on 3/11/2020

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.

train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
            This can be thought of as a list of 7500 vectors that are each
            3072 dimensional.  We have 3072 dimensions because there are
            each image is 32x32 and we have 3 color channels.
            So 32*32*3 = 3072. RGB values have been scaled to range 0-1.

train_labels - List of labels corresponding with images in train_set
example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
         and X1 is a picture of a dog and X2 is a picture of an airplane.
         Then train_labels := [1,0] because X1 contains a picture of an animal
         and X2 contains no animals in the picture.

dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
          It is the same format as train_set
"""
### Used help from Piazza post @1315 for loop structure for LR

import math
import numpy

def trainPerceptron(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained weight and bias parameters 
    W = numpy.zeros(train_set.shape[1])
    b = 0
    for i in range (max_iter): #total amount of times to iterate through training set 
        for j in range (len(train_set)): #In each epoch, go through and update w, b
            if (numpy.dot(train_set[j], W)+b) > 0:
                W += (-1 + train_labels[j]) * learning_rate * train_set[j]
                b += (-1 + train_labels[j]) * learning_rate
            else:
                W += train_labels[j] * learning_rate * train_set[j]
                b += train_labels[j] * learning_rate
    return W, b

def classifyPerceptron(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train perceptron model and return predicted labels of development set
    myReturn = []
    W, b = trainPerceptron(train_set, train_labels, learning_rate, max_iter)
    for i in (numpy.dot(dev_set, W) + b):
        if i > 0:
            myReturn.append(1)
        else:
            myReturn.append(0)
    return myReturn

def sigmoid(x):
    # TODO: Write your code here
    # return output of sigmoid function given input x
    s = 1/(1+numpy.exp(-x))
    return s

def trainLR(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained weight and bias parameters 
    W = numpy.zeros(train_set.shape[1])
    b = 0
    for i in range (max_iter): #total amount of times to iterate through training set 
        weight_gradient = 0
        bias_gradient = 0
        for j in range (len(train_set)): #In each epoch, go through and update w, b
            weight_gradient += numpy.dot(sigmoid(numpy.dot(train_set[j], W)+b) - train_labels[j], train_set[j]) 
            bias_gradient += sigmoid(numpy.dot(train_set[j], W)+b) - train_labels[j]
        W -= learning_rate/len(train_set) * weight_gradient
        b -= learning_rate/len(train_set) * bias_gradient 
    return W, b

def classifyLR(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train LR model and return predicted labels of development set
    myReturn = []
    W, b = trainLR(train_set, train_labels, learning_rate, max_iter)
    for i in sigmoid(numpy.dot(dev_set, W) + b):
        if i > 0.5:
            myReturn.append(1)
        else:
            myReturn.append(0)
    return myReturn

def classifyEC(train_set, train_labels, dev_set, k):
    # Write your code here if you would like to attempt the extra credit
    myReturn = []
    W, b = trainLR(train_set, train_labels, 0.01, 190)
    for i in sigmoid(numpy.dot(dev_set, W) + b):
        if i > 0.5:
            myReturn.append(1)
        else:
            myReturn.append(0)
    return myReturn
