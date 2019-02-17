from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.quiz,name = 'quiz'),
    path('check/',views.check,name = 'check'),
    path('result/',views.result,name = 'result'),
    path('detail/',views.detail,name = 'detail'),
    path('upload/',views.upload,name="upload")
]