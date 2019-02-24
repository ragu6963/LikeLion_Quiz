from django.shortcuts import render,redirect
from .models import Quiz, History,Challenge
from django.contrib.auth.models import User
from django.contrib import auth
import csv,io
import operator

def index(request):
    challenge = Challenge.objects.all() 
    condition = ""
    if request.user.is_authenticated == True: 
        condition = "인증"

    dic = {}
    for data in challenge:
        key = data.user
        value = data.rightcnt
        if key in dic.keys():
            if dic[key] < value:
                dic[key] = value 
        else:
            dic[key] = value
    
    dic_list = sorted(dic.items(), key=lambda x: x[1], reverse=True) 
    

    return render(request,'index.html',{"challenge":challenge,"dic":dic_list,"condition":condition})

def start(request):
    return render(request, 'start.html')

def quiz(request):    
    if request.method =="POST":
        history_id = request.POST['history']
        history = History.objects.get(id = history_id)
        quiz = Quiz.objects.all()
        
        for ex in history.set.keys():
            quiz = quiz.exclude(id = ex) 
            
        history.save()
        quiz = quiz.order_by('?').first()

        return render(request,'quiz.html',{"quiz":quiz,"history":history})

    if request.method =="GET": 
        history = History() 
        quiz = Quiz.objects.all()
        quiz = quiz.order_by('?').first()  
        history.set={} 
        history.save()
        return render(request,'quiz.html',{"quiz":quiz,"history":history})

def check(request): 
    if request.method =="POST":
        history_id = request.POST['history']
        quiz_id = request.POST['quiz']
        history = History.objects.get(id = history_id)
        quiz = Quiz.objects.get(id = quiz_id)
        select = request.POST['select']
        result =""
        if select == quiz.ans:
            result = "정답"
            history.set[quiz_id] = result
        else:
            result = "오답"
            history.set[quiz_id] = result
        history.save()
        count = 0
        for key in history.set.keys():
            count= count+1
        return render(request,'check.html',{"history":history,"count":count,"result":result})

def result(request):
    if request.method =="POST":
        history_id = request.POST['history']
        history = History.objects.get(id = history_id)
        result ={}
        for key,value in history.set.items():
            result[key] = value

        count = 0

        for key in history.set.keys():
            count= count+1 

        return render(request,'result.html',{"history":history,"count":count,"result":result})

def detail(request):
    quiz_id = request.GET['quiz_id']
    quiz = Quiz.objects.get(id = quiz_id)

    return render(request,'detail.html',{"quiz":quiz})



def upload(request):
    template = "upload.html"

    prompt = {
        'order' : 'order of the csv should be content,category,example1,example2,example3,source,ans'
    }
    if request.method == "GET":
        return render(request,template,prompt)
    
    csv_file = request.FILES['file'] 
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter = ',', quotechar="|"):
        _, created = Quiz.objects.update_or_create(
            content = column[0],
            category = column[1],
            example1 = column[2],
            example2 = column[3],
            example3 = column[4],
            source = column[5],
            ans = column[6]
        )
    context = {}
    return render(request,template,context)
