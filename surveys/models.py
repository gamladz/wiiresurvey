from django.db import models


class Survey(models.Model):

    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

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

    def __str__(self):
        return self.text


class Choice(models.Model):

    text = models.CharField(max_length=200, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")

    def __str__(self):
        return self.text


class Response(models.Model):
    """
    This provides a way to get a collection of questions and answers
    from a particular user for a particular survey.
    """
    responder_id = models.CharField(max_length=150)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="responses")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.responder_id


class Answer(models.Model):

    body = models.TextField(blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    response = models.ForeignKey(Response, on_delete=models.CASCADE, null=True,  related_name="answers")

    def __str__(self):
        return self.body
