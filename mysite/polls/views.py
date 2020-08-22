from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailsView(generic.DetailView):
    template_name = "polls/details.html"
    model = Question


class ResultsView(generic.DetailView):
    template_name = "polls/results.html"
    model = Question


def vote(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    try:
        answer_id = request.POST["answer_id"]
    except Exception as e:
        return render(request, "polls/details.html", context={
            "question": question,
            "error_message": "something wrong"
        })


    selected_choice = question.answer_set.get(pk=answer_id)
    selected_choice.votes += 1
    selected_choice.save()

    return HttpResponseRedirect(
        reverse("polls:results", args=(question_id, ))
    )
