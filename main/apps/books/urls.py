from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^back$', views.back),
    url(r'^add_books$', views.add_books),
    url(r'^submit_new_books$', views.add_books_and_reviews)
]
