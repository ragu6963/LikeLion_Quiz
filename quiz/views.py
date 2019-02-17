from django.shortcuts import render,redirect
from .models import Quiz, History
import csv,io

def index(request):

    return render(request,'index.html')

def quiz(request):  
    try:
        history_id = request.GET['history_id']
        history = History.objects.get(id = history_id)
        quiz = Quiz.objects.all()

        for ex in history.qu.keys():
            quiz = quiz.exclude(id = ex)
        history.save()
        quiz = quiz.order_by('?').first()  
        return render(request,'quiz.html',{"quiz":quiz,"history":history})

    except:
        history = History() 
        quiz = Quiz.objects.all()
        quiz = quiz.order_by('?').first()  
        history.qu={}
        history.save()
        return render(request,'quiz.html',{"quiz":quiz,"history":history})

def check(request):
    history_id = request.GET['history_id']
    history = History.objects.get(id = history_id)
    
    sel = request.GET['sel']
    quiz_id = request.GET['quiz_id']
    quiz = Quiz.objects.get(id = quiz_id)
    ans = quiz.ans 

    if sel == ans:
        res = "정답"
    else :
        res = "오답"


    history.qu[quiz.id] = res
    history.save()
    count = 0
    for key in history.qu.keys():
        count= count+1
    return render(request,'check.html',{"sel":sel,"ans":ans,"res":res,"history":history,"count":count})

def result(request):
    history_id = request.GET['history_id']
    history = History.objects.get(id = history_id)
    res = {}
    for key,value in history.qu.items():
        res[key] = value

    return render(request,'result.html',{"res":res,"history_id":history_id})

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