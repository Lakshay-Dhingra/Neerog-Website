from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from . import tokens
from . import authenticate

from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# render syntax:
# return render(request,'page.html',context_var_dictionary)

def logout(request):
    auth.logout(request)
    return redirect("/")

def signin(request):
    return render(request,'accounts/signin.html')

def signup(request):
    return render(request,'accounts/signup.html')

def login(request):
    email=request.POST['email'];
    password=request.POST['password'];

    #Validation checks
    if(len(email)>254):
        messages.info(request,"Invalid Email! Email can't have more than 254 characters.")
    elif(len(email)<8):
        messages.info(request,"Invalid Email! Email must contain atleast 8 characters")
    elif(len(password)<8):
        messages.info(request,"Invalid Password! Password must contain atleast 8 characters.")
    elif(len(password)>50):
        messages.info(request,"Invalid Password! Password can't have more than 50 characters.")
    else:
        if(authenticate.login(request, email, password)):
            messages.info(request,'Login Successful!')
            return redirect("/")
        else:
            messages.info(request,"Wrong Email or password!")
    return redirect("/accounts/signin")

def register(request):
    user_type=request.POST['user_type']
    name=request.POST['name']
    password=request.POST['password']
    password2=request.POST['password2']
    email=request.POST['email']
    # phone=request.POST['phone']

    #Validation checks
    if(len(user_type)==0):
        messages.info(request,"Please Select a Valid User Type!")
    if(len(name)==0):
        messages.info(request,"Invalid Name! Name can't be empty.")
    elif(len(name)>200):
        messages.info(request,"Invalid Name! Name can't have more than 200 characters.")
    elif(len(email)==0):
        messages.info(request,"Invalid Email! Email can't be empty.")
    elif(len(email)>254):
        messages.info(request,"Invalid Email! Email can't have more than 254 characters.")
    # elif(len(phone)==0):
    #     messages.info(request,"Invalid Phone Number! Phone Number can't be empty.")
    # elif(len(phone)>10):
    #     messages.info(request,"Invalid Phone Number! Phone Number can't have more than 10 characters.")
    elif(len(password)<8):
        messages.info(request,"Invalid Password! Password can't have less than 8 characters.")
    elif(len(password)>50):
        messages.info(request,"Invalid Password! Password can't have more than 50 characters.")
    elif(password != password2):
        messages.info(request,"Invalid Password! Confirm Password and Password fields doesn't match.")
    
    else:
        if(authenticate.hasRegisteredEmail(email)):
            messages.info(request,'This Email is already registered!')
        # elif(authenticate.hasRegisteredPhone(phone)):
        #     messages.info(request,'This Phone is already registered!')
        else:
            if(authenticate.register(name, user_type, password, email)):
                messages.info(request,'Registeration Successful! You will recieve a verification mail for your account shortly.')
                return redirect("/")
            else:
                messages.info(request,"Registeration Failed!")
    return redirect("/accounts/signup")

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and tokens.account_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.info(request,"Thanks for your email confirmation. You can login to your account now.")
        return redirect("/accounts/signin")
    else:
        messages.info(request,"Invalid Activation link!")
        return redirect("/accounts/signup")
