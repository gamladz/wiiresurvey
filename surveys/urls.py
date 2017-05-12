from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

import views


app_name = 'surveys'
urlpatterns = [
    url(r'^$',  views.HomeView.as_view(), name='home'),
    url(r'^about/$',  views.AboutView.as_view(), name='about'),
    url(r'^blog/$',  views.BlogView.as_view(), name='blog'),
    url(r'^privacy-policy/$',  views.PrivacyView.as_view(), name='privacypolicy'),
    url(r'^pricing/$',  views.PricingView.as_view(), name='pricing'),
    url(r'^demochat/$',  views.DemochatView.as_view(), name='demochat'),
    url(r'^success/$',  views.SuccessView.as_view(), name='success'),
    url(r'^thanks/$',  views.ThanksView.as_view()),
    url(r'^survey/(?P<survey_pk>[0-9]+)/$', views.SurveyView.as_view(), name='survey'),
    url(r'^surveylist/$', views.SurveyListView.as_view(), name='survey-list'),
    url(r'^responselist/$', views.ResponseListView.as_view(), name='response-list'),
    url(r'^survey-detail/(?P<survey_pk>[0-9]+)/$', views.SurveyDetailView.as_view(), name='survey-detail'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^first-survey/$',
        csrf_exempt(views.redirects_twilio_request_to_proper_endpoint),
        name='first_survey'),
    url(r'^twilio_survey/(?P<survey_id>\d+)$',
        views.show_survey,
        name='twilio_survey'),
    url(r'^survey/(?P<survey_id>\d+)/question/(?P<question_id>\d+)$',
        views.show_question,
        name='question'),
        url(r'^survey/(?P<survey_id>\d+)/results$',
        views.show_survey_results,
        name='survey_results'),
    url(r'^survey/(?P<survey_id>\d+)/question/(?P<question_id>\d+)/question_response$',
        csrf_exempt(views.save_response),
        name='save_response')
    ]
