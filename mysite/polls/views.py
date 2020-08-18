from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, Http404

from .models import Question


def index(request):
    questions = Question.objects.order_by('-pub_date')[:5]
    context = {
        "questions": questions
    }
    return render(request, "polls/index.html", context=context)


def details(request, question_id):
    try:
        question = get_object_or_404(Question, pk=question_id)
        context = {
            "question": question
        }
    except Question.DoesNotExist:
        raise Http404("404")

    return render(request, "polls/details.html", context=context)


def results(request, question_id):
    return HttpResponse(f"results {question_id}")


def vote(request, question_id):
    return HttpResponse(f"vote {question_id}")
