import uuid
from django.views.generic import TemplateView
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.urls import reverse
from django.db import IntegrityError
from .forms import ContactForm, SurveyForm
from .models import Survey
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from surveys.forms import SignUpForm


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
    template_name = "surveys/survey_list.html"


class ThanksView(TemplateView):
    template_name = "surveys/thanks.html"


class SurveyDetailView(DetailView):
    model = Survey

# def survey(request, survey_id):
#     return render(request, 'surveys/signup.html', {})


class SurveyView(View):

    def get(self, request, *args, **kwargs):
        survey_pk = kwargs.get('survey_pk')
        survey = get_object_or_404(Survey, pk=survey_pk)
        session_id = request.session.session_key

        if survey.responses.all().filter(responder_id=session_id):
            return HttpResponse("You have filled this form before")

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

class SurveyListView(ListView):

    model = Survey


    def get_context_data(self, **kwargs):
        context = super(SurveyListView, self).get_context_data(**kwargs)
        return context

class SurveyDetailView(DetailView):

    model = Survey
    pk_url_kwarg = 'survey_pk'

    def get_context_data(self, **kwargs):
        context = super(SurveyDetailView, self).get_context_data(**kwargs)
        return context


class DemochatView(FormView):
    form_class = ContactForm
    initial = {'key': 'value'}
    template_name = "surveys/demochat.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            organisation = form.cleaned_data['organisation']
            name = form.cleaned_data['name']
            subject = 'Hey ' + name + ', Get Started with Wiire'
            message = 'Hi ' + name + ', thanks for stopping by. I  personally reach out to everyone who visits our website. I\'ll send you an email to get started in the next day or so to get Wiire up and running with ' + organisation + '. Thanks for your interest!\n\nBe in touch soon,\n\nGam'

            from_email = form.cleaned_data['from_email']

            recipients = ['gameli.ladzekpo@gmail.com']
            recipients.append(from_email)

            send_mail(subject, message, from_email, recipients)

            return HttpResponseRedirect(reverse('surveys:success'))

        return render(request, self.template_name, {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('surveys:home')
    else:
        form = SignUpForm()
    return render(request, 'surveys/signup.html', {'form': form})


