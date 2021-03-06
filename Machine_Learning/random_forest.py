import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
# from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from generic import *


def get_forest(train_x, train_y, test_x, test_y):
    start_time = time.time()
    best_forest = tune_forest(train_x, train_y)
    print("--- Best Parameter Random Forest Time: %s seconds ---" % (time.time() - start_time))
    print("Best Random Forest Parameters: " + str(best_forest.get_params()))
    print("Training Mean Test Score: " + str(best_forest.score(train_x, train_y)))
    y_hat = best_forest.predict(test_x)
    print("Testing Mean Test Score " + str(accuracy_score(test_y, y_hat)))
    make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=best_forest, clf_name='Random_Forest')
    # top(best_forest, test_x, test_y, extra_rooms=2)
    with open("results.txt", "a") as my_file:
        my_file.write("[Random Forest] Training Mean Test Score: " + str(best_forest.score(train_x, train_y)))
        my_file.write("[Random Forest] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)))

    with open("classification_reports.txt", "a") as my_file:
        my_file.write("---[Random Forest]---")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            target_names=[str(i) for i in best_forest.classes_]))
    # print(classification_report(y_true=test_y, y_pred=y_hat, target_names=[str(i) for i in best_forest.classes_]))
    return best_forest


# Citation:
# https://towardsdatascience.com/hyperparameter-tuning-the-random-forest-in-python-using-scikit-learn-28d2aa77dd74
# http://scikit-learn.org/stable/auto_examples/model_selection/plot_randomized_search.html#sphx-glr-auto-examples-model-selection-plot-randomized-search-py
# https://towardsdatascience.com/random-forest-in-python-24d0893d51c0
def tune_forest(train_features, train_labels, n_fold=10):
    # Number of trees in random forest
    n_estimators = np.arange(10, 510, 10)
    # Number of features to consider at every split
    max_features = ['auto', 'sqrt']
    # Maximum number of levels in tree
    max_depth = np.arange(3, 20, 1)
    # Minimum number of samples required to split a node
    min_samples_split = np.arange(5, 20, 1)
    # Minimum number of samples required at each leaf node
    min_samples_leaf = np.arange(5, 20, 1)

    # random_grid = {
    #    'n_estimators': n_estimators,
    #    'max_features': max_features,
    #    'max_depth': max_depth,
    #    'min_samples_split': min_samples_split,
    #    'min_samples_leaf': min_samples_leaf,
    #    }

    # Step 1: Use the random grid to search for best hyper parameters
    # First create the base model to tune
    rf = RandomForestClassifier(warm_start=False)
    rf_estimate = GridSearchCV(estimator=rf, param_grid={'n_estimators': n_estimators}, cv=n_fold, verbose=2, n_jobs=-1)
    rf_estimate.fit(train_features, train_labels)
    plot_grid_search(rf_estimate.cv_results_, n_estimators, 'n_estimators')

    rf = RandomForestClassifier(warm_start=False)
    rf_max = GridSearchCV(estimator=rf, param_grid={'max_features': max_features}, cv=n_fold, verbose=2, n_jobs=-1)
    rf_max.fit(train_features, train_labels)
    plot_grid_search(rf_max.cv_results_, max_features, 'max_features')

    rf = RandomForestClassifier(warm_start=False)
    rf_distro = GridSearchCV(estimator=rf, param_grid={'max_depth': max_depth}, cv=n_fold, verbose=2, n_jobs=-1)
    rf_distro.fit(train_features, train_labels)
    plot_grid_search(rf_distro.cv_results_, max_depth, 'max_depth')

    rf = RandomForestClassifier(warm_start=False)
    rf_min_split = GridSearchCV(estimator=rf, param_grid={'min_samples_split': min_samples_split},
                                cv=n_fold, verbose=2, n_jobs=-1)
    rf_min_split.fit(train_features, train_labels)
    plot_grid_search(rf_min_split.cv_results_, min_samples_split, 'min_samples_split')

    rf = RandomForestClassifier(warm_start=False)
    rf_min_leaf = GridSearchCV(estimator=rf, param_grid={'min_samples_leaf': min_samples_leaf},
                               cv=n_fold, verbose=2,  n_jobs=-1)
    rf_min_leaf.fit(train_features, train_labels)
    plot_grid_search(rf_min_leaf.cv_results_, min_samples_leaf, 'min_samples_leaf')

    # -----------------LAST STEP!-------------------
    # Random search of parameters, using 3 fold cross validation,
    # search across 100 different combinations, and use all available cores

    # Fit the random search model
    # rf_random.fit(train_features, train_labels)

    # TODO: IF I ADD MORE "Features", by definition I must increase number of estimators!!
    random_forest = RandomForestClassifier(warm_start=False,
                                           n_estimators=rf_estimate.best_params_['n_estimators'],
                                           max_features=rf_max.best_params_['max_features'],
                                           max_depth=rf_distro.best_params_['max_depth'],
                                           min_samples_split=rf_min_split.best_params_['min_samples_split'],
                                           min_samples_leaf=rf_min_leaf.best_params_['min_samples_leaf'])
    random_forest.fit(train_features, train_labels)
    return random_forest


def main():
    # Read Wifi and Blue Tooth Data Set
    blue_x, blue_y = read_data_set('./blue.csv')
    wifi_x, wifi_y = read_data_set('./wifi.csv')

    # Build your CV sets here
    blue_train_x, blue_train_y, blue_test_x, blue_test_y = get_cv_set(blue_x, blue_y)
    wifi_train_x, wifi_train_y, wifi_test_x, wifi_test_y = get_cv_set(wifi_x, wifi_y)

    blue_forest = get_forest(blue_train_x, blue_train_y, blue_test_x, blue_test_y)
    wifi_forest = get_forest(wifi_train_x, wifi_train_y, wifi_test_x, wifi_test_y)


if __name__ == "__main__":
    main()
