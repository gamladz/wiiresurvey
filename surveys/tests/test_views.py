from django.test import TestCase, Client
from django.urls import reverse
from surveys.models import Response, Survey


# Create your tests here.
class SurveyViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.survey1 = Survey.objects.create(name='survey1')

    def test_survey_route_loads_successfully(self):
        data = {'survey_pk': self.survey1.id}
        response = self.client.get(reverse('surveys:survey', kwargs=data))
        import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 200)




    # def test_survey_view_with_correct_context(self):

    #
    #     If the survey has not been completed (session.id) already
    # exists in database, we should be able to get
    #     sthe survey with the right context.

    #     self.assertContains(response,
    #         "You have filled this form before.")
    #

    # def test_survey_view_with_completed_response(self):

    #     If the survey has already been completed, we should expect
    #     an appropriate message to be displayed

    #     self.assertContains(response,
    #         "You have filled this form before.")






