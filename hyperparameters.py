def get_model_and_params(model_name):

    """
    Convenience method to keep all of the tried parameters in a single place
    """

    #lr: logistic regression
    if model_name == 'lr':

        model = sk.linear_model.LogisticRegression(multi_class='auto', max_iter=4000)
        params = [
                #1/C: penalization parameter, low=stronger regularization,
                #high=less regularization (overfitting risk)
                {'C':  [100], 'penalty': ['l2'], 'solver': ['sag']},
                {'C':  [1, 10, 100], 'penalty': ['l2'], 'solver': ['sag', 'saga']},
                {'C':  [1, 10, 100], 'penalty': ['l1'], 'solver': ['saga']},
                {'C':  [1, 10, 100], 'penalty': ['elasticnet'], 'solver': ['saga'], 'l1_ratio': [0.5]}
        ]

    #dt: decision trees
    elif model_name == 'dt':

        model = sk.tree.DecisionTreeClassifier(random_state=0)
        params = {
        'criterion': ['gini', 'entropy'],
        'max_depth': [5,7,9,10],
        'min_samples_split': [2,3,4], #minimum number of leaves required to split an internal node
        'min_samples_leaf': [1,3], #minimum number of leaves required to to be at a leaf node
        'class_weight': [None, 'balanced']
        }

    #rf: random forest
    elif model_name == 'rf':

        model = RandomForestClassifier(random_state=0, n_jobs=-1)
        params = {
            'max_depth': [5,7,9], #maximum number of features random forest considers splitting a node
            'min_samples_leaf': [3,5], #minimum number of leaves required to split an internal node
            'min_samples_split': [2, 4],
            'max_features': [None, 'sqrt', 'log2', 0.2, 0.3],
            'n_estimators': [100,250,500], #number of trees to build
            'class_weight': [None, 'balanced']
        }


    elif model_name == 'nn':
        model = KerasClassifier(build_fn=create_model, verbose=0, epochs=15)
        params = {
            'n_neurons1' : [32, 64, 128],
            'n_neurons2' : [32, 64, 128],
            'batch_size': [128],
            'n_epochs': [10, 15],
            'learning_rate': [0.01, 0.1],
            'dropout_rate' : [0, 0.2]
            }

    else:
        return -1

    return model, params
