from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
from django.core.exceptions import ObjectDoesNotExist
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = []
        if len(postData['full_name']) <1:
            errors.append('Name must be not empty!')
        if len(postData['full_name']) > 1:
            if (postData['full_name'].isalpha()) != True:
                errors.append("No numbers in your name please!")

        if len(postData['alias']) < 1:
            errors.append( "Alias must not be empty!")

        if len(postData['email']) < 1:
            errors.append( "Email must not be empty!")

        if len(postData['password']) < 5:
            errors.append( "Pass word must be at least 5 characters in lengh.")

        if postData['password'] != postData['confirm_password']:
            errors.append("Pass words do NOT match!")

        if len(postData['email']) > 1:
            if not EMAIL_REGEX.match(postData['email']):
                errors.append("Invalid Email Address!")
        return errors
    def log_validator(self, postData):
        missing = []
        if len(postData["confirm_email"]) < 1:
            missing.append("Email is needed!")
        if len(postData["login_password"]) < 1:
            missing.append("Login Password is needed!")
        else:
            try:
                confirm_email = postData["confirm_email"]
                confirm_password = postData["login_password"]
                searched_user = User.objects.get(email = confirm_email)
                request.session['client'] = searched_user.alias
                if not bcrypt.checkpw(confirm_password.encode(), searched_user.password.encode()):
                    missing.append("Incorrect password")
            except ObjectDoesNotExist:
                missing.append("Account not in database.")
        return missing

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
