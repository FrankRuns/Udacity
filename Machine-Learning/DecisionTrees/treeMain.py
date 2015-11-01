#!/usr/bin/python

""" lecture and example code for decision tree unit """

import sys
from class_tree_vis import prettyPicture, output_image
from prep_tree_terrain_data import makeTerrainData

import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
from classifyDT import classify

features_train, labels_train, features_test, labels_test = makeTerrainData()

### the classify() function in classifyDT is where the magic
### happens--it's your job to fill this in!
clf = classify(features_train, labels_train)

from sklearn import metrics

pred = clf.predict(features_test)

acc = metrics.accuracy_score(labels_test, pred)

### draw the decision boundary with the text points overlaid
prettyPicture(clf, features_test, labels_test)
output_image("test.png", "png", open("test.png", "rb").read())

### print accuracy score
print(acc)