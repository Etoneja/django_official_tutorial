from django.db import models
from django.db.models import Manager
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
# Create your models here.


class QuestionManager(Manager):

    def get_queryset(self):
        return super().get_queryset()\
            .filter(pub_date__lte=timezone.now())\
            .order_by('-pub_date')


class Question(models.Model):
    question_text = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date_published', default=timezone.now)
    slug = models.SlugField(max_length=255, unique_for_date="pub_date")

    def __str__(self):
        return f"{self.id} - {self.question_text}"

    def was_published_recently(self):
        now = timezone.now()
        return now - timedelta(days=1) <= self.pub_date <= now

    def get_absolute_url(self):
        return reverse(
            "polls:details", args=(self.pk, )
        )

    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recentrly"
    was_published_recently.admin_order_field = "pub_date"

    objects = Manager()
    published = QuestionManager()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id} - {self.choice_text}"
