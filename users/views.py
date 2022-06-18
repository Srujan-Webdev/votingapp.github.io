from django.contrib.messages.api import debug
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import CreateUserForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import datetime
import csv
from django.core.mail import send_mail
from .models import Profile
import uuid
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages,auth
from django.contrib.auth import login, authenticate
from django.core.mail import EmailMessage
from django.template.loader import get_template

# Create your views here.

def register(request):

    if request.method == "POST":
        #form = UserCreationForm(request.POST)
        form = CreateUserForm(request.POST)
        if form.is_valid():

            email = request.POST.get('email')
            username = request.POST.get('username')
            password1 = request.POST.get('password1')

            #Restricting user to take only 1 email
            # user_email_obj = User.objects.filter(email=email).first()
            # if user_email_obj is not None:
            #     messages.success(request, "Email already taken, please try with another email")
            #     return redirect("register")

            #Storing variables in session sothat we can these in any function
            request.session['email'] = email
            request.session['username'] = username

            user_obj = form.save()
            #return redirect('/')
            #or
            #return redirect('index')

            # user_obj = User.objects.create(username=username,email=email)
            # user_obj.set_password(password1)
            # user_obj.save()

            #Creating Profile for "authentication token" to the user
            auth_token=str(uuid.uuid4())
            auth_token_admin=str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj,auth_token=auth_token,auth_token_admin=auth_token_admin)
            profile_obj.save()
            
            send_mail_after_registration(email,auth_token)
            send_mail_after_registration_admin_verification(email,username,auth_token_admin)

            messages.info(request, "Your Registration successful, We have sent you an Email please verify it" )

            return redirect('register')
            #return redirect('login')
    else:
        #form = UserCreationForm()
        form = CreateUserForm()

    context = {
        
        'form':form
        
        }    

    return render(request, 'users/register.html', context)


def login(request):

    if request.method == "POST":
        #form = UserCreationForm(request.POST)
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user_obj = User.objects.filter(username=username).first()
            if user_obj is None:
                messages.success(request, "user not found")
                return redirect("login")

            profile_f_obj = Profile.objects.filter(user=user_obj).first()
            if not profile_f_obj.is_verified:
                messages.error(request, "You can't login, please verify your email which we sent to you")
                return redirect("login")
            if not profile_f_obj.is_admin_verified:
                messages.error(request, "You can't login untill 'admin' approves you")
                return redirect("login")            

            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("/")
            else:
                messages.error(request,"Invalid username or password.")

            return redirect('/')
    else:
        #form = UserCreationForm()
        form = AuthenticationForm()

    context = {
        
        'form':form
        
        }    

    return render(request, 'users/login.html', context)
 
def send_mail_after_registration(email,token):
    
    #print("----- welcome_mail_after_registration -----")    
    send_mail(
    '{}'.format('Voting App ---> Your account needs to be verified'),#subject
    'Click the link to verify the account http://127.0.0.1:8000/users/verify/{}'.format(token),
    settings.EMAIL_HOST_USER,#from mail
    ['{}'.format(email)],#to mail list
    fail_silently=False,#will throw error if mail has not sent
)

def send_mail_after_registration_admin_verification(email,username,token):
    
    #print("----- welcome_mail_after_registration -----")    
    send_mail(
    '{}'.format('Voting App ---> Admin approval needs to be done'),#subject
    'Click the link to verify this account(email:{},username:{}) http://127.0.0.1:8000/users/verify_admin/{}'.format(email,username,token),
    settings.EMAIL_HOST_USER,#from mail
    ['{}'.format(settings.EMAIL_HOST_USER)],#to mail list
    fail_silently=False,#will throw error if mail has not sent
)

def verify(request,auth_token):

    profile_filter_obj = Profile.objects.filter(auth_token=auth_token).first()

    if profile_filter_obj:
        if profile_filter_obj.is_verified:
            messages.info(request, "Your email has already been verified, if you still can't login you need to wait untill 'admin' approves")  
            return redirect('login')
        profile_filter_obj.is_verified=True
        profile_filter_obj.save()

        messages.info(request, "Hurray!!!!! Your Email has been verified, now you can login after 'admin' approves you")

    #Welcome mail
    #session_email=request.session['email']
    #session_username=request.session['username']
    #welcome_mail_after_registration(session_email,session_username)
       
    return redirect('login')


def verify_admin(request,auth_token):

    profile_filter_obj_auth_admin = Profile.objects.filter(auth_token_admin=auth_token).first()

    if profile_filter_obj_auth_admin:
        if profile_filter_obj_auth_admin.is_admin_verified:
            messages.info(request, "This Email/Username has already been verified from 'admin' side")  
            return redirect('login')
        profile_filter_obj_auth_admin.is_admin_verified=True
        profile_filter_obj_auth_admin.save()

        messages.info(request, "Hurray!!!!! this Email/Username has been verified now from 'admin' side, you can request the 'user' to login after he/she verifies their email from their end")

    #Welcome mail
    session_email=request.session['email']
    session_username=request.session['username']
    welcome_mail_after_registration(session_email,session_username)
    mail_confirmation_to_admin(session_email,session_username)
       
    return redirect('login')


def welcome_mail_after_registration(email,username):
    
    subject='{}'.format('Welcome to Voting Application!!!!!!!')
    body_html_message = get_template('users/mail.html').render({'username': username})
    from_email=settings.EMAIL_HOST_USER
    to_email=['{}'.format(email)]

    send_mail = EmailMessage(subject,body_html_message,from_email,to_email)
    send_mail.content_subtype = "html"  # Main content is now text/html
    send_mail.send()

    #send_mail(
    '{}'.format('Welcome to Todo Application!!!!!!!'),#subject
    'Your Email verification is successful....... :), now you can feel the \"Todo\" application by logging into it, Your username is {}'.format(username),#Body of the mail
    'srs.webdev.2@gmail.com',#from mail
    ['{}'.format(email)],#to mail list
    fail_silently=False,#will throw error if mail has not sent)

def mail_confirmation_to_admin(email,username):
    
    send_mail(
    '{}'.format('Voting App ---> Admin approval completed'),#subject
    'Admin approval completed for this Email: {},Username: {}'.format(email,username),#Body of the mail
    settings.EMAIL_HOST_USER,#from mail
    ['{}'.format(settings.EMAIL_HOST_USER)],#to mail list
    fail_silently=False,#will throw error if mail has not sent
    )


