from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User

class Quiz(models.Model):  
    content = models.TextField()
    category = models.CharField(max_length=5)
    example1 = models.CharField(max_length=50)
    example2 = models.CharField(max_length=50)
    example3 = models.CharField(max_length=50)
    source = models.TextField()
    ans = models.CharField(max_length=50)

class History(models.Model):
    count = models.IntegerField(default=0)
    set = JSONField() 

class Challenge(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rank = models.BooleanField(default=False)
    rightcnt = models.IntegerField(default=0)
    set = JSONField() 
