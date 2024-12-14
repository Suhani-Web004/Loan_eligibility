from django.shortcuts import render ,  redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from Eloan.models import *
from Eloan.models import NewUser
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password  # Import check_password
from .models import *
from django.http import HttpResponse, JsonResponse
import joblib
import numpy as np
import pandas as pd



# Create your views here.
def wellcome(request):
    return render(request, 'index.html')

def signin(request):
    value = None

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Hash the user's password
        hashed_password = make_password(password)

        try:
            newuser = NewUser.objects.create(username=username, email=email, password=hashed_password)
            newuser.save()
            value = 3  # User created successfully
            request.session['username']=newuser.username
        except IntegrityError as e:
            if 'UNIQUE constraint failed: carapp_newuser.email' in str(e):
                value = 2  # Email already exists
            else:
                value = 1
                
    else:
        return render(request, 'signin.html')

    context = {'value': value}
    return render(request, 'signin.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = NewUser.objects.get(username=username)
            if check_password(password, user.password):
                # Password matches
                request.session['username'] = user.username
                res = render(request, 'home.html')
            else:
                # Password doesn't match
                LoginError = "Invalid Username or Password.."
                res = render(request, 'login.html', {'LoginError': LoginError})
        except NewUser.DoesNotExist:
            # User not found
            LoginError = "Invalid Username or Password.."
            res = render(request, 'login.html', {'LoginError': LoginError})
    else:
        if 'username' in request.session.keys():
            res = render(request, 'home.html')
        else:
            res = render(request, 'login.html')
    return res


def home(request):
    if 'username'  in  request.session.keys():
        return render(request,'home.html')
    else:
        return HttpResponseRedirect('/login')




model = joblib.load('ML_model/loanprediction_model.sav')
COLUMNS = [
    ' no_of_dependents', 
    ' income_annum',
    ' loan_amount',
    ' loan_term',
    ' cibil_score',
    ' residential_assets_value',
    ' luxury_assets_value',
    ' bank_asset_value',
    ' education_ Not Graduate',
    ' self_employed_ Yes'
]

    # Create your views here.
def prediction(request):
    if request.method == 'POST':
        feature = pd.DataFrame(np.zeros((1,10)), columns=COLUMNS)
        for x in COLUMNS[:-2]:
            value = request.POST.get(x.strip(),'')
            if value:
                try:
                    feature[x] = float(value)
                except ValueError:
                    print(f"Invalid value for {x}: {value}")

        self_emp = request.POST.get('self_employed','')
        ed = request.POST.get('education','')
        if self_emp:
            try:
                feature.iloc[1:-1] = float(value)
            except ValueError:
                print(f"Invalid value for self employed")
        if ed:
            try:
                feature.iloc[1:-2] = float(value)
            except ValueError:
                print(f"Invalid value for education")

        print(feature)
        try:
            prediction = model.predict(feature)
            print(f"Prediction: {prediction[0]}")
            return render(request, 'prediction.html', {'prediction': 'Eligible' if prediction[0] else "Not Eligible"})
        except Exception as e:
            print(f"Error during prediction: {e}")
            return render( request, 'home.html', {'error': str(e)})

    return render(request, 'prediction.html')

    
def team(request):
    if 'username'  in  request.session.keys():
        return render(request,'team.html')
    else:
        return HttpResponseRedirect('/login')

def logout(request):
    if 'username'  in  request.session.keys():
        request.session.pop('username')
    return HttpResponseRedirect('login')