from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from firstapp import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from email.message import EmailMessage
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):

    if request.method == 'POST':                #Nhan thong tin nguoi dung dang ky
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exits! Please try some other username")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('home')

        if len(username) < 6:
            messages.error(request, "Username must be at least 6 characters long.")
            return redirect('home')

        if password1 != password2:
            messages.error(request, "Password didn't match!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must be only contain numbers and letters!")
            return redirect('home')

        myuser = User.objects.create_user(username, email, password1)    #Du yeu cau, tao user moi
        myuser.first_name = firstname
        myuser.last_name = lastname 
        myuser.is_active = True                                           #Dat trang thai la active          

        myuser.save()

        messages.success(request, "Your account has been successfully created.")
    

        return redirect('signin')


    return render(request, "authentication/signup.html")

def signin(request):

    if request.method == 'POST':    

        username = request.POST['username']
        password1 = request.POST['password1']

        user = authenticate(username=username, password=password1)          #Kiem tra thong tin duoc nhan vao

        if user is not None:                                                #Neu co trong database
            login(request, user)
            firstname = user.first_name
            return render(request, "authentication/index.html", {"firstname": firstname})
        
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')


    