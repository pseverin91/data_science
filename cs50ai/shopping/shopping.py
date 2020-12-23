import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Load data from csv file
    data = []
    with open(filename) as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
        data = data[1:]
    for i in range(len(data)):
        
        # Change month to numeric
        num = 0
        for month in ["Jan", "Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]:
            data[i][10] = num if data[i][10] == month else data[i][10]
            num += 1
        
        # Change visitor type to numeric
        data[i][15] = 1 if data[i][15] == "Returning_Visitor" else 0
        
        # Change weekend to numeric
        data[i][16] = 0 if data[i][16] == "FALSE" else 1
        
        # Change labels to numeric
        data[i][17] = 0 if data[i][17] == "FALSE" else 1
        
    # Make all values numeric
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = float(data[i][j])
    
    # Define output
    evidence, labels = [], []
    for row in data:
        evidence.append(row[:17])
        labels.append(row[17:][0])
    output = (evidence, labels)
    return output


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Estimate K-Nearest-Neighbors
    knn = KNeighborsClassifier(n_neighbors = 1)
    knn.fit(evidence, labels)
    
    return knn


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Initiate sensitivity and specificity variables
    sensitivity, specificity = 0, 0
    positives, negatives = 0, 0
    for i in range(len(labels)):
        
        # Compute number of positives
        sensitivity += 1 if labels[i] == 1 and labels[i] == predictions[i] else 0
        positives += 1 if labels[i] == 1 else 0
        
        # Compute number of negatives
        specificity += 1 if labels[i] == 0 and labels[i] == predictions[i] else 0
        negatives += 1 if labels[i] == 0 else 0
        
    # Compute positive and negative rate
    sensitivity /= positives
    specificity /= negatives
    
    # Output
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
