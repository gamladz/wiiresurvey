from rest_framework import viewsets
from surveys.models import Survey, Question, Choice, Response, Answer
import serializers


class SurveyViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions to the Survey model.
    """
    queryset = Survey.objects.all()
    serializer_class = serializers.SurveySerializer

    def perform_create(self, serializer):
        serializer.save()

class QuestionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions to the Question model.
    """
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer

    def perform_create(self, serializer):
        serializer.save()

class ChoiceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions to the Choice model.
    """
    queryset = Choice.objects.all()
    serializer_class = serializers.ChoiceSerializer

    def perform_create(self, serializer):
        serializer.save()

class ResponseViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions to the Response model.
    """
    queryset = Response.objects.all()
    serializer_class = serializers.ResponseSerializer

    def perform_create(self, serializer):
        serializer.save()

class AnswerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions to the Answer model.
    """
    queryset = Answer.objects.all()
    serializer_class = serializers.AnswerSerializer

    def perform_create(self, serializer):
        serializer.save()
