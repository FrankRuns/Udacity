#!/usr/bin/python

""" 
    this is the code to accompany the Lesson 2 (SVM) mini-project

    use an SVM to identify emails from the Enron corpus by their authors
    
    Sara has label 0
    Chris has label 1

"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################
### your code goes here ###

from sklearn.svm import SVC

# features_train = features_train[:len(features_train)/100] 
# labels_train = labels_train[:len(labels_train)/100] 

t0 = time()
clf = SVC(kernel='rbf', C=10000)
clf.fit(features_train, labels_train)
print "training time:", round(time()-t0, 3), "s"

pred = clf.predict(features_test)

# How many test cases are predicted as Chris?
chris = sum(pred)
print(chris)

# pred_10 = clf.predict(features_test[10])
# pred_26 = clf.predict(features_test[26])
# pred_50 = clf.predict(features_test[50])
# print(pred_10, pred_26, pred_50)

from sklearn import metrics

accuracy = metrics.accuracy_score(labels_test, pred)
print(accuracy)

#########################################################


