import time
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import scale
from generic import *


# http://scikit-learn.org/stable/auto_examples/neural_networks/plot_mlp_alpha.html#sphx-glr-auto-examples-neural-networks-plot-mlp-alpha-py
# http://scikit-learn.org/stable/auto_examples/neural_networks/plot_mlp_training_curves.html#sphx-glr-auto-examples-neural-networks-plot-mlp-training-curves-py
def get_brain(train_x, train_y, test_x, test_y):
    start_time = time.time()
    clf = tune_brain(train_x, train_y)
    print("--- Best Parameter NN Generation: %s seconds ---" % (time.time() - start_time))
    # Print Training and Test Error
    print("Best NN Parameters: " + str(clf.get_params()))
    print("Training Mean Test Score: " + str(clf.score(train_x, train_y)))
    y_hat = clf.predict(test_x)
    print("Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)))

    make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=clf, clf_name='NN')
    # top(clf, test_x, test_y, extra_rooms=2)
    with open("results.txt", "a") as my_file:
        my_file.write("[NN] Training Mean Test Score: " + str(clf.score(train_x, train_y)))
        my_file.write("[NN] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)))

    with open("classification_reports.txt", "a") as my_file:
        my_file.write("---[Random Forest]---")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            target_names=[str(i) for i in clf.classes_]))
    # print(classification_report(test_y, y_hat, target_names=[str(i) for i in clf.classes_]))
    return clf


# Note alpha needs to grow exponentially!
def tune_brain(train_x, train_y, n_fold=10):
    # want to go from 0.001 to 1, but on exponential scale!
    alphas = np.logspace(start=-5, stop=0, endpoint=True, num=5)
    hidden_layer = np.arange(3, 10, 1)
    solvers = ['lbfgs', 'adam']
    # param_grid = {'alpha': alphas, 'hidden_layer_sizes': hidden_layer, 'solver': solvers}

    # ----alpha----
    brain_alpha = GridSearchCV(MLPClassifier(warm_start=False), {'alpha': alphas}, n_jobs=-1, cv=n_fold)
    brain_alpha.fit(train_x, train_y)
    plot_grid_search(brain_alpha.cv_results_, alphas, 'alpha')
    # ----hidden layer----
    brain_layers = GridSearchCV(MLPClassifier(warm_start=False), {'hidden_layer_sizes': hidden_layer}, n_jobs=-1, cv=n_fold)
    brain_layers.fit(train_x, train_y)
    plot_grid_search(brain_layers.cv_results_, hidden_layer, 'hidden_layer')
    # ---solvers----
    brain_solver = GridSearchCV(MLPClassifier(warm_start=False), {'solver': solvers}, n_jobs=-1, cv=n_fold)
    brain_solver.fit(train_x, train_y)
    plot_grid_search(brain_solver.cv_results_, solvers, 'solver')

    # ----------------Final---------------------
    clf = MLPClassifier(warm_start=False, hidden_layer_sizes=brain_layers.best_params_['hidden_layer_sizes'],
                        alpha=brain_alpha.best_params_['alpha'], solver=brain_solver.best_params_['solver'])
    clf.fit(train_x, train_y)
    return clf


def main():
    # Read Wifi and Blue Tooth Data Set
    blue_x, blue_y = read_data_set('./blue.csv')
    wifi_x, wifi_y = read_data_set('./wifi.csv')

    # Build your CV sets here
    blue_train_x, blue_train_y, blue_test_x, blue_test_y = get_cv_set(blue_x, blue_y)
    wifi_train_x, wifi_train_y, wifi_test_x, wifi_test_y = get_cv_set(wifi_x, wifi_y)

    # I HAVE BEEN WARNED THAT THIS CLASSIFIER NEEDS SCALED DATA!
    blue_train_x, blue_test_x = scale(blue_train_x, blue_test_x)
    wifi_train_x, wifi_test_x = scale(wifi_train_x, wifi_test_x)

    blue_brain = get_brain(blue_train_x, blue_train_y, blue_test_x, blue_test_y)
    wifi_brain = get_brain(wifi_train_x, wifi_train_y, wifi_test_x, wifi_test_y)


if __name__ == "__main__":
    main()