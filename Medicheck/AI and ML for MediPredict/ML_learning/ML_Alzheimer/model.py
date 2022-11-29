# Kian Cliffe
# R00179744

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, auc, roc_curve
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.callbacks import ModelCheckpoint

# Note that 'Group' column is whether the patient has Alzheimer's or not


# Loading dataset
df = pd.read_csv('alzheimers.csv', sep=',')
print(df.head())

# Dropping 3 categorical columns as these are identification parameters and not useful for
# training model
df.drop(['Subject ID', 'MRI ID'], axis=1, inplace=True)

# Hand is dropped as it won't help with prediction whether patient has alzheimer's or not
df.drop(['Hand'], axis=1, inplace=True)
#df.drop(columns=['Subject ID', 'MRI ID'])
#print(df.head())

# Converting categorical data into numerical. (M:1 F:0)
df['M/F'] = np.where((df['M/F'] == 'M'), 1, 0)
print(df.head())

# Checking for empty columns
#print(df.isna().sum())

# Filling empty values with their mean from their column
df['SES'] = df.SES.fillna(df.SES.mean())
df['MMSE'] = df.MMSE.fillna(df.MMSE.mean())
#print(df.isna().sum())

# Changing string values into whether patient has a form of alzheimer's or not
df['Group'] = df['Group'].replace(['Nondemented', 'Demented', 'Converted'], [0, 1, 1])
print(df.head())

# Feature Engineering, assigning all but Group to X variable and the response 'Group' to
# y variable
feature_names = ['Visit', 'MR Delay', 'M/F', 'Age', 'EDUC', 'SES', 'MMSE', 'CDR', 'eTIV',
                 'nWBV', 'ASF']

X = df[feature_names]
y = df.Group

print(X, y)

# Spot Check Algorithms to test for the best one
models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))
models.append(('RF', RandomForestClassifier()))
models.append(('GB', GradientBoostingClassifier()))
models.append(('CART', DecisionTreeClassifier()))


# Train/test split, test_size=0.3,
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,  random_state=0)

# evaluate each model in turn using 10 splits per algorithm then using the mean result of those splits to find the
# accuracy for each algorithm along with the standard deviation
results = []
names = []
for name, model in models:
    kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
    cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy')
    results.append(cv_results)
    names.append(name)
    print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))

# Make predictions on test dataset using
model = GradientBoostingClassifier()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Evaluate Predictions
print()
print('Accuracy for test set for Gradient Boosting Classifier = {}'.format(accuracy_score(y_test, predictions)))
#print(confusion_matrix(y_test, predictions))
print()
print(classification_report(y_test, predictions))

# Saving Model with Pickle
filename = 'alzheimer_model.pkl'  # Can use .sav file also
pickle.dump(model, open(filename, 'wb'))

''' 
Each Value has to be integer like in test_value.
-------------------------
Alzheimer's
-------------------------
Visit, MR Delay, M/F, Age, EDUC, SES, MMSE, CDR, eTIV, nWBV, ASF 
'''

test_value = [[1, 0, 1, 75, 12, 12, 23, 0.5, 1678, 0.736, 1.046]]  # This test returns: 1, meaning has dementia
test_value2 = [[2, 457, 1, 88, 14, 2, 30, 0, 2004, 0.681, 0.876]]  # This test returns: 0, meaning no dementia

loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.predict(test_value)
result2 = loaded_model.predict(test_value2)
print(result)
print(result2)
