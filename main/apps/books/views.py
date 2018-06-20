from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import *
def index(request):
    return render(request, "belt_reviewer/index.html")

def register(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors):
        for words in errors:
            messages.error(request, words)
    else:
        great =[]
        great.append("Successfully Registered, Thank you")
        for good in great:
            messages.success(request, good)
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print hash1
        User.objects.create(full_name = request.POST['full_name'],alias = request.POST['alias'], password = hash1, email = request.POST['email'])
    return redirect("/")

def login(request):
    errors = User.objects.log_validator(request.POST)
    if len(errors):
        for words in errors:
            messages.error(request, words)
    else:
        return render(request, "belt_reviewer/dashboard.html")
    return redirect('/')
def back(request):
    del request.session['client']
    return redirect('/')
