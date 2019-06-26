from django.shortcuts import render, HttpResponse, redirect
from .models import User, Chat, Message, Stock
from django.contrib import messages
import bcrypt
import datetime
import re


# ------------------------------------------------------------------
# Home
# ------------------------------------------------------------------

def home(request):
    return render(request, "login_and_registration_app/home.html")




# ------------------------------------------------------------------
# Registration
# ------------------------------------------------------------------

def registration(request):
    return render(request, "login_and_registration_app/registration.html")

def registration_process(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/registration')
    else:
        DBfirst_name = request.POST["first_name"]
        DBlast_name = request.POST["last_name"]
        DBemail = request.POST["email"]
        pw_to_hash = request.POST["password"]
        DBpassword = bcrypt.hashpw(pw_to_hash.encode(), bcrypt.gensalt())
        DBpassword = DBpassword.decode()
        new_user = User.objects.create(DBfirst_name=DBfirst_name, DBlast_name=DBlast_name, DBemail=DBemail, DBpassword=DBpassword)
        request.session['userid'] = new_user.id
        request.session['first_name'] = new_user.DBfirst_name
        request.session['isloggedin'] = True
        request.session.modified = True
        return redirect("/news")




# ------------------------------------------------------------------
# Login
# ------------------------------------------------------------------

def login(request):
    return render(request, "login_and_registration_app/login.html")

def login_process(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        messages.error(request, request.POST["emailLogin"], "holdLoginEmail")
        return redirect('/login')
    else:
        current_user = User.objects.get(DBemail = request.POST['emailLogin'])
        request.session['userid'] = current_user.id
        request.session['isloggedin'] = True
        request.session['first_name'] = current_user.DBfirst_name
        return redirect("/news")


# ------------------------------------------------------------------
# Login
# ------------------------------------------------------------------

def logout(request): 
    request.session['isloggedin'] = False   #Flip boolean to logout
    return redirect ("/")

# ------------------------------------------------------------------
# News
# ------------------------------------------------------------------

def news(request):
    print (request.session['isloggedin'])
    if request.session['isloggedin'] == False :
        print ("hack")
        return render(request, "login_and_registration_app/news.html")
        # return redirect("/")
    else: 
        return render(request, "login_and_registration_app/news.html")




# ------------------------------------------------------------------
# Investments
# ------------------------------------------------------------------
def investments(request):
    return render(request, "login_and_registration_app/investments.html")

def investments_process(request):
    return redirect("/investments")


# ------------------------------------------------------------------
# Communities 
# ------------------------------------------------------------------
def community(request):
    return render(request, "login_and_registration_app/community.html")


def add_chatroom_process(request):
    return redirect("/chatroom/add")

def view_chatroom(request, chatroomid):
    context = {
        'chatroomid': chatroomid,
    }
    return render(request, "login_and_registration_app/chatroom.html", context)

def find_chatroom_process(request):
    return redirect("/find_chatroom/id")

# ------------------------------------------------------------------
# Login
# ------------------------------------------------------------------

def logout(request):
    request.session.clear()
    request.session['isloggedin'] = False
    return redirect('/')
