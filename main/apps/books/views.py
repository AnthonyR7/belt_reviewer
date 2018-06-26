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
        conformed_user = User.objects.get(email = request.POST['confirm_email'])
        request.session['client'] = {
            "id" : conformed_user.id
        }

        user = User.objects.get(id = request.session['client']['id'])
        context = {
            "name" : user.alias,
            # "id"   : user.id
        }
        return render(request, "belt_reviewer/dashboard.html",context)
    return redirect('/')
def back(request):
    del request.session['client']
    return redirect('/')

def add_books(request):
    return render(request,"belt_reviewer/create_books.html")

def add_books_and_reviews(request):
    errors = Book.objects.validator(request.POST)
    if len(errors):
        for words in errors:
            messages.error(request, words)
            return redirect("/add_books")
    else:
        user = User.objects.get(id = request.session["client"]['id'])
        num = request.POST.get('rate',None)
        a_book = Book.objects.create(title = request.POST['title'],author = request.POST['author'])
        create_review = Review.objects.create(book= a_book, writter = user, review = request.POST['desc'], rating = num)
        reviewForBook = Review.objects.get(book = a_book )
        context = {
            "title" : a_book.title,
            "author" : a_book.author,
            "reviews" : reviewForBook.review
        }
    return render(request,"belt_reviewer/display_books.html", context)
