from django.test import TestCase
from surveys.models import Survey
from django.core.exceptions import ValidationError

# Create your tests here.
class SurveyTest(TestCase):
    """Tests the survey Model """

    def setUp(self):
        Survey.objects.create(name='survey1')

    def test_duplicate_survey_cannot_be_saved(self):
        survey1 = Survey(name='survey1')

        self.assertRaises(ValidationError, survey1.save)


    def test_case_insensitivity_for_duplicate_surveys(self):
        survey2 = Survey(name='SURvey1')

        self.assertRaises(ValidationError, survey2.save)

    def test_edited_survey_cannot_be_a_duplicate(self):
         Survey.objects.create(name='survey2')

         survey = Survey.objects.get(name='survey2')
         survey.name = 'survey1'
         self.assertRaises(ValidationError, survey.save)






