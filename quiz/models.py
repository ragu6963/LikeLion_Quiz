from django.db import models
from jsonfield import JSONField



class Quiz(models.Model):  
    content = models.TextField()
    category = models.IntegerField()
    example1 = models.CharField(max_length=50)
    example2 = models.CharField(max_length=50)
    example3 = models.CharField(max_length=50)
    source = models.TextField()
    ans = models.CharField(max_length=50)
 

class History(models.Model):
    excl = models.TextField()
    qu = JSONField()


