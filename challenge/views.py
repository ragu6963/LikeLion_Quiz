from django.shortcuts import render,redirect
from quiz.models import Quiz, History,Challenge
from django.contrib.auth.models import User
from django.contrib import auth


def start(request):
    return render(request, 'ch_start.html')

def quiz(request):    
    if request.method =="POST":
        challenge_id = request.POST['challenge']
        quiz_id = request.POST['quiz']
        select = request.POST['select']

        challenge = Challenge.objects.get(id = challenge_id) 
        quiz = Quiz.objects.get(id = quiz_id) 
        result ="" 
        

        if select == quiz.ans:
            result = "O"
            challenge.set[quiz_id] = result
            challenge.rightcnt = challenge.rightcnt+1
        else:
            result = "X"
            challenge.set[quiz_id] = result
            dic={}
            for key,value in challenge.set.items():
                dic[key] = value
            return render(request, 'ch_result.html',{"challenge":challenge,"dic":dic})

        quiz = Quiz.objects.all()
        
        for q in challenge.set.keys():
            quiz = quiz.exclude(id = q) 

        challenge.save()
        quiz = quiz.order_by('?').first()

        return render(request,'ch_quiz.html',{"quiz":quiz,"challenge":challenge})

    if request.method =="GET": 
        challenge = Challenge() 
        quiz = Quiz.objects.all()
        quiz = quiz.order_by('?').first()  
        challenge.set={} 
        challenge.save()
        return render(request,'ch_quiz.html',{"quiz":quiz,"challenge":challenge})

