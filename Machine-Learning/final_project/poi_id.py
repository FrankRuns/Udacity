#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi', 'salary',
						 'to_messages',
						 'deferral_payments',
						 'total_payments',
						 'exercised_stock_options',
						 'bonus',
						 'restricted_stock',
						 'shared_receipt_with_poi',
						 'restricted_stock_deferred',
						 'total_stock_value',
						 'expenses',
						 'loan_advances',
						 'from_messages',
						 'other',
						 'from_this_person_to_poi',
						 'director_fees',
						 'deferred_income',
						 'long_term_incentive',
						 'from_poi_to_this_person'] # You will need to use more features

# Based on k-best...
# to_message, shared_receipt_with_poi, loan_advances, from_poi_to_this_person

for key, val in data_dict.iteritems():
	val['m_ratio'] = val['shared_receipt_with_poi'] / val['from_poi_to_this_person']

def dict_to_list(key,normalizer):
    new_list=[]

    for i in data_dict:
        if data_dict[i][key]=="NaN" or data_dict[i][normalizer]=="NaN":
            new_list.append(0.)
        elif data_dict[i][key]>=0:
            new_list.append(float(data_dict[i][key])/float(data_dict[i][normalizer]))
    return new_list

### create two lists of new features
em_ratio=dict_to_list("to_messages","from_messages")

### insert new features into data_dict
count=0
for i in data_dict:
    data_dict[i]["em_ratio"]=em_ratio[count]
    count +=1

features_list = ['poi', 'shared_receipt_with_poi',
						'em_ratio',
						'bonus']

### Load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r") )

### Task 2: Remove outliers
### Immediately remove the observation for TOTAL
del data_dict['TOTAL']
del data_dict['BLACHMAN JEREMY M']
del data_dict['FREVERT MARK A']
del data_dict['LAY KENNETH L']
### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)






selection = SelectKBest(k=1)

from sklearn.feature_selection import SelectKBest
x_new = SelectKBest(k='all').fit_transform(features_train, labels_train)
x_new = SelectKBest(k='all')
x_new.fit_transform(features_train, labels_train)
x_new.scores_

from sklearn.pipeline import Pipeline, FeatureUnion
combined_features = FeatureUnion([("univ_select", selection)])

X_features = combined_features.fit(features_train, labels_train).transform(features_train)

clf = GaussianNB()

from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=100)
rfc = rfc.fit(features_train, labels_train)

pipeline = Pipeline([("features", combined_features), ("nb", clf)])

param_grid = dict(features__univ_select__k=[1, 2, 3, 4])

from sklearn.grid_search import GridSearchCV
grid_search = GridSearchCV(pipeline, param_grid=param_grid, verbose=10)

grid_search.fit(features_train, labels_train)
preds = grid_search.predict(features_test)

clf = clf.fit(features_train, labels_train)

preds = clf.predict(features_test)
preds = rfc.predict(features_test)

from sklearn import metrics
accuracy = metrics.accuracy_score(labels_test, preds)
print(accuracy)

from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score
cm = confusion_matrix(labels_test, preds)
ps = precision_score(labels_test, preds)
rs = recall_score(labels_test, preds)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)