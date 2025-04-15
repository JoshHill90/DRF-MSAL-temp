from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [
   path("login",  views.auth_page, name="login"),
   path("getAToken", views.redirect_auth, name="getAToken"),
   path("validate_access", views.validate_access),
   path("validation", views.user_validation)
] 