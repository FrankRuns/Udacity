#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### the first feature must be "poi".
features_list = ['poi', 'salary','shared_receipt_with_poi',
                        'deferred_income','bonusexpsal',
                        'em_ratio', 'total_navalue_count',
                        'total_total', 'sal_navalue_count',
                        'fromto_ratio']

### load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
del data_dict['TOTAL']
del data_dict['SKILLING JEFFREY K']
del data_dict['BELFER ROBERT']
del data_dict['BHATNAGAR SANJAY']

### Task 3: Create new feature(s)
### leverage pandas for this step
import pandas as pd
import numpy as np

pdata = pd.DataFrame.from_dict(data_dict, orient='index')

### create NaN metadata features
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

### remove text field and convert NaNs to 0
pdata = pdata.drop('email_address', 1)
pdata = pdata.replace(np.nan, 0, regex=True)

### create other features
pdata['sal_ratio'] = pdata['salary'] / pdata['total_payments']
pdata['nonsal_ratio'] = (pdata['bonus'] + pdata['long_term_incentive'] + pdata['expenses']) / pdata['total_payments']
pdata['em_ratio'] = (pdata['shared_receipt_with_poi'] + pdata['from_this_person_to_poi'] + pdata['from_poi_to_this_person'] ) / (pdata['to_messages'] + pdata['from_messages'])
pdata['total_total'] = pdata['total_payments'] + pdata['total_stock_value']
pdata['from_ratio'] = pdata['from_this_person_to_poi'] / pdata['from_messages']
pdata['sent_ratio'] = (pdata['from_poi_to_this_person'] + pdata['shared_receipt_with_poi']) / pdata['to_messages']
pdata['fromto_ratio'] = pdata['from_ratio'] + pdata['sent_ratio']
pdata['bonusexpsal'] = pdata['bonus'] + pdata['expenses'] + pdata['salary']

### convert back to dictionary
pdata = pdata.replace(np.nan, 0, regex=True)
pdata = pdata.replace(np.inf, 0, regex=True)
pdata = pdata.replace(-np.inf, 0, regex=True)
pdict = pdata.T.to_dict()

### store to my_dataset for easy export below.
my_dataset = pdict

### extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Scale the feature set
### features are scaled in the Pipeline

### Task 4: Try a varity of classifiers
### please name your classifier clf for easy export below.
### note that if you want to do PCA or other multi-stage operations,
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

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier

pipe_dtc = Pipeline([('scl', MinMaxScaler()),
                     ('pca', PCA(n_components=2, whiten=True)),
                     ('clf', DecisionTreeClassifier(criterion='gini',
                                                  min_samples_split=60,
                                                  random_state=42))])

clf = pipe_dtc.fit(features, labels)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)