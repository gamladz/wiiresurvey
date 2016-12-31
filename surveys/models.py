from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Survey(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    question_text = models.TextField()
    required = models.BooleanField(default=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    TEXT = 'TEXT'
    RADIO = 'RADIO'
    SELECT_MULTIPLE = 'SELECT MULTIPLE'
    INTEGER = 'INTEGER'
    QUESTION_TYPE_CHOICES = (
        (TEXT, 'Text'),
        (RADIO, 'Radio'),
        (SELECT_MULTIPLE, 'Select multiple'),
        (INTEGER, 'Integer'),
    )
    question_type = models.CharField(
        max_length=50,
        choices=QUESTION_TYPE_CHOICES,
        default=TEXT,
    )

    # To do:
    # Figure out if this is best approach or if we need to create a separate model instance for this
    choices = models.TextField(blank=True, null=True, help_text='Enter comma separated values')

    def __str__(self):
        return self.question_text

# To do:
# Have this model inline with question so user can enter the choices as they fill the questions
# Have a way to let the user know that this is not necessary if the question type selected is Text
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    def __str__(self):
        return self.choice_text


class Response(models.Model):
    """
    This provides a way to get a collection of questions and answers
    from a particular user for a particular survey.
    """
    response_id = models.CharField(max_length=150)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.response_id


class Answer(models.Model):
    answer_body = models.TextField(blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)


    def __str__(self):
        return self.answer_body
