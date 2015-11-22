#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
# features_list = ['poi', 'bonus', 'salary', 'total_stock_value', 'deferred_income',
#                  'short_gain', 'total_total', 'sal_ratio',
#                  'shared_receipt_with_poi', 'restricted_stock', 'em_ratio', 'other'] # You will need to use more features


# features_list = ['poi', 'bonus', 'salary', 'exercised_stock_options',
#                  'short_gain', 'total_total', 'sal_ratio', 'from_ratio',
#                  'shared_receipt_with_poi', 'restricted_stock', 'em_ratio', 'other'] 
# 0.8695, 0.5682, 0.0895, 0.15 

# features_list = ['poi', 'salary', 'bonus', 'total_stock_value', 'exercised_stock_options',
#                  'from_ratio', 'short_gain', 'deferred_income', 'total_total']
# Random Forest, Accuracy: 0.87147	Precision: 0.57725	Recall: 0.13450	F1: 0.21

# features_list = ['poi', 'salary', 'bonus', 'total_stock_value', 'exercised_stock_options',
#                  'from_ratio', 'short_gain', 'deferred_income', 'total_total', 'sal_ratio']
# Random Forest, Accuracy: 0.87247	Precision: 0.59732	Recall: 0.13350	F1: 0.21

# BEST YET.
# features_list = ['poi', 'salary','shared_receipt_with_poi','deferred_income','bonusexpsal',
#  'em_ratio','total_navalue_count','total_total', 'sal_navalue_count','fromto_ratio']

features_list = ['poi', 'salary','shared_receipt_with_poi','deferred_income','bonusexpsal',
 'em_ratio', 'total_navalue_count','total_total', 'sal_navalue_count', 'fromto_ratio']

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

pdata = pdata.replace('NaN', np.nan, regex=True)

temp = []
for el in pdata['email_address'].values:
    if type(el) == float:
        temp.append(False)
    else:
        temp.append(True)
pdata['has_email_data'] = temp
pdata['total_navalue_count'] = pdata.isnull().sum(axis=1)
pdata['sal_navalue_count'] = pdata[['salary', 'deferral_payments', 'long_term_incentive', 'total_payments', 'bonus', 'expenses', 'loan_advances', 'other', 'director_fees', 'deferred_income']].isnull().sum(axis=1)

pdata = pdata.drop('email_address', 1)

pdata = pdata.replace(np.nan, 0, regex=True)

pdata = pdata[pdata.index != 'SKILLING JEFFREY K']
pdata = pdata[pdata.index != 'BELFER ROBERT']
pdata = pdata[pdata.index != 'BHATNAGAR SANJAY']

pdata['short_gain'] = pdata['exercised_stock_options'] - pdata['long_term_incentive']
pdata['sal_ratio'] = pdata['salary'] / pdata['total_payments']
pdata['nonsal_ratio'] = (pdata['bonus'] + pdata['long_term_incentive'] + pdata['expenses']) / pdata['total_payments']
pdata['stock_ratio'] = pdata['restricted_stock'] / pdata['total_stock_value']
pdata['em_ratio'] = (pdata['shared_receipt_with_poi'] + pdata['from_this_person_to_poi'] + pdata['from_poi_to_this_person'] ) / (pdata['to_messages'] + pdata['from_messages'])
pdata['total_total'] = pdata['total_payments'] + pdata['total_stock_value']
pdata['from_ratio'] = pdata['from_this_person_to_poi'] / pdata['from_messages']
pdata['sent_ratio'] = (pdata['from_poi_to_this_person'] + pdata['shared_receipt_with_poi']) / pdata['to_messages']
pdata['fromto_ratio'] = pdata['from_ratio'] + pdata['sent_ratio']
pdata['bonusexpsal'] = pdata['bonus'] + pdata['expenses'] + pdata['salary']

pdata = pdata.replace(np.nan, 0, regex=True)
pdata = pdata.replace(np.inf, 0, regex=True)
pdata = pdata.replace(-np.inf, 0, regex=True)
pdict = pdata.T.to_dict()

### Store to my_dataset for easy export below.
my_dataset = pdict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

### Scale the feature set

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
# from sklearn.cross_validation import train_test_split
# features_train, features_test, labels_train, labels_test = \
#     train_test_split(features, labels, test_size=0.3, random_state=42)

# rfc = RandomForestClassifier(n_estimators=100,
# 							criterion='entropy',
# 							min_samples_split=25)
# NOTE: Higher min_samples_split decreases accuracy.. but your
# false positive rate falls sharply..

# param_grid = {"model__max_depth": [3, None],
#               "model__max_features": [1, 3, 5],
#               "model__min_samples_split": [1, 3, 10],
#               "model__min_samples_leaf": [1, 3, 10],
#               "model__bootstrap": [True, False],
#               "model__criterion": ["gini", "entropy"]}

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

# pipe_svc = Pipeline([('scl', StandardScaler()),
#                      ('pca', PCA(n_components=2)),
#                      ('clf', SVC(random_state=1,
#                      			 kernel='linear',
#                      			 C=1))])

# pipe_rfc = Pipeline([('scl', MinMaxScaler()),
#                      ('pca', PCA(n_components=2)),
#                      ('clf', RandomForestClassifier(random_state=1,
#                      			 n_estimators=100,
#                      			 criterion='gini',
#                      			 min_samples_split=20))])

# pipe_rfc = Pipeline([('scl', StandardScaler()),
#                      ('pca', PCA(n_components=2)),
#                      ('clf', AdaBoostClassifier(RandomForestClassifier(
#                                                 n_estimators=100,
#                                                 criterion='gini',
#                                                 min_samples_split=40,
#                                                 random_state=1)))])

# pipe_dtc = Pipeline([('scl', MinMaxScaler()),
#                      ('pca', PCA(n_components=2)),
#                      ('clf', DecisionTreeClassifier(criterion='gini',
#                      								min_samples_split=10,
#                      								random_state=1))])
# features_list = ['poi', 'salary', 'total_payments', 'exercised_stock_options',
# 				 'bonus','total_stock_value', 'deferred_income', 'from_ratio',
#  				 'sal_ratio', 'total_total', 'short_gain']

# pipe_dtc = Pipeline([('scl', MinMaxScaler()),
#                      ('pca', PCA(n_components=2)),
#                      ('clf', DecisionTreeClassifier(criterion='entropy',
#                                                   min_samples_split=20,
#                                                   random_state=1))])

# pipe_dtc = Pipeline([('scl', MinMaxScaler()),
#                      ('pca', PCA(n_components=2, whiten=True)),
#                      ('clf', DecisionTreeClassifier(criterion='gini',
#                                                   min_samples_split=60,
#                                                   random_state=42))])

pipe_dtc = Pipeline([('scl', MinMaxScaler()),
                     ('pca', PCA(n_components=2)),
                     ('clf', DecisionTreeClassifier(random_state=42))])

clf = pipe_dtc.fit(features, labels)

print(clf)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)