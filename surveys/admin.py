from django.contrib import admin

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from .models import Survey, Question, Answer, Choice, Response


class ChoiceInline(NestedStackedInline):
    model = Choice
    extra = 1

class QuestionInline(NestedStackedInline):
    model = Question
    extra = 0

    inlines = [ChoiceInline]
    search_fields = ['question']

@admin.register(Survey)
class SurveyAdmin(NestedModelAdmin):
    readonly_fields = ('slug',)
    inlines = [QuestionInline]

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    model = Response

    inlines = [AnswerInline]

