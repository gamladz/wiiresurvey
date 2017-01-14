from rest_framework import serializers

from surveys.models import Survey, Question, Choice, Response, Answer


class SurveySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Survey
        fields = ('url','id','name', 'description', 'date_created',
                  'date_modified', 'questions', 'responses')

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ('url','id','text', 'required', 'survey', 'type',
                  'choices','answers')

class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Choice
        fields = ('url','id','text', 'question')

class ResponseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Response
        fields = ('url','id','responder_id', 'survey', 'date_created',
                  'date_modified','answers')

class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ('url','id', 'body', 'question', 'response')
