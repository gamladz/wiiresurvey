import uuid
from django.views.generic import TemplateView
from django.views import View
from django.views.generic.edit import FormView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.urls import reverse
from django.db import IntegrityError
from .forms import ContactForm, SurveyForm
from .models import Survey



# Create your views here.

class HomeView(TemplateView):
    template_name = "surveys/home.html"


class BlogView(TemplateView):
    template_name = "surveys/blog.html"


class PricingView(TemplateView):
    template_name = "surveys/pricing.html"


class AboutView(TemplateView):
    template_name = "surveys/about.html"


class PrivacyView(TemplateView):
    template_name = "surveys/privacypolicy.html"


class SuccessView(TemplateView):
    template_name = "surveys/success.html"


class ThanksView(TemplateView):
    template_name = "surveys/thanks.html"


def survey(request, survey_id):
    return render(request, 'surveys/signup.html', {})


class SurveyView(View):

    def get(self, request,  *args, **kwargs):
        survey_pk = kwargs.get('survey_pk')
        survey = get_object_or_404(Survey, pk=survey_pk)

        survey_form = SurveyForm(survey=survey)

        context = {
            'survey_form': survey_form,
            'survey': survey
        }
        return render(request, 'surveys/survey.html', context)

    def post(self, request, *args, **kwargs):

        survey_pk = kwargs.get('survey_pk')
        survey = get_object_or_404(Survey, pk=survey_pk)
        survey_form = SurveyForm(request.POST, survey=survey)

        # get the nickname if any was passed in

        responder_id = request.session.session_key

        if responder_id is None:
            responder_id = uuid.uuid4()

        if survey_form.is_valid():
            try:
                survey_form.save(survey, responder_id)
                # redirect to the response page
                return HttpResponseRedirect(reverse('surveys:success'))
            except IntegrityError:
                return HttpResponse("You have filled this form before")

        else:
            # re-render form with errors
            context = {
                'survey_form': survey_form,
                'survey': survey
            }
            return render(request, 'surveys/survey.html', context)


class SignupView(FormView):
    form_class = ContactForm
    initial = {'key': 'value'}
    template_name = "surveys/signup.html"


    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>


            organisation = form.cleaned_data['organisation']
            name = form.cleaned_data['name']
            subject = 'Hey ' + name + ', Get Started with Wiire'
            message = 'Hi ' + name + ', thanks for stopping by. I personally reach out to everyone who visits our website. I\'ll send you an email to get started in the next day or so to get Wiire up and running with ' + organisation + '. Thanks for your interest!\n\nBe in touch soon,\n\nGam'

            from_email = form.cleaned_data['from_email']

            recipients = ['gameli.ladzekpo@gmail.com']
            recipients.append(from_email)

            send_mail(subject, message, from_email, recipients)


            return HttpResponseRedirect(reverse('success'))

        return render(request, self.template_name, {'form': form})

  # For reportView pass in Report model and use chartjs



