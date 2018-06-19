from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = []
        if len(postData['full_name']) < 1:
            errors.append('Name must not be empty!')
        if len(postData['alias']) < 1:
            errors.append( "Alias must not be empty!")
        if len(postData['email']) < 1:
            errors.append( "Email must not be empty!")
        if len(postData['password']) < 8:
            errors.append( "Password must be at least 8 characters in lengh.")
        if postData['password'] != postData['confirm_password']:
            errors.append("Pass words do NOT match!")
        if not postData['full_name'].isalpha():
            errors.append("Your name can't have numbers!")
        if len(postData['email']) > 1:
            if not EMAIL_REGEX.match(postData['email']):
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
