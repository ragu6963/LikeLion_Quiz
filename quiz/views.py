from django.shortcuts import render, redirect
from .models import Quiz, History, Challenge
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import permission_required
import csv
import io
import operator


def index(request): 

    return render(request, 'index.html')


def start(request):
    return render(request, 'start.html')


def quiz(request):
    if request.method == "POST":
        history_id = request.POST['history']
        quiz_id = request.POST['quiz']
        history = History.objects.get(id=history_id)
        quiz = Quiz.objects.get(id=quiz_id)
        select = request.POST['select']

        if select == quiz.ans:
            history.set[quiz_id] = "O"
        else:
            history.set[quiz_id] = "X"

        quiz = Quiz.objects.all()
        for ex in history.set.keys():
            quiz = quiz.exclude(id=ex)

        history.count = history.count + 1
        history.save()

        if history.count == 13:
            result = {}

            for key, value in history.set.items():
                result[key] = value

            right = 0

            for value in history.set.values():
                if value == "O":
                    right = right+1
            return render(request, 'result.html', {"history": history, "right": right, "result": result,})
        else:
            quiz = quiz.order_by('?').first()

            return render(request, 'quiz.html', {"quiz": quiz, "history": history})

    if request.method == "GET":
        history = History()
        quiz = Quiz.objects.all()
        quiz = quiz.order_by('?').first()
        history.set = {}
        history.count = 1
        history.save()
        return render(request, 'quiz.html', {"quiz": quiz, "history": history}) 

def detail(request):
    quiz_id = request.GET['quiz_id']
    quiz = Quiz.objects.get(id=quiz_id)

    return render(request, 'detail.html', {"quiz": quiz})

@permission_required('admin can_add')
def upload(request):
    template = "upload.html"

    prompt = {
        'order': 'order of the csv should be content,category,example1,example2,example3,source,ans'
    }
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Quiz.objects.update_or_create(
            content=column[0],
            category=column[1],
            example1=column[2],
            example2=column[3],
            example3=column[4],
            source=column[5],
            ans=column[6]
        )
    context = {}
    return render(request, template, context)
