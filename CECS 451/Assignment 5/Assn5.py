import sklearn
import pandas as pd
import matplotlib.pyplot as plt

# preprocessing
raw_data = sklearn.datasets.load_breast_cancer()
source = pd.DataFrame(raw_data.data, columns=raw_data.feature_names)
target = raw_data.target

source_train, source_test, target_train, target_test = sklearn.model_selection.train_test_split(source, target,
                                                                                                test_size=0.5)

criterion = 'entropy'
depth = 2


# simple DT
simple_DT = sklearn.tree.DecisionTreeClassifier(criterion=criterion, max_depth=depth)
simple_DT.fit(source_train, target_train)


confusion_matrix = sklearn.metrics.confusion_matrix(target_test, simple_DT.predict(source_test))
normalized_cm = confusion_matrix.astype("float") / confusion_matrix.sum(axis=1, keepdims=True)
print("\nModel: Simple DT")
print(f"Accuracy: {(normalized_cm[0][0] + normalized_cm[1][1])/2}")
print("Confusion Matrix:")
print(normalized_cm)
sklearn.tree.plot_tree(simple_DT, feature_names=raw_data.feature_names, fontsize=15)
plt.title("Decision tree")
plt.show()

# bagging
score_history = []
for i in range(1, 30):
    bagging = sklearn.ensemble.BaggingClassifier(estimator=sklearn.tree.DecisionTreeClassifier(criterion=criterion,
                                                                                               max_depth=depth),
                                                 n_estimators=i)
    bagging.fit(source_train, target_train)
    bagging_score = sklearn.metrics.accuracy_score(target_test, bagging.predict(source_test))
    score_history.append((i, bagging_score))

zip_history = zip(*score_history)
plt.title("Bagging plot")
plt.xlabel("n_estimators")
plt.ylabel("bagging_score")
plt.plot(*zip_history, color='b')
plt.show()

# adaboost
score_history = []
for i in range(1, 30):
    adaboost = sklearn.ensemble.AdaBoostClassifier(estimator=sklearn.tree.DecisionTreeClassifier(criterion=criterion,
                                                                                                 max_depth=depth),
                                                   n_estimators=i)
    adaboost.fit(source_train, target_train)
    boost_score = sklearn.metrics.accuracy_score(target_test, adaboost.predict(source_test))
    score_history.append((i, boost_score))

zip_history = zip(*score_history)
plt.title("Adaboost plot")
plt.xlabel("n_estimators")
plt.ylabel("boost_score")
plt.plot(*zip_history, color='b')
plt.show()


# random forest
score_history = []
for i in range(1, 30):
    random_forest = sklearn.ensemble.RandomForestClassifier(criterion=criterion, max_depth=depth, n_estimators=100, max_features=i)
    random_forest.fit(source_train, target_train)
    forest_score = sklearn.metrics.accuracy_score(target_test, random_forest.predict(source_test))
    score_history.append((i, forest_score))

zip_history = zip(*score_history)
plt.title("Random forest plot")
plt.xlabel("max_features")
plt.ylabel("boost_score")
plt.plot(*zip_history, color='b')
plt.show()

