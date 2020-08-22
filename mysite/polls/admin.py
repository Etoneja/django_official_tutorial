from django.contrib import admin
from .models import Question, Answer

# Register your models here.


class AnswersInline(admin.TabularInline):

    model = Answer
    extra = 2


class QuestionAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Published date", {"fields": ["pub_date"]}),
    ]
    inlines = [AnswersInline]
    list_display = (
        "question_text", "pub_date", "was_published_recently"
    )
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
