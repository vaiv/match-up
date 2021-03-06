import itertools
import numpy as np
import random
import os
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import validation_curve
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot as plt
import io
import collections


def CountFrequency(arr):
    return collections.Counter(arr)


def summation(elements):
    answer = 0
    for i in range(len(elements)):
        answer += elements[i]
    return answer


def mean(elements):
    numerator = summation(elements)
    return numerator/len(elements)


def std_dev(elements):
    miu = mean(elements)
    variance = 0
    for i in range(len(elements)):
        variance += (elements[i] - miu) * (elements[i] - miu)
    variance = variance/len(elements)
    return variance


def normal(elements):
    return None


# Input: A file with numbers:
# Like 1, 2, 3, 4, 5, 1
# Get <1, 2> <2, 1>, <3, 1>, def
def frequency_count(filename="./../../HOME_g8.csv", header=True):
    freq_map = None
    whole = ""
    with io.open(filename, "r") as f:
        for row in f:
            if header:
                f.readline()
                header = False
            # The last column always gets corrupted!
            else:
                row = row.replace('\n', '')
                whole += row
    print(whole)
    int_list = [int(x) for x in whole.split(",")]
    freq_map = CountFrequency(int_list)
    print(freq_map)
    return freq_map


# Input: A Hash Map <K, V> Key is item, Value is Frequency
# Plot a Histogram!
def frequency_histogram(hash_map):
    # Filtering is required
    good_map = dict((key, value) for key, value in hash_map.items() if 1 <= key <= 11)
    k = list(good_map.keys())
    v = list(good_map.values())
    plt.bar(k, v, align='center', color='blue')
    plt.xlabel('elements')
    plt.ylabel('count')
    plt.title('Frequency histogram')
    # plt.xticks(indexes, labels)
    # plt.savefig(str('./histogram.png'))
    plt.show()


# This is only for this specific case...
def read_data_set(filename, isnumeric=False):
    x = np.genfromtxt(filename, delimiter=',', skip_header=1)
    if isnumeric:
        y = x[:, 0]
    else:
        y = np.genfromtxt(filename, delimiter=',', skip_header=1, dtype=str)
        y = y[:, 0]
    # x must delete first column which is the label
    x = x[:, 1:]
    print(y)
    return x, y


# This is only for this specific case...
def read_cluster_data_set(filename):
    x = np.genfromtxt(filename, delimiter=',', skip_header=1)
    return x


def get_cv_set(training_set, test_set, percentile=0.2):
    row = np.shape(training_set)[0]
    col = np.shape(training_set)[1]
    sample_idx = random.sample(range(row), int(percentile * row))

    # Get your CV data
    cv_train = training_set[sample_idx[:], 0:col]
    cv_test = test_set[sample_idx[:]]

    # Remove CV data from original
    set_diff = np.setdiff1d(np.arange(row), sample_idx)
    training_set = training_set[set_diff[:], 0:col]
    test_set = test_set[set_diff[:]]
    return training_set, test_set, cv_train, cv_test


def top(clf, test_x, test_y, extra_rooms=1):
    # Get your list...
    # Sort it such that highest probabilities come first...
    # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    # To print highest first, set reverse=True
    probability_dict = []
    for i in range(len(test_y)):
        if hasattr(clf, 'decision_function'):
            probability_dict.append(dict(zip(clf.classes_, clf.decision_function(test_x)[i])))
        else:
            probability_dict.append(dict(zip(clf.classes_, clf.predict_proba(test_x)[i])))
        probability_dict[i] = sorted([(v, k) for k, v in probability_dict[i].items()], reverse=True)

    success = 0
    # Let us say test the first 3 rooms? See if it matches!
    for i in range(len(test_y)):
        # print(probability_dict[i])
        for j in range(extra_rooms):
            if probability_dict[i][j][1] == test_y[i]:
                success = success + 1
                break
    # print("Test Error for " + str(extra_rooms) + " Rooms: " + str(success/len(test_y)))


def scale(train_x, test_x):
    scalar = StandardScaler()
    # Don't cheat - fit only on training data
    scalar.fit(train_x)
    x_train = scalar.transform(train_x)
    # apply same transformation to test data
    x_test = scalar.transform(test_x)
    return x_train, x_test


# If the data is co-linear you must use PCA
# Hopefully this function should get the PCA the explains up to 90% variance minimum
def scale_and_pca(train_x, test_x):
    scaled_train_x, scaled_test_x = scale(train_x, test_x)
    pr_comp = PCA(n_components=0.99, svd_solver='full')
    pr_comp.fit(scaled_train_x)
    return pr_comp.transform(scaled_train_x), pr_comp.transform(scaled_test_x)


def plot_grid_search(cv_results, grid_param, name_param, directory="Cross_Validation"):
    # Create target Directory if don't exist
    if not os.path.exists(directory):
        os.mkdir(directory)
    #    print("Directory ", directory, " Created! ")
    # else:
        # print("Directory ", "Cross_Validation", " already exists")

    # Get Test Scores Mean and std for each grid search
    scores_mean = cv_results['mean_test_score']
    scores_mean = np.array(scores_mean).reshape(len(grid_param))

    # Plot Grid search scores
    _, ax = plt.subplots(1, 1)

    # Param1 is the X-axis, Param 2 is represented as a different curve (color line)
    ax.plot(grid_param, scores_mean, label="CV-Curve")

    ax.set_title("Grid Search Scores", fontsize=20, fontweight='bold')
    ax.set_xlabel(name_param, fontsize=16)
    ax.set_ylabel('CV Average Score', fontsize=16)
    ax.legend(loc="best", fontsize=15)
    ax.grid('on')
    plt.savefig(str('./Cross_Validation/CV_Plot_'+name_param+'.png'))
    # plt.show()


def plot_validation_curve(x, y, param_range, param_name, clf, clf_name="SVM"):
    train_scores, test_scores = validation_curve(
        clf, x, y, param_name=param_name, param_range=param_range,
        cv=10, scoring="accuracy", n_jobs=-1)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.title("Validation Curve with " + clf_name)
    plt.xlabel(param_name)
    plt.ylabel("Score")
    plt.ylim(0.0, 1.1)
    lw = 2
    plt.semilogx(param_range, train_scores_mean, label="Training score",
                 color="darkorange", lw=lw)
    plt.fill_between(param_range, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.2,
                     color="darkorange", lw=lw)
    plt.semilogx(param_range, test_scores_mean, label="Cross-validation score",
                 color="navy", lw=lw)
    plt.fill_between(param_range, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.2,
                     color="navy", lw=lw)
    plt.legend(loc="best")
    plt.show()


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    #    print("Normalized confusion matrix")
    # else:
    #    print('Confusion matrix, without normalization')
    # print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def make_confusion_matrix(y_true, y_pred, clf, clf_name, directory="Confusion_Matrix"):
    # Create target Directory if don't exist
    if not os.path.exists(directory):
        os.mkdir("Confusion_Matrix")
    #    print("Directory ", directory, " Created ")
    # else:
    #    print("Directory ", directory, " already exists")

    # Compute confusion matrix
    cnf_matrix = confusion_matrix(y_true, y_pred)
    np.set_printoptions(precision=2)
    # Plot non-normalized confusion matrix
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=[str(i) for i in clf.classes_], normalize=False,
                          title='Confusion matrix, without normalization: ')
    plt.savefig(str('./Confusion_Matrix/Confusion_Matrix_'+clf_name+'.png'))

    # Plot normalized confusion matrix
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=[str(i) for i in clf.classes_], normalize=True,
                          title='Normalized confusion matrix')
    plt.savefig(str('./Confusion_Matrix/Normalized_Confusion_Matrix_'+clf_name+'.png'))
    # plt.show()
