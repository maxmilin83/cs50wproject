from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .forms import UserRegistrationForm,UserLoginForm
from .decorators import user_not_authenticated



# Create your views here.

@user_not_authenticated
def register(request):    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,f"New account created {user.username}")

            return redirect("/")
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)

    else:
        form = UserRegistrationForm()
    
    return render(request,"users/registration.html",{"form":form})


@login_required
def custom_logout(request):
    logout(request)
    messages.info(request,"Logged out successfully")
    return redirect("index")

@user_not_authenticated
def custom_login(request):    
    if request.method == "POST":
        form = UserLoginForm(request=request,data=request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
            )
            if user is not None:
                login(request,user)
                messages.success(request,f"Hello <b>{user.username}</b> You have been logged in")
                return redirect("index")
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)

    
    form = UserLoginForm()

    return render(request,"users/login.html",{"form":form})