#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi', 'total_payments', 'exercised_stock_options', 
                 'bonus', 'expenses', 'poi_mail', 's_ratio'] # You will need to use more features
print('features: ', features_list)

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
del data_dict['TOTAL']

### Task 3: Create new feature(s)
import pandas as pd
import numpy as np
pdata = pd.DataFrame.from_dict(data_dict, orient='index')
pdata = pdata.replace("NaN", 0, regex=True)
# I assume poi's have relatively greater email exchange with other pois
# Create percentage of poi-related email to total emails for each individual
pdata['poi_mail'] = ( pdata['from_poi_to_this_person'] + pdata['from_this_person_to_poi'] + pdata['shared_receipt_with_poi'] ) / ( pdata['to_messages'] + pdata['from_messages'] )
# I assume that people receiving relatively greater incentive pay are receiving it for a reason
# Create percentage of incentive pay to salary
pdata['s_ratio'] = ( pdata['bonus'] ) / pdata['salary']
# Need to replace Nan and inf values
# Need to turn poi variable back into character from integer
pdata = pdata.replace(np.nan, 0, regex=True)
pdata = pdata.replace(np.inf, 0, regex=True)
pdata = pdata.replace(-np.inf, 0, regex=True)
pdict = pdata.T.to_dict()

print('Sample element of data', pdict.itervalues().next())

### Store to my_dataset for easy export below.
my_dataset = pdict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Scale the feature set
from sklearn.preprocessing import MinMaxScaler

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
# from sklearn.naive_bayes import GaussianNB
# clf = GaussianNB()

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.1, random_state=42)

print('Test set created...')
print('Building random forest...')

from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV

rfc = RandomForestClassifier(n_estimators=100)
# param_grid = {"model__max_depth": [3, None],
#               "model__max_features": [1, 3, 5],
#               "model__min_samples_split": [1, 3, 10],
#               "model__min_samples_leaf": [1, 3, 10],
#               "model__bootstrap": [True, False],
#               "model__criterion": ["gini", "entropy"]}

scaler = MinMaxScaler()
pipeline_object = Pipeline([('scaler', scaler),('model', rfc)])
# clf = GridSearchCV(pipeline_object, param_grid, scoring = 'accuracy')

clf = pipeline_object.fit(features_train, labels_train)
print('This is the final classifier...')

from sklearn import datasets, linear_model, cross_validation, grid_search
kf_total = cross_validation.KFold(len(features), n_folds=10, indices=True, shuffle=True, random_state=4)
print([clf.fit(features_train, labels_train).score(features_test,labels_test) for train_indices, test_indices in kf_total])

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)