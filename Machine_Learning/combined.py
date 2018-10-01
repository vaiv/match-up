from sklearn.ensemble import VotingClassifier
from generic import *


# Overall Purpose...
# I will have 3 Classifiers
# Wifi, BlueTooth and Misc. Rooms
# I can combined them using the Voting Classifier
# Reference: http://scikit-learn.org/stable/modules/ensemble.html
# I am assuming the three input classifiers are fitted...
def combined_classifier(room_clf, wifi_clf, blue_clf, train_x, train_y):
    # The type of classifier will depend on preliminary results...
    clf = VotingClassifier(estimators=[('dt', room_clf), ('knn', wifi_clf),
                                       ('svc', blue_clf)], voting='soft', weights=[2, 1, 2], n_jobs=1)
    clf.fit(train_x, train_y)


def main():
    # pip.main(['install', 'mlxtend'])
    # Read Wifi and Blue Tooth Data Set
    blue_x, blue_y = read_data_set('./blue.csv')
    wifi_x, wifi_y = read_data_set('./wifi.csv')

    # Build your CV sets here
    blue_train_x, blue_train_y, blue_test_x, blue_test_y = get_cv_set(blue_x, blue_y)
    wifi_train_x, wifi_train_y, wifi_test_x, wifi_test_y = get_cv_set(wifi_x, wifi_y)


if __name__ == "__main__":
    main()
