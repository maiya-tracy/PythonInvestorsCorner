from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
    def basic_validator(self, postData):     #bug with Duong last name(says it contains numbers)
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Invalid First Name! - Must be 2 characters long"
        if not (postData['first_name'].isalpha()) == True:
            errors['first_name'] = "Invalid First Name! - Can only contain alphabetic characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Invalid Last Name! - Must be 2 characters long"
        if not (postData['last_name'].isalpha()) == True:
            errors['last_name'] = "Invalid Last Name! - Can only contain alphabetic characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address!"
        emailAlreadyExists = User.objects.filter(DBemail=postData['email'])
        if (len(emailAlreadyExists))>0:
            errors['email'] = "Email already in system"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if postData['password'] != postData['password_confirm']:
            errors['confirmpw'] = "Password and Confirm Password must match"
        return errors
    def login_validator(self, postData):
        errors = {}
        print (postData)
        loginemailAlreadyExists = User.objects.filter(DBemail=postData['emailLogin']).exists()
        if not loginemailAlreadyExists :
            errors['loginemail'] = "Failure to log in"
            return errors
        user = User.objects.get(DBemail=postData["emailLogin"])
        pw_to_hash = postData["passwordLogin"]
        if not bcrypt.checkpw(pw_to_hash.encode(), user.DBpassword.encode()):
            errors['loginemail'] = "Failure to log in"
        return errors

class User(models.Model):
    DBfirst_name = models.CharField(max_length=255)
    DBlast_name = models.CharField(max_length=255)
    DBemail = models.CharField(max_length=255)
    DBpassword = models.CharField(max_length=255)
    friends = models.ManyToManyField("self")
    #chats = all chats the user is in
    #user_messages = all messages the user has sent
    #watched_stocks = all stocks the user is watching
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return f"<User object: {self.DBfirst_name} {self.DBlast_name} {self.DBemail} {self.DBpassword} ({self.id})>"

class ChatManager(models.Manager):
    def chatroom_validator():
        errors = {}
        return errors

class Chat(models.Model):
    DBtopic = models.CharField(max_length = 255)
    #chat_messages = all messages in the chat
    chat_users = models.ManyToManyField(User, related_name = 'chats')
    DBtype = models.BooleanField() #0 is a DM, 1 is a Forum
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ChatManager()

class MessageManager(models.Manager):
    def message_validator():
        errors = {}
        return errors

class Message(models.Model):
    DBmessage = models.TextField()
    chat = models.ForeignKey(Chat, related_name = 'chat_messages')
    sent_by = models.ForeignKey(User, related_name = 'user_messages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class StockManager(models.Manager):
    def stock_validator():
        errors = {}
        return errors

class Stock(models.Model):
    users = models.ManyToManyField(User, related_name = 'watched_stocks')
    symbol = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = StockManager()

class Stock_Price(models.Model) :
    stock = models.ForeignKey(Stock, related_name='prices')
    date = models.DateField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




