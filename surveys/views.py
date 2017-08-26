import uuid


from django.views.generic import TemplateView
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from surveys.middleware import MessageClient
from .forms import ContactForm, SurveyForm, TextMessageForm
from .models import Survey, Question, Answer, Response


# Create your views here.

class HomeView(TemplateView):
    template_name = "surveys/home.html"


class LandingView(TemplateView):
    template_name = "surveys/landing.html"


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

class ContactView(TemplateView):
    template_name = "surveys/contact.html"



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
    form_class = TextMessageForm

    def post(self, request, *args, **kwargs):
         form = self.form_class(request.POST)
         if form.is_valid():
            patient_number = form.cleaned_data['patient_number']
            message = form.cleaned_data['message']
            MessageClient.send_message(MessageClient(),message,patient_number)

            return redirect('surveys:home')

    def get_context_data(self, **kwargs):
        context = super(SurveyDetailView, self).get_context_data(**kwargs)
        context['form'] = TextMessageForm
        return context


class ResponseDetailView(DetailView):

    model = Response
    pk_url_kwarg = 'response_pk'


    def get_context_data(self, **kwargs):
        context = super(ResponseDetailView, self).get_context_data(**kwargs)

        response_pk = self.get_object().pk
        response = Response.objects.get(pk=response_pk)

        context['answer_list'] = response.answers.all()



        return context


class ResponseListView(ListView):

    model = Response


    def get_context_data(self, **kwargs):
        context = super(ResponseListView, self).get_context_data(**kwargs)
        return context


class DemochatView(FormView):
    form_class = ContactForm
    initial = {'key': 'value'}
    template_name = "surveys/landing.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            # Send Email to new user
            name = form.cleaned_data['sender_name']
            patient_number = form.cleaned_data['patient_number']
            from_email = form.cleaned_data['from_email']
            recipients = ['gameli.ladzekpo@gmail.com']
            subject = 'Success: ' + name + ', your questionnaire was sent with Wiire'
            message = 'Hi ' + name + ', You just sent a to' + patient_number + ' questionnaire with Wiire. \n\n As soon as the recipeint has completed it, you will be sent another email with a link for you to view the results. We do not ask the recipeint for any personal inforomation. Thanks for stopping by \n\n Thanks for using Wiire\n\nGam'

            recipients.append(from_email)
            send_mail(subject, message, from_email, recipients)

            MessageClient.send_message(MessageClient(), name, patient_number)

            return HttpResponseRedirect(reverse('surveys:success'))

        return render(request, self.template_name, {'form': form})

@require_POST
def redirects_twilio_request_to_proper_endpoint(request):
    answering_question = request.session.get('answering_question_id')
    if not answering_question:
        first_survey = Survey.objects.first()

        redirect_url = reverse('surveys:twilio_survey',
                               kwargs={'survey_id': first_survey.id})
    else:
        question = Question.objects.get(id=answering_question)
        redirect_url = reverse('surveys:save_response',
                               kwargs={'survey_id': question.survey.id,
                                       'question_id': question.id})
    return HttpResponseRedirect(redirect_url)


@csrf_exempt
def show_survey(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    first_question = survey.first_question

    first_question_ids = {
        'survey_id': survey.id,
        'question_id': first_question.id
    }

    first_question_url = reverse('surveys:question', kwargs=first_question_ids)

    welcome = 'Great, text reminders will help you take your medication properly so you can feel better'
    if request.is_sms:
        twiml_response = MessagingResponse()
        twiml_response.message(welcome)
        twiml_response.redirect(first_question_url, method='GET')
    else:
        twiml_response = VoiceResponse()
        twiml_response.say(welcome)
        twiml_response.redirect(first_question_url, method='GET')

    return HttpResponse(twiml_response, content_type='application/xml')

@require_GET
def show_question(request, survey_id, question_id):
    question = Question.objects.get(id=question_id)
    if request.is_sms:
        twiml = sms_question(question)
    else:
        twiml = voice_question(question)

    request.session['answering_question_id'] = question.id
    return HttpResponse(twiml, content_type='application/xml')


def map_choices_dict(question):
    choices_dict = {}
    choices = question.choices.all()
    count = 1
    for choice in choices:
        choices_dict[count] = (choice.id, choice.text,)
        count += 1

    return choices_dict


def render_select_one_choices(question):
    # '1 - Not at all\n2 - Several days\n3- More than half the days\n4 - Nearly every day',
    choices_dict = map_choices_dict(question)
    choices_string = ''
    for key, value in choices_dict.iteritems():
        choices_string += '{key} - {value}\n'.format(key=key, value=value[1])
    return choices_string


def sms_question(question):

    sms_instructions = {
        Question.TEXT: 'Please type your answer',
        Question.SELECT_ONE: render_select_one_choices(question),
        Question.INTEGER: 'enter integer'
    }
    twiml_response = MessagingResponse()

    twiml_response.message(question.text)
    twiml_response.message(sms_instructions[question.type])

    return twiml_response

def voice_question(question):
    twiml_response = VoiceResponse()

    twiml_response.say(question.text)
    twiml_response.say(VOICE_INSTRUCTIONS[question.type])

    action = save_response_url(question)
    if question.type == Question.TEXT:
        twiml_response.record(
            action=action,
            method='POST',
            max_length=6,
            transcribe=True,
            transcribe_callback=action
        )
    else:
        twiml_response.gather(action=action, method='POST')
    return twiml_response


@require_POST
def save_response(request, survey_id, question_id):

    responder_id = request.COOKIES['sessionid']
    survey = Survey.objects.get(id=survey_id)

    try:
        response = Response.objects.get(responder_id=responder_id,
                                    survey=survey)
    except ObjectDoesNotExist:
        response = Response.objects.create(responder_id=responder_id,
                                    survey=survey)

    # response = Response.objects.get(responder_id=responder_id,
    #                                 survey=survey)
    # if not response:
    #     response = Response.objects.create(responder_id=responder_id,
    #                                        survey=survey).save()

    question = Question.objects.get(id=question_id)

    save_response_from_request(request, question, response)

    next_question = question.next()
    if not next_question:
        return goodbye(request)
    else:
        return next_question_redirect(next_question.id, survey_id)


def next_question_redirect(question_id, survey_id):
    parameters = {'survey_id': survey_id, 'question_id': question_id}
    question_url = reverse('surveys:question', kwargs=parameters)

    twiml_response = MessagingResponse()
    twiml_response.redirect(url=question_url, method='GET')
    return HttpResponse(twiml_response)


def goodbye(request):
    goodbye_messages = ['That was the last question',
                        'your answers will be used to provide you with the best care']
    if request.is_sms:
        response = MessagingResponse()
        [response.message(message) for message in goodbye_messages]
    else:
        response = VoiceResponse()
        [response.say(message) for message in goodbye_messages]
        response.hangup()

    return HttpResponse(response)


def save_response_from_request(request, question, response):
    # session_id = request.POST['MessageSid' if request.is_sms else 'CallSid']

    request_body = _extract_request_body(request, question.type)
    phone_number = request.POST['From']

    choices_dict = map_choices_dict(question)
    choice_id = choices_dict[int(request_body)][0]
    choice = question.choices.get(id=choice_id)

    Answer.objects.create(selected_choice=choice,
                         phone_number=phone_number,
                         body=request_body,
                         question=question,
                         response=response).save()

def _extract_request_body(request, question_kind):
    Question.validate_kind(question_kind)

    if request.is_sms:
        key = 'Body'
    elif question_kind in [Question.YES_NO, Question.NUMERIC]:
        key = 'Digits'
    elif 'TranscriptionText' in request.POST:
        key = 'TranscriptionText'
    else:
        key = 'RecordingUrl'

    return request.POST.get(key)


@require_GET
def show_survey_results(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    responses_to_render = [answer.as_dict() for answer in survey.answers]

    template_context = {
        'responses': responses_to_render,
        'survey_title': survey.title
    }

    return render_to_response('results.html', context=template_context)
