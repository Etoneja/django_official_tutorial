from django.contrib import admin
from .models import Question, Answer

# Register your models here.


class AnswersInline(admin.TabularInline):

    model = Answer
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {"fields": ["question_text", "slug"]}),
        ("Published date", {"fields": ["pub_date"]}),
    ]
    inlines = [AnswersInline]
    list_display = (
        "id", "question_text", "slug", "pub_date", "was_published_recently"
    )
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    prepopulated_fields = {"slug": ("question_text", )}


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):

    raw_id_fields = ("question", )

