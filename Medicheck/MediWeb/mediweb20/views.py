from django.http import HttpResponse
from django.shortcuts import render 
from django.contrib.auth import authenticate
from django.db import models

import pyrebase 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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



    
config= {
    "apiKey": "AIzaSyBu86x_GupGfNc_NHIaD8CwdGVp-UJfwKo",
    "authDomain": "mediweb-94472.firebaseapp.com",
    "databaseURL": "https://mediweb-94472-default-rtdb.firebaseio.com",
    "projectId": "mediweb-94472",
    "storageBucket": "mediweb-94472.appspot.com",
    "messagingSenderId": "863481855765",
    "appId": "1:863481855765:web:56c4173ed1f3cca2e0731c"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


if not firebase_admin._apps:
    cred = credentials.Certificate("mediweb-key.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


        
patientsList = [] 
doctorslist = [] 

class doctor: 
        def __init__(self, firstName, lastName, emailAddress, listOfPatients,specialty): 
            self.firstName = firstName
            self.lastName = lastName
            
            self.emailAddress = emailAddress
            self.listOfPatients = listOfPatients
            self.specialty = specialty


doctors_ref = db.collection('doctors')
doc_docs = doctors_ref.stream()

for doc in doc_docs:
    firstName = u'{}'.format(doc.to_dict()['FirstName'])
    lastName = u'{}'.format(doc.to_dict()['LastName'])
    email = u'{}'.format(doc.to_dict()['Email'])
    listOfPatients = u'{}'.format(doc.to_dict()['ListOfPatients'])
    specialty = u'{}'.format(doc.to_dict()['Specialty'])

    doctorslist.append(doctor (firstName, lastName, email, listOfPatients, specialty))
   
def getPatients(username):
    class patient: 
        def __init__(self, firstName, lastName, emailAddress, patientID, phoneNumber, address, DOB): 
            self.firstName = firstName 
            self.lastName = lastName
            self.emailAddress = emailAddress

            self.patientID = patientID
            self.phoneNumber = phoneNumber
            self.address = address
            self.DOB = DOB

    if not patientsList:
        users_ref = db.collection('patients')
        docs = users_ref.stream()

        for doc in docs:
            patient_first_name = u'{}'.format(doc.to_dict()['FirstName'])
            patient_last_name = u'{}'.format(doc.to_dict()['LastName'])
            patient_email = u'{}'.format(doc.to_dict()['Email'])

            patientID = u'{}'.format(doc.to_dict()['PatientID'])
            phoneNumber = u'{}'.format(doc.to_dict()['Phone Number'])
            address = u'{}'.format(doc.to_dict()['Address'])
            dob = u'{}'.format(doc.to_dict()['DOB'])

            for doctor in doctorslist:
                if (doctor.emailAddress == username):
                    for patient_id in doctor.listOfPatients:
                        if (patientID == patient_id):
                            patientsList.append(patient (patient_first_name, patient_last_name, patient_email, patientID, phoneNumber, address, dob))


    else:
        patientsList.clear()

        users_ref = db.collection('patients')
        docs = users_ref.stream()

        for doc in docs:
            patient_first_name = u'{}'.format(doc.to_dict()['FirstName'])
            patient_last_name = u'{}'.format(doc.to_dict()['LastName'])
            patient_email = u'{}'.format(doc.to_dict()['Email'])

            patientID = u'{}'.format(doc.to_dict()['PatientID'])
            phoneNumber = u'{}'.format(doc.to_dict()['Phone Number'])
            address = u'{}'.format(doc.to_dict()['Address'])
            dob = u'{}'.format(doc.to_dict()['DOB'])

            for doctor in doctorslist:
                if (doctor.emailAddress == username):
                    for patient_id in doctor.listOfPatients:
                        if (patientID == patient_id):
                            patientsList.append(patient (patient_first_name, patient_last_name, patient_email, patientID, phoneNumber, address, dob))



def seePatientDetails(request):
    patientID = request.POST.get('patientID')

    for patient in patientsList:
        if (patient.patientID == patientID):
            return render(request, 'patient-details.html', {
                    "patient" : patient,
                    "patientID" : patientID,  
                })


def updatePatientDetails(request):
    # patientID_input = request.POST.get('patientID')

    patientID_input = 2

   

    firstName = ""
    lastName = ""
    email = ""
    address = ""
    phoneNumber = ""

    for patient in patientsList:
        print(type(patientID_input))
        print(type(int(patient.patientID) ))

        if (int(patient.patientID) == patientID_input):



            firstName = patient.patient_first_name
            lastName = patient.patient_last_name
            email = patient.patient_email
            address = patient.address
            phoneNumber = patient.phoneNumber

            print(firstName, lastName, email, address, phoneNumber)




    return render(request, 'patient-details.html', {
            "firstName" : firstName,
       "lastName" :  lastName,
        "email" :  email,
        "address" : address,
         "phoneNumber" :  phoneNumber,
        })


def patients(request):
    return render(request, 'patients.html', {
        "patientsList" : patientsList,   
        })



def welcome(request):
    return render(request,'welcome.html')


import re   
  
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
  
def checkEmail(email):   
  
    if(re.search(regex,email)):   
        return True
    else:   
        return False 


def signup_post(request):
    email = request.POST.get('email')
    passs = request.POST.get('password')

    firstName = request.POST.get('firstName')
    lastName = request.POST.get('lastName')
    specialty = request.POST.get('specialty_from_dropdown')

    toChange = ""
    allgood = True

    for doctor in doctorslist:
        if (doctor.emailAddress == email):
            tochange = toChange + "\n" + "Email already exists in our database."

            allgood = False
    
    if (firstName == "" or lastName == "" or passs == "" or email == ""):
        tochange = toChange + "\n" + "Some fields are empty. Please fill them up. "
        allgood = False
    
    if (checkEmail(email) == False):
        tochange = toChange + "\n" + "Your email address is invalid. Please enter a valid email."

    
    
    if (allgood == True):
        try:
            # creating a user with the given email and password
            user=authe.create_user_with_email_and_password(email,passs)
            id = len(doctorslist) + 1
            id_str = str(id)

            db.collection("doctors").add(
            {
            'DoctorID' : id_str,
            'FirstName' : firstName,
                'LastName' : lastName,
            'Specialty' : specialty,

            'Email' : email,
            'Password' : passs,

            'ListOfPatients' : [],
        })

            uid = user['localId']
            idtoken = request.session['uid']
            print(uid)

        except:
            return HttpResponse("Something went wrong...")

        return render(request,"welcome.html")
    
    else:
        return render(request, 'signup.html', {
            "specialtiesList" : specialtiesList,
        "tochange" : tochange,
        })

specialtiesList= ["Surgeon", "Podiatrist"]  

def signup(request):
    return render(request, 'signup.html', {
    "specialtiesList" : specialtiesList,
    })

doctor_firstName = ""
doctor_LastName = ""
specialty = ""

def signin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    for doctor in doctorslist:
        if (doctor.emailAddress == username):
            print("OK")

            doctor_firstName = doctor.firstName
            doctor_LastName = doctor.lastName
            specialty = doctor.specialty

    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(username,password)

    except:
        return HttpResponse("Wrong username or password")

    session_id=user['idToken']
    request.session['uid']=str(session_id) 

    getPatients(username)
    
    return render(request, 'dashboard.html', {
        "user_FirstName" : doctor_firstName,
        "user_LastName" : doctor_LastName,
        "user_Specialty": specialty
        })

def logout(request):
    try:
        del request.session['uid']

    except:
        pass

    print("You're logged in")
    return render(request,"welcome.html")

def dashboard(request):
    return render(request, 'dashboard.html', {
        "user_FirstName" : doctor_firstName,
        "user_LastName" : doctor_LastName,
        "user_Specialty": specialty
        })



def riskProfiles(request):
    return render(request, 'risk-profiles.html', {
        "patientsList" : patientsList,
        
        })



def alzheimerRiskProfile_Api():
    result = "Medium level of risk"
    return result

def patientRiskProfiles(request):
    patientID = request.POST.get('patient_from_dropdown')
    AlzheimerRiskProfile_Report = []
    docs = db.collection("patients").get()

    for doc in docs:
        if (str(doc.to_dict()['PatientID']))==patientID:
            key = doc.id
            AlzheimerRiskProfile_Report = u'{}'.format(doc.to_dict()['Alzheimer_RiskLevel_Reports'])

        else:
            print("They are different...")

    return render(request, 'user-profiling.html', {
        "patientsList" : patientsList,
        "alzheimer_RiskReports" : AlzheimerRiskProfile_Report,  
    })


def alzheimerRiskProfilesRun(request):
    alzheimerRiskProfile_Api()

    patientID = request.POST.get('patient_from_dropdown')
    patientId_string = str(patientID)
    docs = db.collection("patients").get()

    for doc in docs:
        if (str(doc.to_dict()['PatientID']))==patientId_string:

            key = doc.id
            AlzheimerRiskProfile_Report = []
            AlzheimerRiskProfile_Report.append(u'{}'.format(doc.to_dict()['Alzheimer_RiskLevel_Reports']))
            
            print(AlzheimerRiskProfile_Report)

            tempList = []
            tempList.append(alzheimerRiskProfile_Api())

            db.collection("patients").document(key).update({"Alzheimer_RiskLevel_Reports": tempList})

        else:
            print("They are different...")

    return render(request, 'risk-profiles.html', {
        "patientsList" : patientsList,
        
        })


def userProfiling(request):
     return render(request, 'user-profiling.html', {
         "patientsList" : patientsList,
    })




def dataAggregator(request):
    return render(request, 'data-aggregator.html', {
         "patientsList" : patientsList,
    })


def dataAggregatorPost(request):
    import csv


    patientID = request.POST.get('patient_from_dropdown')
    patientId_string = str(patientID)
    docs = db.collection("patients").get()

    for doc in docs:
        if (str(doc.to_dict()['PatientID']))==patientId_string:

            patient_FirstName = u'{}'.format(doc.to_dict()['FirstName'])
            patient_lastName = u'{}'.format(doc.to_dict()['LastName'])

            name = patient_FirstName + "_" + patient_lastName + "_" + "dataset.csv"

         

            with open(name, mode='w') as employee_file:
                employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                employee_writer.writerow([  u'{}'.format(doc.to_dict()['Alzheimer_RiskLevel_Reports'])    ])


        else:
            print("They are different...")



    


    return render(request, 'data-aggregator.html', {
         "patientsList" : patientsList,
         "result" : "Dataset generated successfully!"
    })

