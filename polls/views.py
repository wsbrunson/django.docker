from datetime import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
import django_rq

from .models import Question
from .jobs import test_queue



def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    print('hello there')
    scheduler = django_rq.get_scheduler('default')
    scheduler.schedule(
        scheduled_time=datetime.utcnow(),
        func=test_queue,
        interval=60,
        repeat=None,
    )
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)