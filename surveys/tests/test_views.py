from django.test import TestCase, Client
from django.urls import reverse
from django.template.loader import render_to_string

from surveys.models import Response, Survey


# Create your tests here.
class SurveyViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.survey1 = Survey.objects.create(name='survey1')

    def test_survey_route_loads_successfully(self):
        data = {'survey_pk': self.survey1.id}
        response = self.client.get(reverse('surveys:survey', kwargs=data))
        self.assertEqual(response.status_code, 200)

    def test_survey_loads_with_correct_context(self):
        data = {'survey_pk': self.survey1.id}
        response = self.client.get(reverse('surveys:survey', kwargs=data))
        # Check that the rendered context contains survey and survey_form.
        self.assertIn('survey', response.context.keys())
        self.assertIn('survey_form', response.context.keys())

    def test_user_cannot_fill_same_survey_twice(self):
        responder_id = self.client.session.session_key
        Response.objects.create(responder_id=responder_id, survey=self.survey1)
        data = {'survey_pk': self.survey1.id}

        response = self.client.get(reverse('surveys:survey', kwargs=data))
        self.assertContains(response, "You have filled this form before")

        response = self.client.post(reverse('surveys:survey', kwargs=data))
        self.assertContains(response, "You have filled this form before")

    def test_correct_template_was_rendered_with_view(self):
        data = {'survey_pk': self.survey1.id}
        response = self.client.get(reverse('surveys:survey', kwargs=data))

        self.assertTemplateUsed(response, 'surveys/survey.html')


class HomeViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_view_route_loads_successfully(self):
        response = self.client.get(reverse('surveys:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_loads_with_correct_template(self):
        response = self.client.get(reverse('surveys:home'))
        self.assertTemplateUsed(response, 'surveys/home.html')


class PricingViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_pricing_view_route_loads_successfully(self):
        response = self.client.get(reverse('surveys:pricing'))
        self.assertEqual(response.status_code, 200)

    def test_pricing_view_loads_with_correct_template(self):
        response = self.client.get(reverse('surveys:pricing'))
        self.assertTemplateUsed(response, 'surveys/pricing.html')

class AboutViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_pricing_view_route_loads_successfully(self):
        response = self.client.get(reverse('surveys:about'))
        self.assertEqual(response.status_code, 200)

    def test_pricing_view_loads_with_correct_template(self):
        response = self.client.get(reverse('surveys:about'))
        self.assertTemplateUsed(response, 'surveys/about.html')

class SuccessViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_pricing_view_route_loads_successfully(self):
        response = self.client.get(reverse('surveys:success'))
        self.assertEqual(response.status_code, 200)

    def test_pricing_view_loads_with_correct_template(self):
        response = self.client.get(reverse('surveys:success'))
        self.assertTemplateUsed(response, 'surveys/success.html')
