from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^back$', views.back),
    url(r'^add_books$', views.add_books),
    url(r'^submit_new_books$', views.add_books_and_reviews),
    url(r'^user_info/$', views.user_info),
    url(r'^go_add_and_review$', views.add_books),
    url(r"^home$", views.home),
    url(r'^delete_review$', views.remove)
]
