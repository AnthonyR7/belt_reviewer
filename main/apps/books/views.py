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
        sameBook = Book.objects.filter(title = request.POST['title'],author = request.POST['author'])
        if not sameBook:
            print "not the same book and new one will be created"
            a_book = Book.objects.create(title = request.POST['title'],author = request.POST['author'])
            create_review = Review.objects.create(book= a_book, writter = user, review = request.POST['desc'], rating = num)
            reviewForBook = a_book.reviews.all()#reverse-lookup
            context = {
                "title" : a_book.title,
                "author" : a_book.author,
                "reviews" : reviewForBook
            }
        else:
            print "Same book will be used, but not created"
            use_same_book = Book.objects.get(title = request.POST['title'],author = request.POST['author'])
            create_review = Review.objects.create(book = use_same_book , writter = user, review = request.POST['desc'], rating = num)
            reviewForBook = use_same_book.reviews.all()
            context = {
                "title" : use_same_book.title,
                "author" : use_same_book.author,
                "reviews" : reviewForBook
            }
    return render(request,"belt_reviewer/display_books.html", context)
def user_info(request):
    user = User.objects.get(id = request.session["client"]['id'])
    userReview = user.reviews.all()
    context = {
        "alias" : user.alias,
        "name" : user.full_name,
        "num" : len(user.reviews.all()),
        "email" : user.email
    }
    return render(request, "belt_reviewer/user_reviews.html", context)
def home(request):
    user = User.objects.get(id = request.session['client']['id'])
    context = {
        "name" : user.alias,
        # "id"   : user.id
    }
    return render(request, "belt_reviewer/dashboard.html", context)
def remove(request):
    user = User.objects.get(id = request.session["client"]['id'])
    
