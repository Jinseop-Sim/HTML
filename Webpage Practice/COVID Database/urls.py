from django.contrib import admin
from django.urls import path
from myApp import views

urlpatterns = [
    path('', views.initial_page),
    path('index/', views.display, name='index'),
    path('stud/', views.insert_stud),
    path('index/prof/', views.insert_prof),
    path('index/count/', views.insert_counties),
    path('index/covid/', views.insert_covid)
]
