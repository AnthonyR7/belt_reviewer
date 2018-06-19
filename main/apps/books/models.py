from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def reg_validator(self, postData):
        print postData
        errors = []
        if (postData.get('full_name', False)) == False:
            print postData
            errors.append('Name must not be empty!')

        if (postData.get('full_name', False)) == True:
            if not postData.get('full_name').isalpha():
                errors.append("Your name can't have numbers!")

        if (postData.get('Alias', False)) == False:
            errors.append( "Alias must not be empty!")

        if (postData.get('Email', False)) == False:
            errors.append( "Email must not be empty!")

        if (postData.get('password', False)) == False:
            errors.append("Password must not be empty!")

        elif (postData.get('password', False)) == True:
            if len(postData['password']) < 8:
               errors.append( "Password must be at least 8 characters in lengh.")

        if postData.get('password') != postData.get('confirm_password'):
            errors.append("Pass words do NOT match!")

        if (postData.get('email', False)) == True:
            if not EMAIL_REGEX.match(postData.get('email')):
                errors.append("Invalid Email Address!")

        return errors
    # def log_validator(self, postData):

class User(models.Model):
    full_name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password =models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
class Books(models.Model):
    item = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
class UsersBooks(models.Model):
    student = models.ForeignKey(User)
    reading = models.ForeignKey(Books)
