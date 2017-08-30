import qrcode
import StringIO

import os.path
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.text import slugify

# USER Class


class Survey(models.Model):

    name = models.CharField(max_length=150)
    slug = models.SlugField(null=True, unique=True, editable=False)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    @property
    def responses(self):
        return Answer.objects.filter(question__survey__id=self.id)

    @property
    def first_question(self):
        return Question.objects.filter(survey__id=self.id
                                       ).order_by('id').first()


    def clean(self):
        self.slug = slugify(self.name)

        if Survey.objects.filter(slug=self.slug).exists():
            try:
                self.validate_unique()
            except ValidationError:
                raise ValidationError(_("Entry with {0} already exists.".format(
                                self.name)))



    def save(self, *args, **kwargs):
        self.clean()
        return super(Survey, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of the model.
        """
        return reverse('surveys:survey-detail', args=[str(self.id)])

    def __str__(self):
        return self.name



class Question(models.Model):

    text = models.TextField()
    required = models.BooleanField(default=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")

    TEXT = 'TEXT'
    SELECT_ONE = 'SELECT ONE'
    INTEGER = 'INTEGER'
    QUESTION_TYPE_CHOICES = (
        (TEXT, 'Text'),
        (SELECT_ONE, 'Select one'),
        (INTEGER, 'Integer'),
    )
    type = models.CharField(
        max_length=50,
        choices=QUESTION_TYPE_CHOICES,
        default=TEXT,
    )

    @classmethod
    def validate_kind(cls, type):
        if type not in [cls.SELECT_ONE, cls.INTEGER, cls.TEXT]:
            raise ValidationError("Invalid question type")


    def next(self):
        survey = Survey.objects.get(id=self.survey_id)


        next_questions = \
            survey.questions.order_by('id').filter(id__gt=self.id)

        return next_questions[0] if next_questions else None

    def __str__(self):
        return self.text


class Choice(models.Model):

    text = models.CharField(max_length=200, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    weighting = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.text



class Response(models.Model):
    """
    This provides a way to get a collection of questions and answers
    from a particular user for a particular survey.
    """
    responder_id = models.CharField(max_length=150, unique=True)
    survey = models.ForeignKey(Survey, null=True, on_delete=models.CASCADE, related_name="responses")
    Age = models.IntegerField(null=True)
    Occupation = models.CharField(max_length=150, null=True)
    Gender = models.CharField(max_length=150, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.responder_id

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of the model.
        """
        return reverse('surveys:response-detail', args=[str(self.id)])


class Answer(models.Model):

    body = models.TextField(blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    response = models.ForeignKey(Response, on_delete=models.CASCADE, null=True,  related_name="answers")
    call_sid = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    selected_choice = models.ForeignKey(Choice, null=True, blank=True, on_delete=models.CASCADE, related_name="answers")



    def __str__(self):
        return self.body or self.selected_choice.text

    def as_dict(self):
        return {
                'text': self.question.body,
                'type': self.question.kind,
                'response': self.response,
                'call_sid': self.call_sid,
                'phone_number': self.phone_number,
                }
