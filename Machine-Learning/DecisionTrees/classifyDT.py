def classify(features_train, labels_train):
    
    ### your code goes here--should return a trained decision tree classifer

    from sklearn import tree
    clf = tree.DecisionTreeClassifier(min_samples_split=2)
    clf = clf.fit(features_train, labels_train)
    
    return clf