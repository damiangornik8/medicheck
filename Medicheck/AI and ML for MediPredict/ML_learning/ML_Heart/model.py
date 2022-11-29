# Kian Cliffe
# R00179744

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# Loading dataset
df = pd.read_csv('heartdisease.csv', header=None)
# Naming columns
df.columns = ['age', 'sex', 'cp', 'trestbps', 'chol',
              'fbs', 'restecg', 'thalach', 'exang',
              'oldpeak', 'slope', 'ca', 'thal', 'target']
#print(df.columns)

# Cleaning dataset with pandas library

#print(df.isnull().sum())  # Returns number of missing values

df['target'] = df.target.map({0: 0, 1: 1, 2: 1, 3: 1, 4: 1})  # Mapping 1:0 whether patient has heart disease or not
df['sex'] = df.sex.map({0: 'female', 1: 'male'})
df['thal'] = df.thal.fillna(df.thal.mean())  # fill missing values with the sample mean
df['ca'] = df.ca.fillna(df.ca.mean())   # fill 'ca' column's missing values with the sample mean

# 1 = Male, 0 = Female
df['sex'] = df.sex.map({'female': 0, 'male': 1})

df['target'] = df['target'].replace([2, 3, 4], [1, 1, 1])  # Converting all ints where patient has heart disease to 1
#print(df.head)

# Feature Engineering, assigning all but target to X variable and the response 'target' to
# y variable

feature_names = ['age', 'sex', 'cp', 'trestbps', 'chol',
              'fbs', 'restecg', 'thalach', 'exang',
              'oldpeak', 'slope', 'ca', 'thal']

X = df[feature_names]
y = df.target

#print(X, y)
#print(X.head(10))

# splitting the data into training and testing, with 30% of data being used for testing
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.3,
                                                    random_state=0)


# Spot Check Algorithms to test for the best one
models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))

# evaluate each model in turn using 10 fold cross evaluation per algorithm then using the
# mean result of those splits to find the accuracy for each algorithm along with the standard deviation
results = []
names = []
for name, model in models:
    kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
    cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
    results.append(cv_results)
    names.append(name)
    print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))

# Make predictions on test dataset using NB model
model = GaussianNB()
model.fit(X_train, Y_train)
predictions = model.predict(X_test)

# Evaluate Predictions
print()
print('Accuracy for test set for Gaussian Naive Bayes = {}'.format(accuracy_score(Y_test, predictions)))
print()
#print(confusion_matrix(Y_test, predictions))
print(classification_report(Y_test, predictions))

# Saving Model with Pickle
filename = 'heart_model.pkl'
pickle.dump(model, open(filename, 'wb'))

'''
# Loading model with pickle
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(X_test, Y_test)
print(result)
'''

'''
Each Value has to be integer like in test_value.
-------------------------
Heart
-------------------------
age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
'''

test_value = [[63, 1, 1, 145, 233, 1, 2, 150, 0, 2.3, 3, 0, 6]]  # This test returns: 0, meaning no heart disease
test_value2 = [[63, 1, 4, 130, 254, 0, 2, 147, 0, 1.4, 2, 1, 7]]  # This test returns: 1, meaning has heart disease

loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.predict(test_value)
result2 = loaded_model.predict(test_value2)
print(result)
print(result2)
