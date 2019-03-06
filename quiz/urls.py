from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('start/',views.start,name = 'start'),
    path('quiz/',views.quiz,name = 'quiz'), 
    path('detail/',views.detail,name = 'detail'),  
]