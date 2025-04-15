from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [
   path('', views.health_and_csrf_token),
   path('api/v1/dynamic-form/', views.dynamic_form),
   path('error_logs', views.error_log),
] 

# change to silk thread dev forms