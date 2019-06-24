from django.shortcuts import render, HttpResponse, redirect


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
    return redirect("/registration")




# ------------------------------------------------------------------
# Login
# ------------------------------------------------------------------

def login(request):
    return render(request, "login_and_registration_app/login.html")

def login_process(request):
    return redirect("/news")




# ------------------------------------------------------------------
# News
# ------------------------------------------------------------------

def news(request):
    return render(request, "login_and_registration_app/news.html")




# ------------------------------------------------------------------
# Investments
# ------------------------------------------------------------------
def investments(request):
    return render(request, "login_and_registration_app/investments.html")

def investments_process(request):
    return redirect("/user/investments")


# ------------------------------------------------------------------
# add/find Chatrooms
# ------------------------------------------------------------------
def add_chatroom(request):
    return render(request, )

def add_chatroom_process(request):
    return redirect("/user/chatroom/add")







