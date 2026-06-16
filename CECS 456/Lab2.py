import keras
import pandas as pd
import time
import tensorflow as tf
import sklearn
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

rounds = 20


def comparison(seed: int):
    # time logging variables
    ANNtime = 0.0  # anything needed for the ANN will be logged here
    DTtime = ANNtime  # and anything needed for the DT here

    # loading
    start = time.time()  # both models need this section
    data = pd.read_csv(r"D:\Desktop\CSULB\CECS 456\stroke_risk_dataset.csv", low_memory=False)

    # preprocessing
    # drop irrelevant column
    data = data.drop(columns=["Stroke Risk (%)"])

    # normalize age column
    data["Age"] = (data["Age"] - data["Age"].values.min()) / (data["Age"].values.max() - data["Age"].values.min())

    # data and target sets
    source = data.drop("At Risk (Binary)", axis=1)
    target = data["At Risk (Binary)"].values

    # time updating
    current = time.time()
    ANNtime += current - start
    DTtime += current - start

    # ANN
    start = time.time()
    source_tensor = tf.convert_to_tensor(source, dtype=tf.float32)
    target_tensor = tf.convert_to_tensor(target, dtype=tf.float32)

    ANN = keras.Sequential([
        keras.layers.Dense(2, activation="relu", input_shape=(source.shape[1],)),
        keras.layers.Dense(1, activation="sigmoid")
    ])

    ANN.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    ANN.fit(source_tensor, target_tensor, epochs=10, batch_size=32, validation_split=0.2, verbose="False")

    current = time.time()
    ANNtime += current - start

    # Decision Tree
    start = time.time()

    depth = 15

    source_train, source_test, target_train, target_test = sklearn.model_selection.train_test_split(source,
                                                                                                    target,
                                                                                                    test_size=0.2,
                                                                                                    random_state=seed)

    DT = sklearn.tree.DecisionTreeClassifier(max_depth=depth, random_state=seed)

    DT.fit(source_train, target_train)

    current = time.time()

    DTtime += current - start

    # comparison

    # ANN
    ANN_predict_prob = ANN.predict(source_test).flatten()
    ANN_predict = (ANN_predict_prob > 0.5).astype(int)

    # DT
    DT_predict = DT.predict(source_test)
    DT_predict_prob = DT.predict_proba(source_test)[:, 1]

    return [target_test, DT_predict, ANN_predict, ANNtime/DTtime, DT_predict_prob, ANN_predict_prob]


def main():

    tests = []
    DT_predictions = []
    ANN_predictions = []
    time_avg = 0
    DT_predictions_probs = []
    ANN_predictions_probs = []

    for i in range(1, rounds + 1):
        print(f"\nRound {i}/{rounds}\n")
        result = comparison(seed=i)  # run one test

        tests.extend(result[0])
        DT_predictions.extend(result[1])
        ANN_predictions.extend(result[2])
        time_avg += result[3] / rounds
        DT_predictions_probs.extend(result[4])
        ANN_predictions_probs.extend(result[5])




    # Compute confusion matrices
    cm_dt = sklearn.metrics.confusion_matrix(tests, DT_predictions)
    cm_nn = sklearn.metrics.confusion_matrix(tests, ANN_predictions)

    # Plot confusion matrices
    labels = ["Negative", "Positive"]

    # change to percentages
    cm_dt = cm_dt.astype("float") / cm_dt.sum(axis=1, keepdims=True)
    cm_nn = cm_nn.astype("float") / cm_nn.sum(axis=1, keepdims=True)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    sns.heatmap(cm_dt, annot=True, fmt=".2%", cmap="Blues", xticklabels=labels, yticklabels=labels, ax=axes[0])
    axes[0].set_title("Decision Tree Confusion Matrix")
    axes[0].set_xlabel("Predicted")
    axes[0].set_ylabel("Actual")

    sns.heatmap(cm_nn, annot=True, fmt=".2%", cmap="Oranges", xticklabels=labels, yticklabels=labels, ax=axes[1])
    axes[1].set_title("Neural Network Confusion Matrix")
    axes[1].set_xlabel("Predicted")
    axes[1].set_ylabel("Actual")



    # Define metrics

    metrics = ["Accuracy", "Precision", "Recall", "F1-Score", "AUC"]


    DT_accuracy = sklearn.metrics.accuracy_score(tests, DT_predictions)
    DT_precision = sklearn.metrics.precision_score(tests, DT_predictions)
    DT_recall = sklearn.metrics.recall_score(tests, DT_predictions)
    DT_f1 = sklearn.metrics.f1_score(tests, DT_predictions)
    DT_auc = sklearn.metrics.roc_auc_score(tests, DT_predictions_probs)
    values_DT = [DT_accuracy, DT_precision, DT_recall, DT_f1, DT_auc]  # this would be completely unreadable if I put the functions in it


    ANN_accuracy = sklearn.metrics.accuracy_score(tests, ANN_predictions)
    ANN_precision = sklearn.metrics.precision_score(tests, ANN_predictions)
    ANN_recall = sklearn.metrics.recall_score(tests, ANN_predictions)
    ANN_f1 = sklearn.metrics.f1_score(tests, ANN_predictions)
    ANN_auc = sklearn.metrics.roc_auc_score(tests, ANN_predictions_probs)
    values_ANN = [ANN_accuracy, ANN_precision, ANN_recall, ANN_f1, ANN_auc]  # this would be completely unreadable if I put the functions in it

    label_pos = np.arange(len(metrics))  # Label positions



    # Create bar plots
    plt.figure(figsize=(8, 5))
    plt.bar(label_pos - 0.2, values_DT, width=0.4, label="Decision Tree", color="royalblue")
    plt.bar(label_pos + 0.2, values_ANN, width=0.4, label="Neural Network", color="darkorange")

    plt.xticks(label_pos, metrics)
    plt.ylabel("Score")
    plt.title("Model Performance Comparison")

    plt.legend()

    plt.figure(figsize=(8, 5))
    plt.bar(label_pos - 0.2, values_DT, width=0.4, label="Decision Tree", color="royalblue")
    plt.bar(label_pos + 0.2, values_ANN, width=0.4, label="Neural Network", color="darkorange")

    plt.xticks(label_pos, metrics)
    plt.ylabel("Score")
    plt.title("Model Performance Comparison (logarithmic)")

    plt.legend()

    plt.yscale("log")


    # ROC curve



    # Compute ROC curve data
    fpr_dt, tpr_dt, _ = sklearn.metrics.roc_curve(tests, DT_predictions_probs)
    fpr_nn, tpr_nn, _ = sklearn.metrics.roc_curve(tests, ANN_predictions_probs)

    # Compute AUC values
    auc_dt = sklearn.metrics.auc(fpr_dt, tpr_dt)
    auc_nn = sklearn.metrics.auc(fpr_nn, tpr_nn)

    # Plot ROC curve
    plt.figure(figsize=(8, 6))
    plt.plot(fpr_dt, tpr_dt, label=f"Decision Tree (AUC = {auc_dt:.2f})", linestyle="--", color="blue")
    plt.plot(fpr_nn, tpr_nn, label=f"Neural Network (AUC = {auc_nn:.2f})", linestyle="-", color="orange")

    # Add reference line
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Random Model")

    # Labels and legend
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve Comparison")
    plt.legend()



    print(f"DT was {time_avg:.4f}x faster than ANN on avg.")

    plt.show()

main()