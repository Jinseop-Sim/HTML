from django.contrib import admin
from django.urls import path
from myApp import views

urlpatterns = [
    path('', views.display, name = 'index'),
    path('addrecord/', views.add_record, name = 'addrecord'),
    path('edit/<int:student_id>', views.edit_record, name = 'edit'),
    path('delete/<int:student_id>', views.delete_record, name = 'delete')
]
