def classify(features_train, labels_train):   
    ### import the sklearn module for GaussianNB
    ### create classifier
    ### fit the classifier on the training features and labels
    ### return the fit classifier
    
        
    ### your code goes here!
    
    from sklearn.svm import SVC
    
    clf = SVC(kernel='rbf', gamma=1000, C=1)
    # clf = SVC(kernel='rbf', gamma=1000, C=100)
    # clf = SVC(kernel="linear")
    clf.fit(features_train, labels_train)
    
    return clf