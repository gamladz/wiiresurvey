
import json
from .models import Survey, Question


class SurveyLoader(object):

    def __init__(self, survey_content):
        self.survey = json.loads(survey_content)

    def load_survey(self):
        new_survey = Survey(name=self.survey['name'])
        questions = [Question(text=question['text'],
                              type=question['type'])
                     for question in self.survey['questions']]
        new_survey.save()

        new_survey.questions.add(*questions)
