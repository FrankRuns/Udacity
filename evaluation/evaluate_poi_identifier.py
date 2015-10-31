#!/usr/bin/python


"""
    starter code for the evaluation mini-project
    start by copying your trained/tested POI identifier from
    that you built in the validation mini-project

    the second step toward building your POI identifier!

    start by loading/formatting the data

"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### add more features to features_list!
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)


### your code goes here 

from sklearn import tree
from sklearn import cross_validation
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score

features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(features, labels, test_size = 0.3, random_state = 42)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(features_train, labels_train)

preds = clf.predict(features_test)

acc = accuracy_score(labels_test, preds)

cm = confusion_matrix(labels_test, preds)

ps = precision_score(labels_test, preds)

rs = recall_score(labels_test, preds)

predictions = [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1] 
true_labels = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0]