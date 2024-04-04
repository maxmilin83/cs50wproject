from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate,get_user_model
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .forms import UserRegistrationForm,UserLoginForm,UserUpdateForm,SetPasswordForm,PasswordResetForm 
from .decorators import user_not_authenticated

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.db.models.query_utils import Q



# Create your views here.
def activate(request,uidb64,token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        User = None

    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"You activated your account")
        return redirect("login")
    else:
        messages.error(request,"Activation link is invalid")

    return redirect("index")




def activateEmail(request,user,to_email):
    mail_subject = "Activate user account"
    message = render_to_string("template_activate_account.html",{
        'user':user.username,
        'domain':get_current_site(request),
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol':'https' if request.is_secure() else 'http'
    })


    email = EmailMessage(mail_subject,message,to=[to_email])
    if email.send():
        messages.success(request, f"Dear {user},please go to your email {to_email} and click the activate link \
                        to complete registration")
    else:
        messages.error(request,f'Problem sending email to {to_email} check if you typed it correctly')

@user_not_authenticated
def register(request):    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            activateEmail(request,user,form.cleaned_data.get('email'))

            return redirect("index")
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


def profile(request,username):
    if request.method == "POST":
        user=request.user
        form = UserUpdateForm(request.POST,instance=user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request,f"{user_form.username}, Your profile has been updated!")
            return redirect("profile",user_form.username)
        

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(request,"users/profile.html",{"form":form})
    

    return redirect()


@login_required
def password_change(request):
    user = request.user
    if request.method == "POST":
        print("test")
        form = SetPasswordForm(user,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your password has been changed")
            return redirect("login")
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)

    form  = SetPasswordForm(user)
    return render(request,'password_reset_confirm.html',{'form':form})


@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        "Password reset instructions sent, if provided email exists"
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('index')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(request,'password_reset_confirm.html',{'form':form})



def passwordResetConfirm(request,uidb64,token):

    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        User = None

    if user is not None and account_activation_token.check_token(user,token):
        if request.method == 'POST':
            form = SetPasswordForm(user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Password reset")
                return redirect("login")
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)

        form = SetPasswordForm(user)


        return render(request,'password_reset_confirm.html',{'form':form})
    else:
        messages.error(request,"Link is expired")
    
    messages.error(request,"Something went wrong redirecting to home page")
    return redirect("index")
