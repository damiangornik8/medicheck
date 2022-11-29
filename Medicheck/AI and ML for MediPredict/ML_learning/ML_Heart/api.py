import pickle


df = [[63, 1, 1, 145, 233, 1, 2, 150, 0,
              2.3, 3, 0, 6, 0]]

df.columns = ['age', 'sex', 'cp', 'trestbps', 'chol',
              'fbs', 'restecg', 'thalach', 'exang',
              'oldpeak', 'slope', 'ca', 'thal', 'target']



# Loading model with pickle
filename = 'heart_model.sav'

loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.predict(df)
print(result)
