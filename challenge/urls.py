from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('start/',views.start,name = 'ch_start'),
    path('quiz/',views.quiz,name = 'ch_quiz'), 
]