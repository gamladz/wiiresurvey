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




    """
    QRcode = models.ImageField(upload_to='QRcode', blank=True, null=True)
    def get_absolute_url(self):
        return reverse('surveys:survey', args=[str(self.id)])
    def save(self):
        self.generate_qrcode()
        force_update = False
        # If the instance already has been saved, it has an id and we set
        # force_update to True
        if self.id:
            force_update = True
        # Force an UPDATE SQL query if we're editing the image to avoid integrity exception
        super(Survey, self).save(force_update=force_update)
    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )
        qr.add_data(self.get_absolute_url())
        qr.make(fit=True)
        image = qr.make_image()
        temp_handle = StringIO.StringIO()
        image.save(temp_handle, 'png')
        temp_handle.seek(0)
        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.QRcode.name)[-1],
                temp_handle.read(), content_type='image/png')
        # Save SimpleUploadedFile into QR code field field
        self.QRcode.save(
            '%s_QRcode.%s' % (os.path.splitext(suf.name)[0], 'png'),
            suf,
            save=False
        )
    """

    def __str__(self):
        return self.name



class Question(models.Model):

    text = models.TextField()
    required = models.BooleanField(default=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")

    TEXT = 'TEXT'
    SELECT_ONE = 'SELECT ONE'
    SELECT_MULTIPLE = 'SELECT MULTIPLE'
    INTEGER = 'INTEGER'
    QUESTION_TYPE_CHOICES = (
        (TEXT, 'Text'),
        (SELECT_ONE, 'Select one'),
        (SELECT_MULTIPLE, 'Select multiple'),
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

    def __str__(self):
        return self.text

    """

    Class Report(models.Model)

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="responses")
    questions = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="responses")
    OverallSentiment = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="responses")
    OverallVotes = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="responses")
    proportion of answers with a value over some arbitraty marker


    This provides a way to get an overview of questions, choices and answers

    The form should post to the Report Model - A class based view
    And overall responses

    click on the survey has an associated report view.
    """


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


class Answer(models.Model):

    body = models.TextField(blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    response = models.ForeignKey(Response, on_delete=models.CASCADE, null=True,  related_name="answers")
    call_sid = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)

    # Some answers has a sentiment rating, dependent on the body text assuming the associated question is of type free text, can be nullable
    # counter =


    def __str__(self):
        return self.body

    def as_dict(self):
        return {
                'text': self.question.body,
                'type': self.question.kind,
                'response': self.response,
                'call_sid': self.call_sid,
                'phone_number': self.phone_number,
                }


