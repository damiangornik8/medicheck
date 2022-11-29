# Kian Cliffe
# R00179744

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import RocCurveDisplay
from keras.models import Sequential
from keras.layers import Dense

# Loading dataset
df = pd.read_csv('diabetes.csv', sep=',')

df.drop_duplicates(inplace=True)  # Drop duplicates
#print(df.duplicated().sum())

# Removing rows where these columns have a value = 0 as it would give an inaccurate reading
# as these values are either never 0 as the patient would be dead or rarely 0.
#print("Total : ", df[df.SkinThickness == 0].shape[0])
#print("Total : ", df[df.Insulin == 0].shape[0])
columns = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']

for col in columns:
    df[col].replace(0, np.NaN, inplace=True)  # Replacing values of 0 with NaN values

df.dropna(inplace=True)  # Dropping all NAN values

#print(df.head(10))

# Feature Engineering, assigning all but Outcome to X variable and the response 'Outcome' to
# y variable
feature_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI',
                 'DiabetesPedigreeFunction', 'Age']
X = df[feature_names]
y = df.Outcome  # Whether they have diabetes or not

#print(X, y)


# Spot Check Algorithms to test for the best one
models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))
models.append(('RF', RandomForestClassifier()))
models.append(('GB', GradientBoostingClassifier()))

'''
model = Sequential()

model.add(Dense(12, input_dim=8, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
history = model.fit(X, y, validation_split=0.33, epochs=100, batch_size=10, verbose=0)
# list all data in history
print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
'''


# Add test split later test_size=0.3,
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=df.Outcome,
                                                    random_state=0)

# evaluate each model in turn using 10 splits per algorithm then using the mean result of those splits to find the
# accuracy for each algorithm along with the standard deviation
results = []
names = []
for name, model in models:
    kfold = StratifiedKFold(n_splits=10, random_state=0, shuffle=True)
    cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy')
    results.append(cv_results)
    names.append(name)
    print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))

# Make predictions on test dataset using RandomForestClassifier() algorithm
model = RandomForestClassifier()
model.fit(X_train, y_train)  # Here x and y includes the dataframe with headers
predictions = model.predict(X_test)


#svc_disp = RocCurveDisplay.from_estimator(model, X_test, y_test)
#plt.show()
#print(svc_disp)


# Evaluate Predictions by printing accuracy of model
print()
print('Accuracy for test set for Random Forest Classifier = {}'.format(accuracy_score(y_test, predictions)))
#print(confusion_matrix(y_test, predictions))
print()
print(classification_report(y_test, predictions))


# Saving Model with Pickle
filename = 'diabetes_model.pkl'
pickle.dump(model, open(filename, 'wb'))


# Loading model with pickle
#loaded_model = pickle.load(open(filename, 'rb'))
#result = loaded_model.score(X_test, y_test)
#print(result)

'''
Each Value has to be integer like in test_value.
-------------------------
Diabetes
-------------------------
Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age

'''

test_value = [[2, 138, 62, 35, 0, 33.6, 0.127, 47]]  # This test returns: 0, meaning not likely to have heart disease
test_value2 = [[3, 171, 72, 33, 135, 33.3, 0.199, 24]] # This test returns: 1, meaning likely to have heart disease


loaded_model = pickle.load(open(filename, 'rb'))
result1 = loaded_model.predict(test_value)
result2 = loaded_model.predict(test_value2)
print(result1)
print(result2)
