from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .models import User, Chat, Message, Stock, Stock_Price
from django.contrib import messages
import bcrypt
import datetime
import re

from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from social_django.models import UserSocialAuth

from faker import Factory, Faker
from django.http import JsonResponse
from django.conf import settings

from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import (
	SyncGrant,
	ChatGrant
)
# Stocks
import pandas_datareader.data as web
from pandas_datareader._utils import RemoteDataError as error #handle error for non existent stock
from datetime import datetime
from datetime import timedelta


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
			messages.error(request, value, extra_tags=key)
		return redirect('/registration')
	else:
		DBfirst_name = request.POST["first_name"]
		DBlast_name = request.POST["last_name"]
		DBemail = request.POST["email"]
		pw_to_hash = request.POST["password"]
		has_usable_password = True
		DBpassword = bcrypt.hashpw(pw_to_hash.encode(), bcrypt.gensalt())
		DBpassword = DBpassword.decode()
		DBusername = DBfirst_name[0] + DBlast_name
		new_user = User.objects.create(
			DBfirst_name=DBfirst_name, DBlast_name=DBlast_name, DBemail=DBemail, DBpassword=DBpassword, has_usable_password=has_usable_password, DBusername=DBusername)
		request.session['userid'] = new_user.id
		request.session['first_name'] = new_user.DBfirst_name
		request.session['username'] = new_user.DBusername
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
			messages.error(request, value, extra_tags=key)
		messages.error(request, request.POST["emailLogin"], "holdLoginEmail")
		return redirect('/login')
	else:
		current_user = User.objects.get(DBemail=request.POST['emailLogin'])
		request.session['userid'] = current_user.id
		request.session['isloggedin'] = True
		request.session['first_name'] = current_user.DBfirst_name
		request.session['username'] = current_user.DBusername
		return redirect("/news")



def settings_page(request):
	if 'isloggedin' not in request.session or  request.session['isloggedin'] == False:
		print("hack")
		return redirect("/")
	else:
		user = request.User

		try:
			github_login = user.social_auth.get(provider='github')
		except UserSocialAuth.DoesNotExist:
			github_login = None

		try:
			facebook_login = user.social_auth.get(provider='facebook')
		except UserSocialAuth.DoesNotExist:
			facebook_login = None

		can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

		return render(request, 'login_and_registration_app/settings_page.html', {
			'github_login': github_login,
			'facebook_login': facebook_login,
			'can_disconnect': can_disconnect
		})

def password(request):
	if 'isloggedin' not in request.session or  request.session['isloggedin'] == False:
		print("hack")
		return redirect("/")
	else:
		if request.User.has_usable_password():
			PasswordForm = PasswordChangeForm
		else:
			PasswordForm = AdminPasswordChangeForm

		if request.method == 'POST':
			form = PasswordForm(request.User, request.POST)
			if form.is_valid():
				form.save()
				update_session_auth_hash(request, form.User)
				messages.success(request, 'Your password was successfully updated!')
				return redirect('password')
			else:
				messages.error(request, 'Please correct the error below.')
		else:
			form = PasswordForm(request.User)
		return render(request, 'login_and_registration_app/settings_page.html', {'form': form})

# ------------------------------------------------------------------
# Logout
# ------------------------------------------------------------------

def logout(request):
	request.session['isloggedin'] = False  # Flip boolean to logout
	return redirect("/")


# ------------------------------------------------------------------
# News
# ------------------------------------------------------------------
def news(request):
	if 'isloggedin' not in request.session or  request.session['isloggedin'] == False:
		print("hack")
		return redirect("/")
	else:
		return render(request, "login_and_registration_app/news.html")


# ------------------------------------------------------------------
# Investments
# ------------------------------------------------------------------
def investments(request):
	if 'isloggedin' not in request.session or  request.session['isloggedin'] == False:
		print("hack")
		return redirect("/login")
	else:
		# if "grabbed-stocks" not in request.session :
		pull_investments(request)
		user = User.objects.get(id=request.session["userid"])
		context = {
			"faang": Stock.objects.filter(users=None),
			"your_stocks" :user.watched_stocks.all()
		}
		return render(request, "login_and_registration_app/investments.html", context)

# Seach Bar Stock Lookup
def add_stock(request) :
	if 'isloggedin' not in request.session or  request.session['isloggedin'] == False:
		print("hack")
		return redirect("/login")
	else:
		user = User.objects.get(id=request.session["userid"])
		new_stock = yahoo_pull_API(request, request.POST["symbol"])
		user.watched_stocks.add(new_stock)  #add to user
		return redirect("/investments")
# ------------------------------------------------------------------
# Paper Stocks, "feature is currently unavailable"
# ------------------------------------------------------------------
def paper_stocks(request):
	return render(request, "login_and_registration_app/paper_stocks.html")


# ------------------------------------------------------------------
# Pull Yahoo Finance Data for FAANG Stocks
# ------------------------------------------------------------------
def yahoo_pull_API(request, symbol) :
    start = datetime.now() - timedelta(days=365)
    end = datetime.now()
    stock_exists = Stock.objects.filter(symbol=symbol).exists() #logic to not repeat stocks
    if not stock_exists :
        try :            #Validation for non existent stocks
            f = web.DataReader(symbol, 'yahoo', start, end, ).reset_index()
        except error :
            print ("ERROR")
            return False
        length = len(f) - 1
        adj_price = f['Adj Close'][length]
        date = f['Date'][length]
        new_stock = Stock.objects.create(symbol=symbol)
        new_stock_price = Stock_Price.objects.create(stock=new_stock, date=date, price=adj_price)
        return(new_stock)
    else :
        return False

def pull_investments(request):
	fang = ["FB", "AMZN", "AAPL", "NFLX", "GOOGL", "TSLA"]
	start = datetime.now() - timedelta(days=365)
	end = datetime.now()
	for x  in fang:
		stock_exists = Stock.objects.filter(symbol=x).exists()
		if not stock_exists :
			f = web.DataReader(x, 'yahoo', start, end, ).reset_index()
			length = len(f) - 1
			adj_price = f['Adj Close'][length]
			date = f['Date'][length]
			new_stock = Stock.objects.create(symbol=x)
			new_stock_price = Stock_Price.objects.create(stock=new_stock, date=date, price=adj_price)

def investments_process(request):
	if 'isloggedin' not in request.session or  request.session['isloggedin'] == False:
		print("hack")
		return redirect("/login")
	else:
		return redirect("/investments")



# ------------------------------------------------------------------
# Communities
# ------------------------------------------------------------------
def community(request):
	if 'isloggedin' not in request.session or  request.session['isloggedin'] == False:
		print("hack")
		return redirect("/login")
	else:
		return render(request, "login_and_registration_app/community.html")


def add_chatroom_process(request):
	if 'isloggedin' not in request.session or  request.session['isloggedin'] == False:
		print("hack")
		return redirect("/login")
	else:
		return redirect("/chatroom/add")


def view_chatroom(request, chatroomid):
	if 'isloggedin' not in request.session or  request.session['isloggedin'] == False:
		print("hack")
		return redirect("/login")
	else:
		context = {
			'chatroomid': chatroomid,
		}
		return render(request, "login_and_registration_app/chatroom.html", context)


def find_chatroom_process(request):
	if 'isloggedin' not in request.session or  request.session['isloggedin'] == False:
		print("hack")
		return redirect("/login")
	else:
		return redirect("/find_chatroom/id")

# ------------------------------------------------------------------
# Login
# ------------------------------------------------------------------


def logout(request):
	request.session.clear()
	request.session['isloggedin'] = False
	return redirect('/')


def token(request):
	user = request.session['username']
	return generateToken(user)


def generateToken(identity):
	# Get credentials from environment variables
	account_sid = settings.TWILIO_ACCT_SID
	chat_service_sid = settings.TWILIO_CHAT_SID
	sync_service_sid = settings.TWILIO_SYNC_SID
	api_sid = settings.TWILIO_API_SID
	api_secret = settings.TWILIO_API_SECRET

	# Create access token with credentials
	token = AccessToken(account_sid, api_sid, api_secret, identity=identity)

	print("*********")
	print(identity)
	print(token)

	# Create a Sync grant and add to token
	if sync_service_sid:
		sync_grant = SyncGrant(service_sid=sync_service_sid)
		token.add_grant(sync_grant)

	# Create a Chat grant and add to token
	if chat_service_sid:
		chat_grant = ChatGrant(service_sid=chat_service_sid)
		token.add_grant(chat_grant)

	# Return token info as JSON
	return JsonResponse({'identity': identity, 'token': token.to_jwt().decode('utf-8')})
