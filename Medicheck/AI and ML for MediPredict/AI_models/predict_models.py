# Kian Cliffe
import pickle

''' Need to install package: scikit-learn version 1.0.1 
    TO;DO: Modify model functions to accept firebase inputs as prediction values'''

'''
Each Value has to be integer like in test_value and also needs to be passed in the correct order from firebase.
-------------------------
DIABETES  Accuracy: 73%
-------------------------
Column Names:
Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age
'''

def diabetes_model():

    filename = 'diabetes_model.pkl'  # Name of file being loaded

    test_value = [[2, 138, 62, 35, 0, 33.6, 0.127, 47]]  # This test returns: 0, meaning not likely to have heart disease
    test_value2 = [[3, 171, 72, 33, 135, 33.3, 0.199, 24]]  # This test returns: 1, meaning likely to have heart disease

    loaded_model = pickle.load(open(filename, 'rb'))  # This loads the model
    result1 = loaded_model.predict(test_value)  # This predicts the first set of test values
    result2 = loaded_model.predict(test_value2)  # This predicts the second set of test values

    # Prints results of test values
    print("DIABETES MODEL RESULTS")
    print(result1)  # Should print [0]
    print(result2)  # Should print [1]


'''
Each Value has to be integer like in test_value.
-------------------------
HEART DISEASE  Accuracy: 82%
-------------------------
Column Names:
age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
'''

def heart_model():
    filename = 'heart_model.pkl'  # Name of file being loaded

    test_value = [[63, 1, 1, 145, 233, 1, 2, 150, 0, 2.3, 3, 0, 6]]  # This test returns: 0, meaning no heart disease
    test_value2 = [[63, 1, 4, 130, 254, 0, 2, 147, 0, 1.4, 2, 1, 7]]  # This test returns: 1, meaning has heart disease

    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict(test_value)
    result2 = loaded_model.predict(test_value2)
    print("HEART DISEASE MODEL RESULTS")
    print(result)
    print(result2)


def alzheimer_model():
    filename = 'alzheimer_model.pkl'

    ''' 
    -------------------------
    ALZHEIMER'S  Accuracy: 92%
    -------------------------
    Column Names:
    Visit, MR Delay, M/F, Age, EDUC, SES, MMSE, CDR, eTIV, nWBV, ASF 
    '''

    test_value = [[1, 0, 1, 75, 12, 12, 23, 0.5, 1678, 0.736, 1.046]]  # This test returns: 1, meaning has dementia
    test_value2 = [[2, 457, 1, 88, 14, 2, 30, 0, 2004, 0.681, 0.876]]  # This test returns: 0, meaning no dementia

    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict(test_value)
    result2 = loaded_model.predict(test_value2)
    print("ALZHEIMER'S MODEL RESULTS")
    print(result)
    print(result2)


def main():
    diabetes_model()
    heart_model()
    alzheimer_model()


main()
