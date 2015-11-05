#!/usr/bin/python

from time import time
import matplotlib.pyplot as plt
from prep_terrain_data import makeTerrainData
from class_vis import prettyPicture

features_train, labels_train, features_test, labels_test = makeTerrainData()


### the training data (features_train, labels_train) have both "fast" and "slow" points mixed
### in together--separate them so we can give them different colors in the scatterplot,
### and visually identify them
grade_fast = [features_train[ii][0] for ii in range(0, len(features_train)) if labels_train[ii]==0]
bumpy_fast = [features_train[ii][1] for ii in range(0, len(features_train)) if labels_train[ii]==0]
grade_slow = [features_train[ii][0] for ii in range(0, len(features_train)) if labels_train[ii]==1]
bumpy_slow = [features_train[ii][1] for ii in range(0, len(features_train)) if labels_train[ii]==1]


#### initial visualization
# plt.xlim(0.0, 1.0)
# plt.ylim(0.0, 1.0)
# plt.scatter(bumpy_fast, grade_fast, color = "b", label="fast")
# plt.scatter(grade_slow, bumpy_slow, color = "r", label="slow")
# plt.legend()
# plt.xlabel("bumpiness")
# plt.ylabel("grade")
# plt.show()
#################################################################################


### your code here!  name your classifier object clf if you want the 
### visualization code (prettyPicture) to show you the decision boundary

from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

# clf = AdaBoostClassifier(
#     DecisionTreeClassifier(max_depth=1,min_samples_split=100,random_state=0),
#     algorithm="SAMME",
# 	n_estimators=80,
# 	learning_rate=0.5
# )
# clf = DecisionTreeClassifier(min_samples_split=40)
# clf = RandomForestClassifier(min_samples_split=40, n_estimators=600)
clf = KNeighborsClassifier(n_neighbors=9, 
						   weights='uniform',
						   algorithm='brute',
						   p=1) # p is the distance measure (manhattan or euclidean)

t0 = time()
clf = clf.fit(features_train, labels_train)
print "fitting time:", round(time()-t0, 3), "s"

pred = clf.predict(features_test)

try:
    prettyPicture(clf, features_test, labels_test)
except NameError:
    pass

acc = metrics.accuracy_score(labels_test, pred)

print(acc)