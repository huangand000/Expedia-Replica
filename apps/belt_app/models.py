from __future__ import unicode_literals
import re
from datetime import *
import bcrypt
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NUMBER_REGEX = re.compile(r'^[a-zA-Z]+$')
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors ={}
        if postData['name'] and postData['username'] and postData['password'] and postData['confirm']:
            if len(postData['name']) < 3:
                errors['name'] = "Name must have more than 3 characters"
            if len(postData['username']) < 3:
                errors['username'] = "Username must have more than 3 characters"
            if postData['password'] != postData['confirm']:
                errors['pw_match'] = "Password must match"
            if len(postData['password']) < 8:
                errors['password'] = "Password should be at least 8 characters"
            if User.objects.filter(username=postData['username']):
                errors['username'] = "Username taken"
        else:
            errors['post'] = ""
        return errors

    def login_validator(self, postData):
        errors ={}
        if not User.objects.filter(username=postData['username']):
            errors['username'] = "No Username Found"
        else:
            if not bcrypt.checkpw(postData['loginpw'].encode(), User.objects.filter(username=postData['username'])[0].password.encode()):
                errors['password'] = 'Username and Password dont match'
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = UserManager()

class Travel(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    user = models.ForeignKey(User, related_name="travel_to")
    users = models.ManyToManyField(User, related_name="travels")