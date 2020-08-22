from django.db import models
from django.utils import timezone
from datetime import timedelta
# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date_published', default=timezone.now())

    def __str__(self):
        return f"{self.id} - {self.question_text}"

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - timedelta(days=1)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
