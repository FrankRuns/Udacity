#!/usr/bin/python

import sys
import pickle
sys.path.append("../final_project/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### the first feature must be "poi".
features_list = ['poi', 'exercised_stock_options', 'total_stock_value', 'bonus']

### load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
del data_dict['TOTAL']

### Task 3: Create new feature(s)
### leverage pandas for this step
import pandas as pd
import numpy as np

pdata = pd.DataFrame.from_dict(data_dict, orient='index')

# pdata.loc['BELFER ROBERT']
pdata.loc['BELFER ROBERT', 'expenses'] = 3285.0
pdata.loc['BELFER ROBERT', 'deferral_payments'] = 0.0
pdata.loc['BELFER ROBERT', 'deferred_income'] = -102500.0
pdata.loc['BELFER ROBERT', 'director_fees'] = 102500.0
pdata.loc['BELFER ROBERT', 'total_payments'] = 3285.0
# pdata.loc['BHATNAGAR SANJAY']
pdata.loc['BHATNAGAR SANJAY', 'expenses'] = 137864.0
pdata.loc['BHATNAGAR SANJAY', 'total_payments'] = 137864.0
pdata.loc['BHATNAGAR SANJAY', 'other'] = 0.0
pdata.loc['BHATNAGAR SANJAY', 'director_fees'] = 0.0

### create NaN metadata features
pdata = pdata.replace('NaN', np.nan, regex=True)
pdata['sal_navalue_count'] = pdata[['salary', 'deferral_payments', 
								    'long_term_incentive', 'total_payments',
								    'bonus', 'expenses', 'loan_advances',
								    'other', 'director_fees', 'deferred_income']].isnull().sum(axis=1)

### remove text field and convert NaNs to 0
pdata = pdata.drop('email_address', 1)
pdata = pdata.replace(np.nan, 0, regex=True)

### create other features
pdata['em_ratio'] = (pdata['shared_receipt_with_poi'] + pdata['from_this_person_to_poi'] + pdata['from_poi_to_this_person'] ) / (pdata['to_messages'] + pdata['from_messages'])
pdata['from_ratio'] = pdata['from_this_person_to_poi'] / pdata['from_messages']
pdata['to_ratio'] = (pdata['from_poi_to_this_person'] + pdata['shared_receipt_with_poi']) / pdata['to_messages']

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
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

pipe_knn = Pipeline([('scl', StandardScaler()),
                     ('clf', KNeighborsClassifier(weights = 'uniform',
                                                  n_neighbors = 5,
                                                  p = 1 ))])

clf = pipe_knn.fit(features, labels)
print(clf)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)